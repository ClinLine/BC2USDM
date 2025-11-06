
# from props_testing import PropertyDisplay
from views.ui_display import UIDisplay
from models.CDISC.BiomedicalConceptCategory import BiomedicalConceptCategory as CDISC_Category
from models.USDM.BiomedicalConceptCategory import BiomedicalConceptCategory as USDM_Category
from models.USDM.BiomedicalConcept import BiomedicalConcept as USDM_BC
# from utils.api_utils import get_biomedical_concepts_list, get_latest_biomedical_concept_categories
from utils import api_utils as API
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

    current_repository = list[USDM_BC]

    # __app:"App"

    @staticmethod
    def get_instance():
        '''return a unique static instance of the App class'''
        if App.__app is None:
            App.__app = App()
        return App.__app

    def select_category(self, category_list_index:int):
        
        selected_category:USDM_Category = self.categories[category_list_index]
        
        # TODO: Get All known bcs in category from disc
        # TODO: Create From Dict for list of usdm bcs
        # available_bcs:list[USDM_BC] = USDM_BC.from_dict(get_biomedical_concepts_list(selected_category.id_))
        temp = API.get_biomedical_concepts_list(selected_category.id_, categories=[cat.id_ for cat in self.categories])
        available_bcs:list[USDM_BC] = [USDM_BC(row) for row in temp]
        
        self.biomedical_concepts_in_category = available_bcs
        
        return {
            "category_name":selected_category.label,
            "bc_names": [bc.label for bc in available_bcs]}
        # self.user_ui.update_bcs_in_category_list(selected_category.name, [bc.name for bc in available_bcs])


        # TODO: Update Selected category Label
        # TODO: Get all list of bcs from api
        # TODO: Update biomedical_concepts_in_category
        # TODO: Update UI with new list

    def get_bcs_in_category(self, category:str):
        self.biomedical_concepts_in_category = API.get_biomedical_concepts_list(category)
        return self.biomedical_concepts_in_category
    

    def __new__(cls):
        # Ensure singleton
        if not hasattr(cls, 'instance'):
            cls.instance = super(App, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        
        json_categories = API.get_latest_biomedical_concept_categories()

        # cdisc_categories:list[CDISC_Category] = CDISC_Category.categories_from_json(json_categories)
        usdm_categories:list[USDM_Category] = list(map(USDM_Category.from_json, json_categories))

        # sort categories by name
        usdm_categories.sort(key=lambda usdm_category: usdm_category.name)
        self.categories = usdm_categories
        
        user_ui = UIDisplay(self, App.__APPLICATION_TITLE__, category_names=[cat.label for cat in self.categories])
        
        # user_ui = PropertyDisplay(self, App.__APPLICATION_TITLE__)
        # user_ui.set_cagetories(self.categories)

        self.display = user_ui
        # TODO load from disk

        # user_ui.set_categories([category.name for category in usdm_categories])

        # selection:list[USDM_Category] = []
        
        # user_ui.create_selection_list("Selected Biomedical Concepts:")

        # Biomedical Concepts List
        # TODO: Function > bc category on select
        # TODO: Add label displaying currently selected category name
        # TODO: Add listbox with all BCs in current category
        #   - Check if the BCs are already available
        #       True => Display BC list
        #       False => Fetch, store & display BC list
        # TODO: Add category to listbox when BC is selected
        # TODO: Add bc to listbox when BC is selected

    def __call__(self, *args, **kwds):
        app:App = App()

    @staticmethod
    def get_repository():
        '''return selected USDM BCs'''
        app = App.get_instance()
        if app.current_repository is None:
            print(f"{(app.current_repository)} isn't implemented yet, using demo values instead")
            app.current_repository = [USDM_BC(app.biomedical_concepts_in_category('AIMS'))]
        return app.current_repository


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

        for category in self.categories:
            if category.id_ == id_ or category.name == name:
                current_category = category
                break
        self.current_bcs: list[USDM_BC] = self.get_bcs_in_category(current_category)
        return self.current_bcs
    
    def select_bc(self, index:int):
        selected_bc = self.biomedical_concepts_in_category[index]
        self.biomedical_concepts_in_selection.append(selected_bc)
        return selected_bc.name



def main(*args):
    app:App = App()
    # app.start()

if __name__ == "__main__":
    main()
    