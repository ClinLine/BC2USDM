from tkinter import *
from tkinter import ttk

# from props_testing import PropertyDisplay

# from props_testing import Properties_Container
# from uuid import uuid4 as guid

from views.property_ui import Properties_Container
from views.menu import MenuBar



# from main import App as instance

# from functools import lru_cache

CATEGORY_LISTBOX_NAME = "category-listbox"

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
    __data_columns: int = 4
    __data_column_width = [200,300,300,200]
    __default_width: int = sum(__data_column_width)
    __data_column_height = __default_height
    
    main_app:type["App"] = None
    menubar:MenuBar

    def __init__(self, app:type["App"], *args, **kwargs):
        self.main_app = app
        self.root = Tk() # TK
        self.root.title(kwargs["screenName"])
        
        # Config window
        
        # Add Menubar
        self.root.option_add("*tearOff", FALSE)
        self.menubar = MenuBar(self.root, app=self.main_app)
        self.root.config(menu=self.menubar)

        # Instantiate containers:        
        self.categories_container = CategoriesView(self, width=self.__data_column_width[0])
        self.current_category_container = CurrentCategoryView(self)
        self.current_bc_container = CurrentBiomedicalConceptView(self, width=self.__data_column_width[1], x=self.__data_column_width[0])
        self.root.mainloop()

    def update_categories(self, categories):
        names = [cat.name for cat in categories]
        self.categories_container.set_categories(names)

    def set_current_category(self, index:int):
        bc_names = self.main_app.get_biomedical_concept_names_in_category(index)
        self.current_category_container.set_current_category(bc_names)

class CategoriesView(LabelFrame):
    category_names:StringVar
    categories_overview_frame:ttk.LabelFrame
    TITLE_TEXT = "Biomedical Categories:"
    categories_label:ttk.Label
    categories_overview_listbox:Listbox
    categories_overview_scrollbarX:Scrollbar
    categories_overview_scrollbarY:Scrollbar
    
    def set_categories(self, names:list[str]):
        self.category_names.set(names)

    def get_categories(self):
        return self.category_names.get()
    
    def get_selection(self):
        """
        Returns the selection of this container's listbox

        :return default:Literal[()]: Returns an empty tuple '()' if selection is empty.
        :return value:tuple[int]: Returns a tuple of type int containing the indices of the selected items. <br>
        The returned tuple has a length of 1 if the listbox's selectmode is set to browse or signle.
        """
        select_mode = self.categories_overview_listbox.__getattribute__("selectMode")
        
        self.categories_overview_listbox.curselection()

    def __init__(self, parent, width, **kwargs):
        self.parent = parent
        if "title" in kwargs.keys():
            title = kwargs["title"]
        else:
            title = CategoriesView.TITLE_TEXT
        super().__init__(parent.root, text=title, **kwargs)
        
        # self.categories_overview_frame = ttk.LabelFrame(parent,text=f"BC Categories:")
        # self.categories_overview_frame.place(anchor="nw", relheight=1, width=UIDisplay.__data_column_width[0], in_=parent)

        self.place(anchor="nw", relheight=1, width=width)
        # Update this var's value to update category list
        self.category_names = StringVar(value=["item 1","item 1","item 1","item 1","item 1","item 1"]) 
        self.categories_overview_listbox = Listbox(self, listvariable=self.category_names, name=CATEGORY_LISTBOX_NAME, selectmode=BROWSE)
        self.categories_overview_scrollbarX = Scrollbar(self, orient=HORIZONTAL)
        self.categories_overview_scrollbarY = Scrollbar(self, orient=VERTICAL)
        self.categories_overview_listbox.configure(yscrollcommand=self.categories_overview_scrollbarY.set)
        self.categories_overview_listbox.configure(xscrollcommand=self.categories_overview_scrollbarX.set)
        self.categories_overview_listbox.bind("<<ListboxSelect>>", self._bind_category_listbox)
       
        self.categories_overview_scrollbarX.config(command=self.categories_overview_listbox.xview)
        self.categories_overview_scrollbarX.pack(side=BOTTOM, fill=X, in_=self)
        self.categories_overview_scrollbarY.config(command=self.categories_overview_listbox.yview)
        self.categories_overview_scrollbarY.pack(side=RIGHT, fill=Y, in_=self)

        # TODO: calc height based on window size
        self.categories_overview_listbox.pack(anchor="nw",expand=True,side="left",fill="both")
        self._init_categories()

    def _init_categories(self):
        names = self.parent.main_app.get_category_labels()
        self.category_names.set(names)

    def _bind_category_listbox(self, event, **kwargs):
        self._listbox_onclick(event, **kwargs)

    def _listbox_onclick(self, event, **kwargs):
        selection = event.widget.curselection() # default = ()
        print(f"listbox entry {selection} has been clicked")
        if selection == ():
            return
        # return [self.parent.main_app.get_biomedical_concept_names_in_category(index) for index in selection][0]
        # return self.parent.main_app.get_biomedical_concept_names_in_category(selection[0])
        self.parent.set_current_category(selection[0])



class CurrentCategoryView(LabelFrame):
    svarname:StringVar
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent.root, **kwargs)
        ...

    def set_current_category(self, names:list[str]):
        self.svarname.set(names)

class CurrentBiomedicalConceptView(LabelFrame):
    def __init__(self, parent,  width, x, title:str = None, **kwargs):
        
        super().__init__(parent.root, text=title, **kwargs)
        self.biomedical_concepts_in_category=StringVar()

        if title == "" or title is None:
            title = f"BCs in Category:"

        self.active_category_overview_lframe = ttk.LabelFrame(self,text=title)
        self.place(anchor="nw", relheight=1, width=width, x=x)
        self.active_category_overview_listbox = Listbox(self, listvariable=self.biomedical_concepts_in_category, name="activeCat-listbox")
        self.active_category_overview_scrollbarX = Scrollbar(self, orient=HORIZONTAL)
        self.active_category_overview_scrollbarX.config(command=self.active_category_overview_listbox.xview)
        self.active_category_overview_listbox.configure(xscrollcommand=self.active_category_overview_scrollbarX.set)
        self.active_category_overview_scrollbarY = Scrollbar(self, orient=VERTICAL)
        self.active_category_overview_scrollbarY.config(command=self.active_category_overview_listbox.yview)
        self.active_category_overview_listbox.configure(yscrollcommand=self.active_category_overview_scrollbarY.set)
        self.active_category_overview_listbox.bind("<<ListboxSelect>>", self.bind_active_bc_listbox)
        

        self.active_category_overview_scrollbarX.pack(side=BOTTOM,fill=X,in_=self)
        self.active_category_overview_scrollbarY.pack(side=RIGHT,fill=Y,in_=self)
        self.active_category_overview_listbox.pack(anchor="nw",expand=True,side="left",fill="both")

    def bind_active_bc_listbox(self, event, **kwargs):
        self.listbox_onclick(event, **kwargs)

    def listbox_onclick(self, event, **kwargs):
        print(event.widget.curselection())

class RepositoryView(LabelFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent.root, **kwargs)
        ...

class ProcedureView:
    def __init__(self, **kwargs):
        raise NotImplementedError("Procedure View isn't implemented yet.")

class UIDisplay():
    __default_height: int = 600
    __data_columns: int = 4
    __data_column_width = [200,300,300,200]
    __default_width: int = sum(__data_column_width)
    __data_column_height = __default_height
    # __instance: type["UIDisplay"]
    root:Tk

    __main_app:type["App"]

    mainframe:ttk.Frame

    # Categories Overview
    

    # Biomedical Concept Overview
    selected_biomedical_concepts:StringVar
    selection_frame:ttk.Frame
    selection_label:ttk.Label
    selection_listbox:Listbox
    selection_listbox_scrollbarX:Scrollbar
    selection_listbox_scrollbarY:Scrollbar


    def __init__(self, app_instance: type["App"], title, category_names:list[str],bc_names=None):
        self.__main_app = app_instance
        if bc_names is None:
            bc_names = ["testName"]
        self.setup_ui(title, app_instance)
        # self.category_names.set(category_names)

        self.root.mainloop()
       
    def setup_ui(self, app_title:str, app_instance):
        self.root = Tk()
        self.root.title(app_title)
        self.root.config(height=UIDisplay.__default_height,width=UIDisplay.__default_width)
        self.root.geometry(f"{UIDisplay.__default_width}x{UIDisplay.__default_height}+0+0")
        
       

        # Move the window to the screen left from the primary monitor
        self.root.update_idletasks() # force geometry calc, otherwise all values will be 0
        # PropertyDisplay(testWindow, "PropertyTesting!!")

        self.mainframe:ttk.Frame = ttk.Frame(self.root, padding = "3 3 12 12")
        self.mainframe.config(height=UIDisplay.__default_height,width=UIDisplay.__default_width)
        self.mainframe.pack(fill="both",side="top", expand=True)
        
        # Categories Overview

        # Init Categories overview:

        

        
        # Biomedical Concept Overview

        
       
        # Frame for active biomedical Concept
        # Dummy active biomedical Concept Frame
        self.active_biomedical_concept_overview_lframe = ttk.LabelFrame(self.mainframe,text="Active BC:")
        self.active_biomedical_concept_overview_lframe.place(anchor="nw", relheight=1, width=UIDisplay.__data_column_width[2],x=UIDisplay.__data_column_width[0]+UIDisplay.__data_column_width[1], in_=self.mainframe)
        self.active_biomedical_concept_overview_mainframe = ttk.Frame(self.active_biomedical_concept_overview_lframe)
        self.active_biomedical_concept_overview_mainframe.pack(anchor="nw",fill="x",expand=False)
        
        
        master_frame = self.active_biomedical_concept_overview_mainframe
        
        self.bc_name_label = Label(master_frame, text="Name: ")
        self.bc_name_label.grid(row=0,column=0,sticky="W",in_=master_frame)
        self.bc_name_value = StringVar(value="Dummy BC")
        self.bc_name_entry = Entry(master_frame, textvariable=self.bc_name_value)
        self.bc_name_entry.grid(row=0,column=1,sticky="WE",in_=master_frame,padx=1)
        master_frame.columnconfigure(1,weight=1)
        

        # label_label:Label         label:Textbox
        # ID_Label:Label            ID:Disabled_Text
        self.bc_id_label = Label(master_frame,text="Id: ")
        self.bc_id_value = StringVar(value="C60354")
        self.bc_id_label.grid(row=1,column=0,sticky="W", in_=master_frame)
        self.bc_id_entry = Entry(master_frame,textvariable=self.bc_id_value)
        self.bc_id_entry.configure(state=DISABLED)
        self.bc_id_entry.grid(row=1,column=1, sticky="WE", in_=master_frame,padx=1)
        
        # reference_label:Label     url:Disabled_Text
        self.bc_reference_value = StringVar(value="/mdr/bc/biomedicalconcepts/C445997")
        self.bc_reference_label = Label(master_frame, text="Reference: ")
        self.bc_reference_label.grid(row=2,column=0,sticky="W", in_=master_frame)
        self.bc_reference_entry = Entry(master_frame,textvariable=self.bc_reference_value)
        self.bc_reference_entry.configure(state=DISABLED)
        self.bc_reference_entry.grid(row=2,column=1, sticky="WE", in_=master_frame,padx=1)

        # code_label:Label          code:Disabled_Text
        self.bc_alias_code_value = StringVar(value="C445997")
        self.bc_alias_code_label = Label(master_frame, text="AliasCode: ")
        self.bc_alias_code_label.grid(row=3,column=0,sticky="W", in_=master_frame)
        self.bc_alias_code_entry = Entry(master_frame,textvariable=self.bc_alias_code_value)
        self.bc_alias_code_entry.configure(state=DISABLED)
        self.bc_alias_code_entry.grid(row=3,column=1, sticky="WE", in_=master_frame,padx=1)
        # synonyms:Label            synonyms:Lisbox
        self.bc_synonyms_frame = Frame(master_frame)
        self.bc_synonyms_frame.grid(row=3, column=1,sticky="WE",padx=1)
        self.dummy_synonyms = ["David","Goliath","Synonym 3",]
        self.bc_synonyms_value = StringVar(value=self.dummy_synonyms)
        self.bc_synonyms_label = Label(master_frame, text="Synonyms: ")
        self.bc_synonyms_label.grid(row=3,column=0,sticky="W", in_=master_frame)
        self.bc_synonyms_listbox = Listbox(self.bc_synonyms_frame,listvariable=self.bc_synonyms_value)
        self.bc_synonyms_yscrollbar = Scrollbar(self.bc_synonyms_frame,orient=VERTICAL,command=self.bc_synonyms_listbox.yview)
        self.bc_synonyms_yscrollbar.pack(anchor="ne",fill="y",side="right")
        self.bc_synonyms_listbox.configure(yscrollcommand=self.bc_synonyms_yscrollbar.set)
        if len(self.dummy_synonyms) < 6:
            lbl_height = len(self.dummy_synonyms)
            self.bc_synonyms_yscrollbar.config(width=-1)
        else:
            lbl_height = 5
            self.bc_synonyms_yscrollbar.config(width=12)
        self.bc_synonyms_listbox.config(height=lbl_height)
        self.bc_synonyms_listbox.pack(anchor="nw",fill="both", expand=True, side="left")
        #                           new_synonym:Entry   add_Button:Button
        self.bc_synonyms_entry_frame = Frame(master_frame)
        self.bc_synonyms_entry_frame.grid(row=5,column=1,sticky="EW")
        self.bc_synonyms_entry_value = StringVar()
        self.bc_synonyms_entry = Entry(self.bc_synonyms_entry_frame,textvariable=self.bc_synonyms_entry_value)
        self.bc_synonyms_entry.pack(anchor="w",side="left",fill="x",expand=True)
        self.bc_synonyms_entry_button = Button(self.bc_synonyms_entry_frame,text="add", command=lambda:self.synonym_add_cmd(self.bc_synonyms_entry.get()))
        self.bc_synonyms_entry_button.pack(anchor="w", fill="none",side="right",before=self.bc_synonyms_entry)

        self.bc_synonyms_entry.bind("<Return>", lambda event: self.synonym_add_cmd(self.bc_synonyms_entry.get()))
        # dummy_properties = [{
        #     "id_":str(guid()).upper(),
        #     "label":"Testing Prop",
        #     "isRequired":1,
        #     "isEnabled":0,
        #     "dataType":"Blood sample",
        #     "code":"C2389",
        #     "notes":["beep boop","Bla bla\n bla", "Bla bla \n akj;sdf a;klsdjf ;akdjfa;leksjfa;kldjf;a kljsef;alksejf;aklsjef;aksjfj a;ske;fjkasd;fjk asej;fkasjf;lkasej;fkl asjef;k lasefj a;kslefj asklef ja;skejfa;klsfj a;selkj ;fjkasd;fjk asej;fkasjf;lkasej;fkl asjef;k lasefj a;kslefj asklef ja;skejfa;klsfj a;selkj f", "this is super important too"],
        #     "responseCode":[{
        #         "id":str(guid()).upper(),
        #         "name":"Blood letting",
        #         "label":"Blood letting2",
        #         "isEnabled":1,
        #         "code":"C651654",
        #     },{
        #         "id":str(guid()).upper(),
        #         "name":"Blood letting",
        #         "label":"Blood letting2",
        #         "isEnabled":0,
        #         "code":"C651654",
        #     },],
        # },
        # {
        #     "id_":str(guid()).upper(),
        #     "label":"Testing Prop 2",
        #     "isRequired":1,
        #     "isEnabled":0,
        #     "dataType":"Bs",
        #     "code":"C651549",
        #     "notes":["Bla bla bla", "This is a crutial note", "this is super important too"],
        #     "responseCode":[{
        #         "id":str(guid()).upper(),
        #         "name":"Blood letting",
        #         "label":"Blood letting2",
        #         "isEnabled":1,
        #         "code":"C65154",
        #     }],
        # },{
        #     "id_":str(guid()).upper(),
        #     "label":"Testing Prop",
        #     "isRequired":0,
        #     "isEnabled":1,
        #     "dataType":"Blood sample",
        #     "code":"C64165",
        #     "notes":["Bla bla bla", ],
        #     "responseCode":[{
        #         "id":str(guid()).upper(),
        #         "name":"Blood letting",
        #         "label":"Blood letting2",
        #         "isEnabled":1,
        #         "code":"C65416541",
        #     }],
        # }]
        self.properties_frame = Properties_Container(self.active_biomedical_concept_overview_lframe,frame_title="Properties:", properties=None)
        self.properties_frame.pack(side=TOP, fill=BOTH, expand=True)


    def synonym_add_cmd(self, *args):
        self.dummy_synonyms.append(args[0])
        self.bc_synonyms_value.set(self.dummy_synonyms)
        label_height = 0
        if len(self.dummy_synonyms) < 6:
            label_height = len(self.dummy_synonyms)
            self.bc_synonyms_yscrollbar.config(width=-1)
        else:
            label_height = 5
            self.bc_synonyms_yscrollbar.config(width=12)

        self.bc_synonyms_listbox.config(height=label_height)
        self.bc_synonyms_entry_value.set("")


    # Functions:
    def _bind_category_onclick(self, event, *args, **kwargs):
        # print(event.widget.__dict__)
        # self.on_category_click(event.widget.curselection()[0])
        self.on_category_click(event)

    def on_category_click(self, event):
        print(self.root.focus_get())
        if event.widget._name != CATEGORY_LISTBOX_NAME:
            return
        
        try:

            indices = event.widget.curselection()
            if len(indices) == 1:
                indices = indices[0]
            elif len(indices) == 0:
                return
            result = self.__main_app.select_category(int(indices))
            self.set_active_category(result["category_name"],result["bc_names"])
        except ValueError:
            print(ValueError)
        else:
            event.widget.focus_

    def set_active_category(self, category_name:str, bc_names:list[str]):
        self.active_category_overview_lframe.configure(text=f"{category_name}")
        self.biomedical_concepts_in_category.set(bc_names)

    def bind_active_bc_onclick(self, event, *args, **kwargs):
        # print(event.__dict__)
        print(event.widget.__dict__)
        indices = event.widget.curselection()
        print(f"selection index: {indices}")

        try:
            if len(indices) == 1:
                indices = indices[0]
            bc = self.__main_app.select_bc(indices)
            self.populate_active_bc_overview(bc)
        except ValueError:
            pass
    
    def populate_active_bc_overview(self, bc, **kwargs):
        self.active_biomedical_concept_overview_lframe["text"] = bc.label

    # def on_biomedical_concept_click(self, event, *args):
    #         try:
    #             value = current_bcs[Listbox.curselection(bcs_in_current_category)[0]]
    #         except ValueError:
    #             pass
