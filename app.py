import configparser
from uuid import UUID, uuid4 as guid

# from props_testing import PropertyDisplay
from logic.DAL.data_store import DataStore
from models import USDM
from models.USDM.biomedical_concept_package import BiomedicalConceptPackage
from models.USDM.repository import Repository
from models.USDM.therapeutic_area import TherapeuticArea
from utils.b_colors import BColors
from views.bc2usdm_window import BC2USDM_Window
from models.CDISC.BiomedicalConceptCategory import BiomedicalConceptCategory as CDISC_Category
from models.USDM.biomedical_concept_category import BiomedicalConceptCategory as USDM_Category
from models.USDM.biomedical_concept import BiomedicalConcept as USDM_BC, Code
from utils.api_utils import get_biomedical_concepts_list, get_latest_biomedical_concept_categories
from utils import api_utils as API
from utils.io.FileWriter import FileWriter as fr
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
    persistent_cdisc_repository:Repository = Repository()

    current_category:USDM_Category = None
    biomedical_concepts_in_current_category:list[USDM_BC] = []
    current_biomedical_concept:USDM_BC = None



    def __init__(self):
        super().__init__()
        config = App.load_configs()
        self.data_store = DataStore("./Resources/Cache.json")

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
        
    def apply_to_repository(self, data:dict) -> list[USDM_BC]:
        print(f"{BColors.WARNING}WARNING, changes made in the UI are currently being discarded.{BColors.ENDC}")
        # print(data.keys())
        data_id:UUID = UUID(data["id_"])
        
        # if current bc != the bc being applied
        if self.current_biomedical_concept.id_ != data_id: 
            current_bc = self.get_if_in_repository(data_id)
            print(self.get_if_in_repository(data_id))
            fresh_bc = self.get_from_cdisc_repository(data_id)
            
            if current_bc is None:
                print("Current bc does not exist in current repository")
                print("adding to repository")
                self.current_repository.add_biomedical_concept(fresh_bc)
                
                if self.current_category not in self.current_repository.bc_categories:
                    self.current_repository.bc_categories.append(self.current_category)
                return self.current_repository.biomedical_concepts.values()
            else:
                # Check for changes and apply them
                print("Checking for Changes")
                print("Applying found changes")
                raise NotImplementedError("Editing changes isn't implemented yet")
                # self.update_repository(current_bc, data)
            
            

        # if current bc is the bc being applied
        if data_id == self.current_biomedical_concept.id_ or current_bc is None:
            # apply any possible changes to current_bc
            print("applying changes to current bc")
            # current_bc = USDM_BC(**data)
            current_bc = self.current_biomedical_concept # TEMP!!
            print(f"{BColors.WARNING}WARN|[App.applyToRepo]: Currently we're not taking changes made in the UI into account{BColors.ENDC}")
            
            # if current_bc == self.current_bc: # <- doesn't work, since this only does a reference comp.
            #     self.current_bc = current_bc
            # USDM_BC.sync(self.current_bc, current_bc)
            # else:

                # add current_bc to current_repository
                # print("Adding current bc to current repo")
                # # raise NotImplementedError()
            self.current_repository.add_biomedical_concept(current_bc)
            
            # self.current_repository.update_repository(current_bc)
            if self.current_category not in self.current_repository.bc_categories:
                self.current_category.members.append(current_bc)
                self.current_repository.bc_categories.append(self.current_category)
            else:
                for cat in self.current_repository.bc_categories:
                    if cat is self.current_category and current_bc not in cat.members:
                        cat.members.append(current_bc)
            
            # print("Updating UI (Am I though?)")
            biomedical_concepts_in_repository = self.current_repository.biomedical_concepts.values()
            # self.display == None!!
            # self.display.current_repository_container.added_biomedical_concepts_container.update_added_biomedical_concepts(repo_bcs)
            return biomedical_concepts_in_repository
            # add current_bc's category(s) to current_repository
        else:
            print(f"{BColors.FAIL}App.apply_to_repo: WHAT HAPPENED?!{BColors.ENDC}")

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
        # all_codes = [cat.get_code() for cat in self.categories]
        
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

    [DeprecationWarning]
    def get_biomedical_concept_names_in_category(self, index:int = None, id_:str = None, name:str = None):
        ''' Set bc_selection to all biomedical concepts in provided category and returns a list of the related names
        Raises a ValueError if no index, id or name is provided
        Returns list[str] names
        '''
        current_category = None
        if index is not None:
            current_category = self.categories[index]
        elif id_ is None and name is None:
            # index, id and name are none. So can't provide a category
            raise ValueError("Provide an index, id or name of the category in question")
        else:
            for category in self.categories:
                if category.id_ == id_ or category.name == name:
                    current_category = category
                    break
        self.biomedical_concepts_in_current_category: list[USDM_BC] = self._get_bcs_in_category(current_category)
        return [bc.label for bc in self.biomedical_concepts_in_current_category]

    [DeprecationWarning]
    def select_category(self, category_list_index:int):
        print(f"{BColors.WARNING}[WARNING]: {self.select_bc.__qualname__} is depracated. {BColors.ENDC}")
        self.current_category:USDM_Category = self.categories[category_list_index]

        temp = API.get_biomedical_concepts_list(self.current_category.code.standard_code.code, categories=[cat.code.standard_code.code for cat in self.categories])
        available_bcs:list[USDM_BC] = [USDM_BC(row) for row in temp]

        self.biomedical_concepts_in_current_category = available_bcs

        return {
            "category_name":self.current_category.label,
            "bc_names": [bc.label for bc in available_bcs]}
    #endregion
    
    

    #region Current Biomedical Concept
    def select_bc(self, index:int):
        if len(self.biomedical_concepts_in_current_category) > 0:
            selected_bc = self.biomedical_concepts_in_current_category[index]
            
            # Populate (only) if selected bc hasn't been populated yet
            if not selected_bc._populated:
                code = selected_bc.reference.split('/')[-1]

                '''{
                    "_links":{
                        "parentBiomedicalConcept":{
                            "href":"/mdr/bc/biomedicalconcepts/C81250",
                            "title":"Functional Assessment",
                            "type":"Biomedical Concept" },
                        "parentPackage":{
                            "href":"/mdr/bc/packages/2025-11-18/biomedicalconcepts",
                            "title":"Biomedical Concept Package Effective 2025-11-18",
                            "type":"Biomedical Concept Package"},
                        "self":{
                            "href":"/mdr/bc/biomedicalconcepts/C115789",
                            "title":"6 Minute Walk Functional Test",
                            "type":"Biomedical Concept"}},
                            "conceptId":"C115789",
                            "href":"https://evsexplore.semantics.cancer.gov/evsexplore/concept/ncit/C115789",
                            "categories":[
                                "QRS",
                                "Functional Assessment",
                                "6 Minute Walk Functional Test",
                                "SIX MINUTE WALK",
                                "SIXMW1",
                                "6MWT"],
                            "shortName":"6 Minute Walk Functional Test",
                            "synonyms":["6MWT","SIXMW1","SIX MINUTE WALK"],
                            "definition":"A standardized rating scale developed by Bruno Blake in 1963, which is a performance-based evaluation of functional exercise capacity in subjects with chronic respiratory disease and heart failure, as well as other populations such as healthy older adults and people suffering from fibromyalgia and scleroderma. This functional test contains 6 items and measures the distance an individual is able to walk over a total of six minutes on a hard, flat surface.",
                            "dataElementConcepts":[
                                {"conceptId":"C82525","href":"https://evsexplore.semantics.cancer.gov/evsexplore/concept/ncit/C82525","shortName":"Test Occurrence","dataType":"string","exampleSet":["N","Y"],"ncitCode":"C82525"},
                                {"conceptId":"C25372","href":"https://evsexplore.semantics.cancer.gov/evsexplore/concept/ncit/C25372","shortName":"Category","dataType":"string","exampleSet":["SIX MINUTE WALK"],"ncitCode":"C25372"},
                                {"conceptId":"C82515","href":"https://evsexplore.semantics.cancer.gov/evsexplore/concept/ncit/C82515","shortName":"Collection Date Time","dataType":"datetime","ncitCode":"C82515"},
                                {"conceptId":"C93300","href":"https://evsexplore.semantics.cancer.gov/evsexplore/concept/ncit/C93300","shortName":"Assistive Device","dataType":"string","exampleSet":["cane"],"ncitCode":"C93300"}],
                            "ncitCode":"C115789"}'''



                json_data = API.get_latest_biomedical_concept(code)
                selected_bc.populate(**json_data)
            # lines commented out, since this shouldn't be need to be resolved in this method.
            # if self.biomedical_concepts_in_current_category is None:
            #     self.biomedical_concepts_in_current_category:list[USDM_BC] = []
            # self.biomedical_concepts_in_current_category.append(selected_bc)
            self.biomedical_concepts_in_current_category[index] = selected_bc
            self.set_current_bc(selected_bc)
            return selected_bc
        return None

    

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
