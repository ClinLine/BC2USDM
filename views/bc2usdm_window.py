from tkinter import *
# from tkinter import ttk

# from props_testing import PropertyDisplay

# from props_testing import Properties_Container
# from uuid import uuid4 as guid

from views.categories_view import CategoriesView
from views.current_biomedical_concept_view import CurrentBiomedicalConceptView
from views.current_category_view import CurrentCategoryView
from views.menu import MenuBar
from views.repository.repository_view import RepositoryView



# from main import App as instance

# from functools import lru_cache



# TODO refactor main UI into:
    # - MainDisplay
    #    + MenuBar
    #    + FooterBar (Progress Bar)
    #    + Categories Container
    #       o Labeled Entrybox + btn => Search box
    #       o Listbox with all categories
    #    + Current Category container
    #       o Labeled Entry box + btn => Search box
    #       o Listbox with all BCs in current category
    #    + Current Biomedical Concept container
    #       o General info container
    #       o Properties Container
    #       o Reset to default btn
    #       o Submit to repository btn
    #    + Current Repository Container
    #       o Added categories container
    #          * Search box (labeled entry box + go btn)
    #          * Listbox
    #       o Added Biomedical Concepts Container
    #          * Search box (labeled entry box + go btn)
    #          * Listbox
    #       o defined Procedures TODO
    #          * tbd

class BC2USDM_Window():
    
    __default_height: int = 600
    __data_columns: int = 5
    __data_column_width = [300,300,600,300]
    __default_width: int = sum(__data_column_width)
    __data_column_height = __default_height
    
    main_app:"App" = None
    menubar:MenuBar

    def __init__(self, app:type["App"], *args, **kwargs):
        self.main_app = app
        self.root = Tk() # TK
        self.root.config(
            width=self.__default_width,
            height=self.__default_height)
        self.root.title(kwargs["screenName"])
        
        # Config window
        
        # Add Menubar
        self.root.option_add("*tearOff", FALSE)
        self.menubar = MenuBar(self.root, app=self.main_app)
        self.root.config(menu=self.menubar)

        # Instantiate containers:
        self.categories_container = CategoriesView(self, width=self.__data_column_width[0])
        self.current_category_container = CurrentCategoryView(self, width=self.__data_column_width[1], x=self.__data_column_width[0])
        self.current_bc_container = CurrentBiomedicalConceptView(self, width=self.__data_column_width[2], x=self.__data_column_width[1]+self.__data_column_width[0])
        self.current_repository_container = RepositoryView(self, width=self.__data_column_width[3], x=self.__default_width-self.__data_column_width[3])
        self.root.mainloop()

    def update_current_bc(self, bc):
        # Set current bc in main app
        self.main_app.set_current_bc(bc)
        self.current_bc_container.update_view(bc)
        

    def update_categories(self, categories):
        names = [cat.name for cat in categories]
        self.categories_container.set_categories(names)

    def set_current_category(self, index:int):
        self.main_app.set_current_category_by_index(index)
        
        cat_label = self.main_app.get_current_category_label()
        bc_names = self.main_app.get_biomedical_concept_names_in_current_category()
        # bc_names = self.main_app.get_biomedical_concept_names_in_category(index=index)
        # now to display the
        self.current_category_container.update_current_category(cat_label, bc_names)

    def apply_to_repository(self, bc:dict):
        biomedical_concepts_in_repository = self.main_app.apply_to_repository(bc)
        categories_in_repository = self.main_app.get_categories_in_repository()
        self.current_repository_container.update_bc_list(biomedical_concepts_in_repository)
        self.current_repository_container.update_cat_list(categories_in_repository)