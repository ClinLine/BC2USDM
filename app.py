import configparser
from copy import deepcopy
from uuid import UUID, uuid4 as guid

# from props_testing import PropertyDisplay
# from logic.DAL.data_store import DataStore
# from models.USDM.biomedical_concept_package import BiomedicalConceptPackage
from models.USDM.repository import Repository
from models.USDM.therapeutic_area import TherapeuticArea
from utils.b_colors import BColors
from views.bc2usdm_window import BC2USDM_Window
from models.CDISC.BiomedicalConceptCategory import BiomedicalConceptCategory as CDISC_Category
from models.USDM.biomedical_concept_category import BiomedicalConceptCategory as USDM_Category
from models.USDM.biomedical_concept import BiomedicalConcept as USDM_BC, Code
from models.USDM.comment_annotation import CommentAnnotation
from utils.api_utils import get_biomedical_concepts_list, get_latest_biomedical_concept_categories
from utils import api_utils as API
# from utils.json_encoder import CustomEncoder

App_Instance:'App'

# __categories_list_width: int = 120
class App:
    _CONFIG_FILE_NAME = "config.ini"
    __APPLICATION_TITLE__ = "BC2USDM"
    # display:UIDisplay
    display:BC2USDM_Window

    categories:list[USDM_Category] = []
    biomedical_concepts:list[USDM_BC] = []

    # state:
    current_repository:Repository = None
    # persistent_cdisc_repository:Repository = Repository()

    current_category:USDM_Category = None
    biomedical_concepts_in_current_category:list[USDM_BC] = []
    
    current_biomedical_concept:USDM_BC = None
    original_biomedical_concept:USDM_BC = None



    def __init__(self):
        super().__init__()
        # config = App.load_configs()
        # self.data_store = DataStore("./Resources/Cache.json")

        self._initialize_state()


        # WARNING: last call during operation time
    
    @staticmethod
    def load_configs():
        config = configparser.ConfigParser()
        with open("config.ini", mode="r+t", encoding="UTF-8") as configfile:
            config.read(configfile)
        return config


    def start(self):
        self.display = BC2USDM_Window(app=self, screenName = App.__APPLICATION_TITLE__)
        # calls in init after this line are ran after closing the UI

    def _initialize_state(self):
        self.current_biomedical_concept = None
        self.original_biomedical_concept = None
        
        print("[Info] App.initialize_state: Initializing")
        self.biomedical_concepts_in_current_category = None
        print("\033[93m [Warning] App.initialize_state: No active repository found, creating new one \033[0m")
        print("\033[93m [Warning] App.initialize_state: Loading pre-existing repositories is not supported yet \033[0m")
        self.current_repository = Repository()
        self.persistent_cdisc_repository = Repository()
        # self.persistent_cdisc_repository.business_therapeutic_areas = [TherapeuticArea(Code(code="USDM_PD01", code_system=Code.CodeSystem.CDISC,code_system_version="latest").decode("Latest retrieved repository items"))]
        json_categories = API.get_latest_biomedical_concept_categories()
        usdm_categories:list[USDM_Category] = list(map(USDM_Category.from_json, json_categories))
        usdm_categories.sort(key=lambda usdm_category: usdm_category.name)
        self.set_categories(usdm_categories)

        print("[Info] App.initialize_state: Done")


    def __call__(self, *args, **kwds):
        app:App = App()

    #region Current Repository
    def get_repository(self):
        '''return current repository'''
        return self.current_repository
    
    def set_document_version(self, version:str):
        for ta in self.current_repository.business_therapeutic_areas:
            ta.code.code_system_version = version
    
    def set_therapeutic_area_decode(self, id_:UUID, value:str):
        if not isinstance(id_, UUID):
            id_ = UUID(id_)
        for ta in self.current_repository.business_therapeutic_areas:
            if ta.code.id_ == id_:
                ta.code.decode = value

    def get_therapeutic_areas(self, index:int=None):
        if index is not None:
            return self.current_repository.business_therapeutic_areas[index]
        else:
            return self.current_repository.business_therapeutic_areas
        
    def get_bcs_in_repository(self) -> list[USDM_BC]:
        return self.current_repository.biomedical_concepts.values()
    
    def get_if_in_repository(self, id_:UUID)-> USDM_BC | None:
        for temp_bc in self.get_bcs_in_repository():
            # print(temp_bc)
            if id_ == temp_bc.id_:
                return temp_bc
        return None
    
    def get_from_cdisc_repository(self, request_id:UUID) -> USDM_BC:
        for uuid, bc in self.persistent_cdisc_repository.biomedical_concepts.items():
            if uuid == request_id:
                return bc
        raise ValueError(f"{BColors.FAIL} Request_id should be an UUID in the cache")
        
    def apply_to_repository(self, bc_dao:dict) -> list[USDM_BC]:
        verbose_ = True
        
        if bc_dao["label"] != self.current_biomedical_concept.label:
            self.current_biomedical_concept.label = bc_dao["label"]
        elif verbose_:
            print(f"{BColors.OKBLUE}INFO|[App].apply_to_repository: Labels match, no change required.{BColors.ENDC}")
    
        
        if set(self.current_biomedical_concept.synonyms).difference(set(bc_dao["synonyms"])) != set():
            if verbose_: print(f"{BColors.OKBLUE}INFO|[App].apply_to_repository: Synonyms were changed, applying changes{BColors.ENDC}")
            self.current_biomedical_concept.synonyms = bc_dao["synonyms"]
        else:
            if verbose_: print(f"{BColors.OKBLUE}INFO|[App].apply_to_repository: Synonyms were unchanged{BColors.ENDC}")
        print(f"{BColors.WARNING}WARN|[App].apply_to_repository: since notes aren't currently displayed correctly, they are not taken into account while applying to repo{BColors.ENDC}")
        
        for prop in self.current_biomedical_concept.properties:
            dao_properties = bc_dao["properties"]
            # dao_properties_vals = bc_dao["properties"].values()
            # dao_properties_items = bc_dao["properties"].items()
            for dao_id, dao_prop  in dao_properties.items():
                if verbose_:
                    print(f"{BColors.OKBLUE}INFO|[App].apply_to_repository: prop.id_ = {prop.id_}{BColors.ENDC}")
                    print(f"{BColors.OKBLUE}INFO|[App].apply_to_repository: doa.id_ = {dao_id}{BColors.ENDC}")
                    print(f"{BColors.OKBLUE}INFO|[App].apply_to_repository: matching =  {UUID(dao_id)==prop.id_}{BColors.ENDC}")
                if UUID(dao_id) == prop.id_:
                    prop.label = dao_prop["label"]
                    prop.is_required = dao_prop["is_required"]
                    prop.is_enabled = dao_prop["is_enabled"]
                    prop.datatype = dao_prop["datatype"]

                    
                    unchanged_notes = []
                    # Since the UI only knows of the .text element of CommentAnnotations
                    # We have to separate out the notes that haven't been changed first
                    if verbose_:
                        print(f"{BColors.OKBLUE}INFO|[App].apply_to_repository: this property has {len(prop.notes)} on record.{BColors.ENDC}")
                        print(f"{BColors.OKBLUE}INFO|[App].apply_to_repository: this property has {len(dao_prop["notes"])} on in the UI.{BColors.ENDC}")
                    for note in prop.notes:
                        for note_string in dao_prop["notes"]:
                            if note.text == note_string:
                                unchanged_notes.append(note)
                                break
                    
                    # Next we run through all notes again, skipping the ones that aren't in our list of unchanged_notes
                    # Append them if they're a new note, otherwise overwrite the original if it's a change
                    for index, note in enumerate(prop.notes):
                        # If note is one of the unchanged_notes, skip it
                        if note in unchanged_notes:
                            continue
                        # if ui contains more notes than the original property, append new note to prop.notes
                        # The code is set to the default USER_DEFINE_CODE in the CommentAnnotation class
                        elif index >= len(prop.notes):
                            continue
                            # comment_annotation = CommentAnnotation(
                            #     text=dao_prop["notes"][index],
                            #     codes=[CommentAnnotation.USER_DEFINED_CODE]
                            #     )
                            # prop.notes.append(comment_annotation)
                        else: # -> current note is one of the changed notes
                            # Since lists are ordered, we assume an index match means same note, so changing the changed text should be sufficient
                            note.text = dao_prop["notes"][index]
                    
                    if len(prop.notes) < len (dao_prop["notes"]):
                        # If there are more notes in the UI than on record, add them to the record
                        if verbose_:
                            print(f"{BColors.OKBLUE}INFO|[App].apply_to_repository: UI has {len(prop.notes) - len(dao_prop["notes"])} more notes.{BColors.ENDC}")
                            print(f"{BColors.OKBLUE}INFO|[App].apply_to_repository: first note is:{len(dao_prop["notes"][len(prop.notes):][0])}{BColors.ENDC}")
                            print(f"{BColors.OKBLUE}INFO|[App].apply_to_repository: Attempting to add extra notes{BColors.ENDC}")
                        for note_str in dao_prop["notes"][len(prop.notes):]:
                            comment_annotation = CommentAnnotation(
                                text=note_str,
                                codes=[CommentAnnotation.USER_DEFINED_CODE]
                                )
                            prop.notes.append(comment_annotation)

                    # RESPONSE CODES
                    if verbose_:
                            if prop.response_codes is None:
                                print(f"{BColors.WARNING}WARN|[App].apply_to_repository: prop.response_codes should never be none, it should be [] instead{BColors.ENDC}")
                            print(f"{BColors.OKBLUE}INFO|[App].apply_to_repository: Number of Response Codes found: {len(prop.response_codes)}{BColors.ENDC}")
                            print(f"{BColors.OKBLUE}INFO|[App].apply_to_repository: first note is:{len(dao_prop["notes"][len(prop.notes):][0])}{BColors.ENDC}")
                            print(f"{BColors.OKBLUE}INFO|[App].apply_to_repository: Attempting to add extra notes{BColors.ENDC}")
                    for rc in prop.response_codes:
                        for index, rc_dict in enumerate(dao_prop["response_codes"]):
                            if rc.id_ == rc_dict["id_"]:
                                rc.label = rc_dict["label"]
                                rc.is_enabled = rc_dict["is_enabled"]
                            # If code still matches, continue to new item
                            if rc.code.code == rc_dict["code"]:
                                break
                            else:
                                rc.code = Code(
                                    code=rc_dict["code"],
                                    code_system=Code.CodeSystem.CUSTOM,
                                    code_system_version=Code.DEFAULT_CODE_SYSTEM_VERSION,
                                    decode="User defined Code")
                            break
                    # Since we encountered a match and applied the changes, we are breaking out of the inner loop, to look for the next match
                    break # break out of inner loop to continue to next prop in currentBC.props
            
        # properties: list[dict[str,obj]]
            # label:str
            # id_:str -> UUID(id_)
            # is_required:bool
            # is_enabled:bool
            # datatype:str
            # notes:list[str]
            











        
        self.current_repository.add_biomedical_concept(self.current_biomedical_concept)
        if self.current_category not in self.current_repository.bc_categories:
            self.current_category.members.append(self.current_biomedical_concept)
            self.current_repository.bc_categories.append(self.current_category)
        else:
            for cat in self.current_repository.bc_categories:
                if cat is self.current_category and self.current_biomedical_concept not in cat.members:
                    cat.members.append(self.current_biomedical_concept)
        biomedical_concepts_in_repository = self.current_repository.biomedical_concepts.values()
        return biomedical_concepts_in_repository

    def get_categories_in_repository(self):
        return self.current_repository.bc_categories
    #endregion

    #region Categories list
    def get_category_labels(self):
        categories = self.get_categories()
        return [category.label for category in categories]
    
    def get_categories(self):
        if self.categories is None or len(self.categories) == 0:
            json_categories = API.get_latest_biomedical_concept_categories()
            usdm_categories:list[USDM_Category] = list(map(USDM_Category.from_json, json_categories))
            usdm_categories.sort(key=lambda usdm_category: usdm_category.name)
            self.set_categories(usdm_categories)
        return self.categories

    def set_categories(self, categories:list[USDM_Category]):
        self.categories = categories
        self.persistent_cdisc_repository.bc_categories = categories
        # self.display.categories_container.set_categories([category.label for category in self.categories])

    #endregion
    #region Current Category
    def set_current_category_by_index(self, category_list_index:int):
        self.current_category:USDM_Category = self.categories[category_list_index]
        self.biomedical_concepts_in_current_category = self._get_bcs_in_category(self.current_category.get_code())
        for bc in self.biomedical_concepts_in_current_category:
            if bc not in self.biomedical_concepts:
                self.biomedical_concepts.append(bc)

    def get_current_category_label(self):
        return self.current_category.label
    
    # def get_category_label_by_index(self, index:int=None):
    #     return self.categories[index].label
    
    def get_biomedical_concepts_in_current_category(self):
        return self.biomedical_concepts_in_current_category
    
    def _get_bcs_in_category(self, category_code):
        json_bcs = API.get_biomedical_concepts_list(category_code, self.categories)
        biomedical_concepts_in_category:list[USDM_BC] = []
        try:
            _bcs_in_category = [USDM_BC(label=bc["title"],reference=bc["href"],instance_type=bc["type"]) for bc in json_bcs if json_bcs]
        except TypeError as err:
            print(f"{BColors.WARNING}WARN|[App]._get_bcs_in_category: {err}{BColors.ENDC}")
        else:
            biomedical_concepts_in_category = _bcs_in_category
        
        
        for bc in biomedical_concepts_in_category:
            if bc.id_ not in self.persistent_cdisc_repository.biomedical_concepts:
                self.persistent_cdisc_repository.add_biomedical_concept(bc)
        # self.persistent_cdisc_repository.biomedical_concepts.extend(self.biomedical_concepts_in_current_category)
       
        # self.biomedical_concepts_in_category = [USDM_BC(bc) for bc in API.get_biomedical_concepts_list(category.get_code(), all_codes)]
        return biomedical_concepts_in_category
    
    def get_biomedical_concept_names_in_current_category(self):
        self.biomedical_concepts_in_current_category:list[USDM_BC] = self._get_bcs_in_category(self.current_category.get_code())
        return [bc.label for bc in self.biomedical_concepts_in_current_category]

    # [DeprecationWarning]
    # def get_biomedical_concept_names_in_category(self, index:int = None, id_:str = None, name:str = None):
    #     ''' Set bc_selection to all biomedical concepts in provided category and returns a list of the related names
    #     Raises a ValueError if no index, id or name is provided
    #     Returns list[str] names
    #     '''
    #     current_category = None
    #     if index is not None:
    #         current_category = self.categories[index]
    #     elif id_ is None and name is None:
    #         # index, id and name are none. So can't provide a category
    #         raise ValueError("Provide an index, id or name of the category in question")
    #     else:
    #         for category in self.categories:
    #             if category.id_ == id_ or category.name == name:
    #                 current_category = category
    #                 break
    #     self.biomedical_concepts_in_current_category: list[USDM_BC] = self._get_bcs_in_category(current_category)
    #     return [bc.label for bc in self.biomedical_concepts_in_current_category]

    # [DeprecationWarning]
    # def select_category(self, category_list_index:int):
    #     print(f"{BColors.WARNING}[WARNING]: {self.select_category.__qualname__} is depracated. {BColors.ENDC}")
    #     self.current_category:USDM_Category = self.categories[category_list_index]

    #     temp = API.get_biomedical_concepts_list(self.current_category.code.standard_code.code, categories=[cat.code.standard_code.code for cat in self.categories])
    #     available_bcs:list[USDM_BC] = [USDM_BC(row) for row in temp]

    #     self.biomedical_concepts_in_current_category = available_bcs

    #     return {
    #         "category_name":self.current_category.label,
    #         "bc_names": [bc.label for bc in available_bcs]}
    #endregion
    
    

    #region Current Biomedical Concept
    def select_bc(self, index:int):
        if len(self.biomedical_concepts_in_current_category) > 0:
            selected_bc = self.biomedical_concepts_in_current_category[index]
            
            # Populate (only) if selected bc hasn't been populated yet
            if not selected_bc._populated:
                code = selected_bc.reference.split('/')[-1]

                
                json_data = API.get_latest_biomedical_concept(code)
                selected_bc.populate(**json_data)
            # lines commented out, since this shouldn't be need to be resolved in this method.
            # if self.biomedical_concepts_in_current_category is None:
            #     self.biomedical_concepts_in_current_category:list[USDM_BC] = []
            # self.biomedical_concepts_in_current_category.append(selected_bc)
            self.biomedical_concepts_in_current_category[index] = selected_bc
            self.original_biomedical_concept = None
            self.current_biomedical_concept = selected_bc
            return selected_bc
        return None

    def get_biomedical_concept_by_id(self, id_:UUID) -> USDM_BC | None:
        for bc in self.biomedical_concepts:
            if bc.id_ == id_:
                return bc
        print(f"{BColors.WARNING}WARN|[App].get_bc_by_id: No bc with id {id_} was found.{BColors.ENDC}")
        return None
            

    # def update_current_bc(self, name:str, value) -> None:
    #     # if self.original_biomedical_concept == None:
    #     #     id__ = self.current_biomedical_concept.id_
  
    #     #     self.original_biomedical_concept = deepcopy(self.get_biomedical_concept_by_id(id__))
        
    #     # Apply changes to current BC
    #     self.current_biomedical_concept.set_attribute(name, value)

    #     # if currentBC and originalBC
    #     if self.current_biomedical_concept != self.original_biomedical_concept:
    #         self.current_biomedical_concept.id_ = guid()
    #     if self.original_biomedical_concept.get_attribute(name) != self.current_biomedical_concept.get_attribute(name):
            
    #         self.current_biomedical_concept.id_ = guid()
    #     raise NotImplementedError("Simply getting a copy from self.biomedicalConcepts would get a mutated version, since self.currentBC is already a shallow copy of this instance")


       
        
       

    def set_current_bc(self, bc:USDM_BC):
        self.current_biomedical_concept = bc

    def get_current_bc(self):
        return self.current_biomedical_concept
    #endregion

    # TODO: Review this list
    # TODO: Update Selected category Label
    # TODO: Get all list of bcs from api
    # TODO: Update biomedical_concepts_in_category
    # TODO: Update UI with new list



# App autostart
def main(*args):
    global App_Instance
    App_Instance = App()
    App_Instance.start()

if __name__ == "__main__":
    __name__ = "BC2USDM"
    __package__ = "BC2USDM"
    main()
