from tkinter import *
from tkinter import ttk

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
    
    main_app:type["App"] = None
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
        self.current_repository_container.update_bc_list(biomedical_concepts_in_repository)


        



# class UIDisplay():
#     __default_height: int = 600
#     __data_columns: int = 4
#     __data_column_width = [200,300,300,200]
#     __default_width: int = sum(__data_column_width)
#     __data_column_height = __default_height
#     # __instance: type["UIDisplay"]
#     root:Tk

#     __main_app:type["App"]

#     mainframe:ttk.Frame

#     # Categories Overview
    

#     # Biomedical Concept Overview
#     selected_biomedical_concepts:StringVar
#     selection_frame:ttk.Frame
#     selection_label:ttk.Label
#     selection_listbox:Listbox
#     selection_listbox_scrollbarX:Scrollbar
#     selection_listbox_scrollbarY:Scrollbar


#     def __init__(self, app_instance: type["App"], title, category_names:list[str],bc_names=None):
#         self.__main_app = app_instance
#         if bc_names is None:
#             bc_names = ["testName"]
#         self.setup_ui(title, app_instance)
#         # self.category_names.set(category_names)

#         self.root.mainloop()
       
#     def setup_ui(self, app_title:str, app_instance):
#         self.root = Tk()
#         self.root.title(app_title)
#         self.root.config(height=UIDisplay.__default_height,width=UIDisplay.__default_width)
#         self.root.geometry(f"{UIDisplay.__default_width}x{UIDisplay.__default_height}+0+0")
        
       

#         # # Move the window to the screen left from the primary monitor
#         # self.root.update_idletasks() # force geometry calc, otherwise all values will be 0
#         # # PropertyDisplay(testWindow, "PropertyTesting!!")

#         # self.mainframe:ttk.Frame = ttk.Frame(self.root, padding = "3 3 12 12")
#         # self.mainframe.config(height=UIDisplay.__default_height,width=UIDisplay.__default_width)
#         # self.mainframe.pack(fill="both",side="top", expand=True)
        
#         # Categories Overview

#         # Init Categories overview:

        

        
#         # Biomedical Concept Overview

        
       
#         # Frame for active biomedical Concept
#         # Dummy active biomedical Concept Frame
        

#     # Functions:
#     # def _bind_category_onclick(self, event, *args, **kwargs):
#     #     print(event.widget.__dict__)
#     #     # self.on_category_click(event.widget.curselection()[0])
#     #     # self.on_category_click(event)

#     # def on_category_click(self, event):
#     #     print(self.root.focus_get())
#     #     if event.widget._name != CATEGORY_LISTBOX_NAME:
#     #         return
#     #     try:
#     #         indices = event.widget.curselection()
#     #         if len(indices) == 1:
#     #             indices = indices[0]
#     #         elif len(indices) == 0:
#     #             return
#     #         result = self.__main_app.select_category(int(indices))
#     #         self.set_active_category(result["category_name"],result["bc_names"])
#     #     except ValueError:
#     #         print(ValueError)
#     #     else:
#     #         event.widget.focus_

#     # def set_active_category(self, category_name:str, bc_names:list[str]):
#     #     print("test")
#     # #     self.active_category_overview_lframe.configure(text=f"{category_name}")
#     # #     self.biomedical_concepts_in_category.set(bc_names)

#     # def bind_active_bc_onclick(self, event, *args, **kwargs):
#     #     # print(event.__dict__)
#     #     print(event.widget.__dict__)
#     #     indices = event.widget.curselection()
#     #     print(f"selection index: {indices}")

#     #     try:
#     #         if len(indices) == 1:
#     #             indices = indices[0]
#     #         bc = self.__main_app.select_bc(indices)
#     #         self.populate_active_bc_overview(bc)
#     #     except ValueError:
#     #         pass
    
#     # def populate_active_bc_overview(self, bc, **kwargs):
#     #     self.config(text=bc.label)

#     # def on_biomedical_concept_click(self, event, *args):
#     #         try:
#     #             value = current_bcs[Listbox.curselection(bcs_in_current_category)[0]]
#     #         except ValueError:
#     #             pass