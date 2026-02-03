from uuid import UUID, uuid4 as guid

# from props_testing import PropertyDisplay
from models.USDM.biomedical_concept_package import BiomedicalConceptPackage
from models.USDM.repository import Repository
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

    categories:list[USDM_Category]
    current_category:USDM_Category
    biomedical_concepts_in_category:list[USDM_BC]
    all_biomedical_concepts:list[USDM_BC]
    selected_biomedical_concept:USDM_BC
    biomedical_concepts_in_selection:list[USDM_BC]

    current_repository:Repository = None

    def select_category(self, category_list_index:int):
        self.current_category:USDM_Category = self.categories[category_list_index]

        # TODO: Get All known bcs in category from disc
        temp = API.get_biomedical_concepts_list(self.current_category.code.standard_code.code, categories=[cat.code.standard_code.code for cat in self.categories])
        available_bcs:list[USDM_BC] = [USDM_BC(row) for row in temp]

        self.biomedical_concepts_in_category = available_bcs

        return {
            "category_name":self.current_category.label,
            "bc_names": [bc.label for bc in available_bcs]}


        # TODO: Update Selected category Label
        # TODO: Get all list of bcs from api
        # TODO: Update biomedical_concepts_in_category
        # TODO: Update UI with new list

    def get_bcs_in_category(self, category_code):
        len(self.categories)
        all_codes = [cat.get_code() for cat in self.categories]
        self.biomedical_concepts_in_category = [USDM_BC(bc) for bc in API.get_biomedical_concepts_list(category_code, self.categories)]
        # self.biomedical_concepts_in_category = [USDM_BC(bc) for bc in API.get_biomedical_concepts_list(category.get_code(), all_codes)]
        return self.biomedical_concepts_in_category


    def __init__(self):
        self.biomedical_concepts_in_selection = None
        print("\033[93m [Warning] App.init: No repository found, creating new one \033[0m")
        print(f"\033[93m [Warning] App.init: Loading repositories is not supported yet \033[0m")
        self.current_repository = Repository()

        # last call during runtime
        # user_ui = UIDisplay(self, App.__APPLICATION_TITLE__, category_names=[cat.label for cat in self.categories])
        # self.display = user_ui
        self.display = BC2USDM_Window(app=self, screenName = App.__APPLICATION_TITLE__)
        # calls in init after this line are probably ran after closing the UI

    def __call__(self, *args, **kwds):
        app:App = App()

    def get_repository(self):
        '''return current repository'''
        # if self.current_repository is None:
        #     self.current_repository = Repository()
        #     # Appending a list of bcs, since the repo might have multiple lists of bcs
        #     self.current_repository.biomedical_concepts.append(self.get_bcs_in_category("AIMS"))
        #     for bc in self.current_repository.biomedical_concepts:
        #         bc.populate()
        return self.current_repository

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
        self.biomedical_concepts_in_category: list[USDM_BC] = self.get_bcs_in_category(current_category)
        return [bc.label for bc in self.biomedical_concepts_in_category]
    
    def get_category_label_by_index(self, index:int=None):
        return self.categories[index].label
    
    def select_bc(self, index:int):
        if len(self.biomedical_concepts_in_category) > 0:
            selected_bc = self.biomedical_concepts_in_category[index]
            if self.biomedical_concepts_in_selection is None:
                self.biomedical_concepts_in_selection:list[USDM_BC] = []
            self.biomedical_concepts_in_selection.append(selected_bc)
            self.set_current_bc(selected_bc)
            return selected_bc
        return None
    
    def set_current_bc(self, bc):
        self.current_bc = bc
        print(self.__dict__["current_bc"].label)
        # print(self.display.__dict__)
        # self.display.update_current_bc(bc)
        
    def get_category_labels(self):
        json_categories = API.get_latest_biomedical_concept_categories()
        usdm_categories:list[USDM_Category] = list(map(USDM_Category.from_json, json_categories))

        # sort categories by name
        usdm_categories.sort(key=lambda usdm_category: usdm_category.name)
        self.categories = usdm_categories
        return [category.label for category in self.categories]
    
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
        
    def get_current_bcs(self):
        return self.current_repository.biomedical_concepts
    
    def in_current_repository(self, id_:UUID):
        for tbc in self.get_current_bcs():
            if id_ == tbc.id_:
                return tbc
        return None
        
    def apply_to_repository(self, data:dict):
        print(data.key()[0])
        print(self.current_bc.id_)

        # if current bc != the bc being applied
        if self.current_bc.id_ != data.keys()[0]:
            current_bc = self.in_current_repository(data.keys()[0])
            if current_bc is None:
                print("SOMETHING WENT AWEFULLY WRONG")
            else:
                # Check for changes and apply them
                
                self.update_repository(current_bc, data)
            
            

        # if current bc is the bc being applied
        if data.keys()[0] == self.current_bc.id_:
            # apply any possible changes to current_bc
            # add current_bc to current_repository
            # self.current_repository.update_repository(current_bc)
            self.current_repository.add_category(self.current_category)
            

            # add current_bc's category(s) to current_repository




        


# App autostart
def main(*args):
    app:App = App()


if __name__ == "__main__":
    main()
