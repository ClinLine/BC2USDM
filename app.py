from uuid import UUID, uuid4 as guid

# from props_testing import PropertyDisplay
from models.USDM.biomedical_concept_package import BiomedicalConceptPackage
from models.USDM.repository import Repository
from utils.b_colors import BColors
from views.bc2usdm_window import BC2USDM_Window
from models.CDISC.BiomedicalConceptCategory import BiomedicalConceptCategory as CDISC_Category
from models.USDM.biomedical_concept_category import BiomedicalConceptCategory as USDM_Category
from models.USDM.biomedical_concept import BiomedicalConcept as USDM_BC
from utils.api_utils import get_biomedical_concepts_list, get_latest_biomedical_concept_categories
from utils import api_utils as API
from utils.io.FileWriter import FileWriter as fr
# from utils.json_encoder import CustomEncoder



# __categories_list_width: int = 120
class App(object):
    __APPLICATION_TITLE__ = "BC2USDM"
    # display:UIDisplay
    display:BC2USDM_Window

    categories:list[USDM_Category] = []

    # state:
    current_repository:Repository = None
    
    current_category:USDM_Category = None
    biomedical_concepts_in_current_category:list[USDM_BC] = []
    current_biomedical_concept:USDM_BC = None

    def __init__(self):
        self._initialize_state()

        # WARNING: last call during operation time
        self.display = BC2USDM_Window(app=self, screenName = App.__APPLICATION_TITLE__)
        # calls in init after this line are ran after closing the UI

    def _initialize_state(self):
        print("[Info] App.initialize_state: Initializing")
        self.biomedical_concepts_in_current_category = None
        print("\033[93m [Warning] App.initialize_state: No active repository found, creating new one \033[0m")
        print("\033[93m [Warning] App.initialize_state: Loading pre-existing repositories is not supported yet \033[0m")
        self.current_repository = Repository()
        
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
        # if self.current_repository is None:
        #     self.current_repository = Repository()
        #     # Appending a list of bcs, since the repo might have multiple lists of bcs
        #     self.current_repository.biomedical_concepts.append(self.get_bcs_in_category("AIMS"))
        #     for bc in self.current_repository.biomedical_concepts:
        #         bc.populate()
        return self.current_repository
    
    def set_document_version(self, version:str):
        for ta in self.current_repository.business_therapeutic_areas:
            ta.code.code_system_version = version
    
    def set_therapeutic_area_decode(self, id_:guid, value:str):
        for ta in self.current_repository.business_therapeutic_areas:
            if ta.code.id_ == id_:
                ta.code.decode = value

    def get_therapeutic_areas(self, index:int=None):
        if index is not None:
            return self.current_repository.business_therapeutic_areas[index]
        else:
            return self.current_repository.business_therapeutic_areas
        
    def get_bcs_in_repository(self):
        return self.current_repository.biomedical_concepts
    
    def in_current_repository(self, id_:UUID):
        for temp_id, temp_bc in self.get_bcs_in_repository():
            print(temp_bc)
            if id_ == temp_id:
                return temp_bc
        return None
        
    def apply_to_repository(self, data:dict):
        print(data.keys())
        print(self.current_bc.id_)

        # if current bc != the bc being applied
        if self.current_bc.id_ != data["id_"]:
            current_bc = self.in_current_repository(data["id_"])
            print(self.in_current_repository(data["id_"]))
            
            
            if current_bc is None:
                print("Current bc does not exist in current repository")
            else:
                # Check for changes and apply them
                print("Checking for Changes")
                print("Applying found changes")
                # self.update_repository(current_bc, data)
            
            

        # if current bc is the bc being applied
        if data["id_"] == self.current_bc.id_ or current_bc is None:
            # apply any possible changes to current_bc
            print("applying changes to current bc")
            current_bc = USDM_BC(**data)
            self.current_bc = current_bc
            # add current_bc to current_repository
            print("Adding current bc to current repo")
            self.current_repository.add_biomedical_concept(current_bc)
            
            # self.current_repository.update_repository(current_bc)
            self.current_repository.add_category(self.current_category)
            
            print("Updating UI")
            repo_bcs = self.current_repository.biomedical_concepts
            # self.display == None!!
            self.display.current_repository_container.added_biomedical_concepts_container.update_added_biomedical_concepts(repo_bcs)
            # add current_bc's category(s) to current_repository
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
        # self.display.categories_container.set_categories([category.label for category in self.categories])

    #endregion
    #region Current Category
    def set_current_category_by_index(self, category_list_index:int):
        self.current_category:USDM_Category = self.categories[category_list_index]
        self.biomedical_concepts_in_current_category = self.get_bcs_in_category(self.current_category.get_code())

    def get_current_category_label(self):
        return self.current_category.label
    
    # def get_category_label_by_index(self, index:int=None):
    #     return self.categories[index].label
    
    def get_biomedical_concepts_in_current_category(self):
        return self.biomedical_concepts_in_current_category
    
    def get_bcs_in_category(self, category_code):
        # all_codes = [cat.get_code() for cat in self.categories]
        
        json_bcs = API.get_biomedical_concepts_list(category_code, self.categories)
        biomedical_concepts_in_category = [USDM_BC(label=bc["title"],reference=bc["href"],instance_type=bc["type"]) for bc in json_bcs]
        # self.biomedical_concepts_in_category = [USDM_BC(bc) for bc in API.get_biomedical_concepts_list(category.get_code(), all_codes)]
        return biomedical_concepts_in_category
    
    def get_biomedical_concept_names_in_current_category(self):
        self.biomedical_concepts_in_current_category:list[USDM_BC] = self.get_bcs_in_category(self.current_category.get_code())
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
        self.biomedical_concepts_in_current_category: list[USDM_BC] = self.get_bcs_in_category(current_category)
        return [bc.label for bc in self.biomedical_concepts_in_current_category]

    [DeprecationWarning]
    def select_category(self, category_list_index:int):
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
        self.current_bc = bc

    def get_current_bc(self):
        return self.current_bc
    #endregion

    # TODO: Review this list
    # TODO: Update Selected category Label
    # TODO: Get all list of bcs from api
    # TODO: Update biomedical_concepts_in_category
    # TODO: Update UI with new list



# App autostart
def main(*args):
    app:App = App()


        

# def test(categories:dict):
#     # Print references to test for inconsistencies
#     print(f"{BColors.OKCYAN.value}Print references to test for inconsistencies{BColors.ENDC.value}")
#     # for i in range(0, len(categories)):
#     count = 0
#     total = 0
    
#     l = len(categories)
#     category_codes = []
#     print(f'{BColors.OKCYAN.value}checking Category references{BColors.ENDC.value}')
#     for i, category in progressBar(categories, prefix='Checking Categories:',suffix='Complete', bar_length = 100):
        
#         category_codes.append(category['_links']['self']['href'].split('=')[-1])
#         mdr = category['_links']['self']['href'].split('/')[1]
#         if mdr != mdr:
#             count +=1
#             print(f"{BColors.FAIL.value}[{i}:]{category['_links']['self']['href']}{BColors.ENDC.value}")
#         total +=1

#         # progressBar(i+1,l,prefix='Progress:',suffix='Complete', length = 50)

    
#     print(f'{BColors.OKCYAN.value}checking BC references{BColors.ENDC.value}')
#     # for i, category_code in progressBar(category_codes, prefix="Progress", suffix="Complete", bar_length=50):
#     #     total +=1
#     #     if i < l and category_code != "Merged" and category_code != "Non-Target":
#     #         json_bcs = API.get_biomedical_concepts_list(category_code, [category_code])
            
#     #         # prefix = f'[{i}/{l}] {category_code.zfill(35)}'
#     #         for j, bc in enumerate(json_bcs):
#     #             mdr = bc['href'].split('/')[1]
#     #             if mdr != 'mdr':
#     #                 count +=1
#     #                 print(f"{BColors.FAIL.value}[{j}:]{bc['href']}{BColors.ENDC.value}")

#     bcs = API.get_biomedical_concepts_list('all')
#     l = len(bcs)
#     errors = []
#     for j, bc in progressBar(bcs, prefix=f'Progress', suffix="bcs checked", bar_length=50):
#         total +=1
#         if j < l:
#             mdr = bc['href'].split('/')[1]
#             if mdr != 'mdr':
#                 count +=1
#                 errors.append(f"{BColors.FAIL.value}[{j}:]{bc['href']}{BColors.ENDC.value}")
#                 # function.append(lambda: _ => print(f"{BColors.FAIL.value}[{j}:]{bc['href']}{BColors.ENDC.value}"))
                
#     print(*errors,sep="\n")

#     print(f"test completed, {BColors.FAIL.value}{count}{BColors.ENDC.value}/{total} references didn't start with /mdr/")        



    

if __name__ == "__main__":
    
    main()
