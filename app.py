
# from props_testing import PropertyDisplay
from models.USDM.biomedical_concept_package import BiomedicalConceptPackage
from views.ui_display import UIDisplay, BC2USDM_Window
from models.CDISC.BiomedicalConceptCategory import BiomedicalConceptCategory as CDISC_Category
from models.USDM.BiomedicalConceptCategory import BiomedicalConceptCategory as USDM_Category
from models.USDM.BiomedicalConcept import BiomedicalConcept as USDM_BC
from utils.api_utils import get_biomedical_concepts_list, get_latest_biomedical_concept_categories
from utils import api_utils as API
from utils.io.FileWriter import FileWriter as fr
# from utils.json_encoder import CustomEncoder




# __categories_list_width: int = 120
class App(object):
    __APPLICATION_TITLE__ = "BC2USDM"
    display:UIDisplay

    categories:list[USDM_Category]
    biomedical_concepts_in_category:list[USDM_BC]
    all_biomedical_concepts:list[USDM_BC]
    selected_biomedical_concept:USDM_BC
    biomedical_concepts_in_selection:list[USDM_BC]

    current_repository:list[USDM_BC] = None

    # __app:"App"

    # @staticmethod
    # def get_instance():
    #     '''return a unique static instance of the App class'''
    #     if App.__app is None:
    #         App.__app = App()
    #     return App.__app

    def select_category(self, category_list_index:int):
        print("[App]: select_category has been called")
        selected_category:USDM_Category = self.categories[category_list_index]

        # TODO: Get All known bcs in category from disc
        temp = API.get_biomedical_concepts_list(selected_category.code.standard_code.code, categories=[cat.code.standard_code.code for cat in self.categories])
        available_bcs:list[USDM_BC] = [USDM_BC(row) for row in temp]

        self.biomedical_concepts_in_category = available_bcs

        return {
            "category_name":selected_category.label,
            "bc_names": [bc.label for bc in available_bcs]}


        # TODO: Update Selected category Label
        # TODO: Get all list of bcs from api
        # TODO: Update biomedical_concepts_in_category
        # TODO: Update UI with new list

    def get_bcs_in_category(self, category):
        self.biomedical_concepts_in_category = [USDM_BC(bc) for bc in API.get_biomedical_concepts_list(category.get_code())]
        return self.biomedical_concepts_in_category

    def __init__(self):
        self.biomedical_concepts_in_selection = None
        t = BC2USDM_Window(app=self, screenName = App.__APPLICATION_TITLE__)
        # last call during runtime
        # user_ui = UIDisplay(self, App.__APPLICATION_TITLE__, category_names=[cat.label for cat in self.categories])
        # self.display = user_ui
        # calls in init after this line are probably ran after closing the UI

    def __call__(self, *args, **kwds):
        app:App = App()

    def get_repository(self):
        '''return selected USDM BCs'''
        if self.current_repository is None:
            self.current_repository = []
            # Appending a list of bcs, since the repo might have multiple lists of bcs
            self.current_repository.append(self.get_bcs_in_category("AIMS"))
            for bc in self.current_repository[0]:
                bc.populate()
        return self.current_repository

    def get_biomedical_concept_names_in_category(self, index:int = None, id_:str = None, name:str = None):
        ''' Set bc_selection to all biomedical concepts in provided category and returns a list of the related names
        Raises a ValueError if no index, id or name is provided
        Returns list[str] names
        '''
        print(f"[APP] requesting bc names ")
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
        self.current_bcs: list[USDM_BC] = self.get_bcs_in_category(current_category)
        return self.current_bcs

    def select_bc(self, index:int):
        if len(self.biomedical_concepts_in_category) > 0:
            selected_bc = self.biomedical_concepts_in_category[index]
            if self.biomedical_concepts_in_selection is None:
                self.biomedical_concepts_in_selection:list[USDM_BC] = []
            self.biomedical_concepts_in_selection.append(selected_bc)
            return selected_bc
        else:
            return None
        
    def get_category_labels(self):
        json_categories = API.get_latest_biomedical_concept_categories()
        usdm_categories:list[USDM_Category] = list(map(USDM_Category.from_json, json_categories))

        # sort categories by name
        usdm_categories.sort(key=lambda usdm_category: usdm_category.name)
        self.categories = usdm_categories
        return [category.label for category in self.categories]

# App autostart
def main(*args):
    app:App = App()

if __name__ == "__main__":
    main()
