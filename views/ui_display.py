from tkinter import *
from tkinter import ttk

# from props_testing import PropertyDisplay

# from props_testing import Properties_Container
from uuid import uuid4 as guid

from views.property_ui import Properties_Container
from views.menu import MenuBar



# from main import App as instance

# from functools import lru_cache



# @lru_cache(maxsize=1)
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
    category_names:StringVar
    categories_overview_frame:ttk.LabelFrame
    CATEGORIES_LABEL_TEXT = "Biomedical Categories:"
    categories_label:ttk.Label
    categories_overview_listbox:Listbox
    categories_overview_scrollbarX:Scrollbar
    categories_overview_scrollbarY:Scrollbar

    # Biomedical Concept Overview
    selected_biomedical_concepts:StringVar
    selection_frame:ttk.Frame
    selection_label:ttk.Label
    selection_listbox:Listbox
    selection_listbox_scrollbarX:Scrollbar
    selection_listbox_scrollbarY:Scrollbar



    def __init__(self, app_instance: type["App"], title, category_names:list[str],bc_names=None):
        # super().__init__(master)
        # self.app_instance = app
        self.__main_app = app_instance
        if bc_names is None:
            bc_names = ["testName"]
        self.setup_ui(title, app_instance)
        self.category_names.set(category_names)
        # self.root.pack()

        self.root.mainloop()
       
    def setup_ui(self, app_title:str, app_instance):
        self.root = Tk()
        self.root.title(app_title)
        self.root.config(height=UIDisplay.__default_height,width=UIDisplay.__default_width)
        self.root.geometry(f"{UIDisplay.__default_width}x{UIDisplay.__default_height}")
        
        self.root.option_add("*tearOff", FALSE)
        self.menubar = MenuBar(self.root, app_instance)
        self.root["menu"] = self.menubar
        # testWindow = Toplevel(self.root)
        
        # Move the window to the screen left from the primary monitor
        self.root.update_idletasks() # force geometry calc, otherwise all values will be 0
        # testWindow.geometry(f"+{testWindow.winfo_rootx()-testWindow.winfo_screenwidth()}+{testWindow.winfo_rooty()}")
        # PropertyDisplay(testWindow, "PropertyTesting!!")
        # self.root["bg"]="red"
        # self.root.minsize(UIDisplay.__default_width,UIDisplay.__default_height)

        self.mainframe:ttk.Frame = ttk.Frame(self.root, padding = "3 3 12 12")
        self.mainframe.config(height=UIDisplay.__default_height,width=UIDisplay.__default_width)
        self.mainframe.pack(fill="both",side="top", expand=True)
        # self.mainframe = mainframe
        # self.mainframe["fg"]="green"
        # print(f"mainframe width:{self.mainframe.winfo_width()}")
        # Categories Overview

        # Init Categories overview:
        self.categories_overview_frame = ttk.LabelFrame(self.mainframe,text=f"BC Categories:")
        self.categories_overview_frame.place(anchor="nw", relheight=1, width=UIDisplay.__data_column_width[0], in_=self.mainframe)
        

        self.category_names = StringVar()
        self.categories_overview_listbox = Listbox(self.categories_overview_frame, listvariable=self.category_names)
        self.categories_overview_scrollbarX = Scrollbar(self.categories_overview_frame, orient=HORIZONTAL)
        self.categories_overview_scrollbarY = Scrollbar(self.categories_overview_frame, orient=VERTICAL)
        self.categories_overview_listbox.configure(yscrollcommand=self.categories_overview_scrollbarY.set)
        self.categories_overview_listbox.configure(xscrollcommand=self.categories_overview_scrollbarX.set)
        self.categories_overview_listbox.bind("<<ListboxSelect>>", self._on_category_select)
       
        self.categories_overview_scrollbarX.config(command=self.categories_overview_listbox.xview)
        self.categories_overview_scrollbarX.pack(side=BOTTOM, fill=X, in_=self.categories_overview_frame)
        self.categories_overview_scrollbarY.config(command=self.categories_overview_listbox.yview)
        self.categories_overview_scrollbarY.pack(side=RIGHT, fill=Y, in_=self.categories_overview_frame)

        
        # TODO: calc height based on window size
        self.categories_overview_listbox.pack(anchor="nw",expand=True,side="left",fill="both")
        # Biomedical Concept Overview

        self.biomedical_concepts_in_category=StringVar()
        self.active_category_overview_lframe = ttk.LabelFrame(self.mainframe,text=f"BCs in Category:")
        self.active_category_overview_lframe.place(anchor="nw", relheight=1, width=UIDisplay.__data_column_width[1], x=UIDisplay.__data_column_width[0], in_=self.mainframe)
        self.active_category_overview_listbox = Listbox(self.active_category_overview_lframe, listvariable=self.biomedical_concepts_in_category)
        self.active_category_overview_scrollbarX = Scrollbar(self.active_category_overview_lframe, orient=HORIZONTAL)
        self.active_category_overview_scrollbarX.config(command=self.active_category_overview_listbox.xview)
        self.active_category_overview_listbox.configure(xscrollcommand=self.active_category_overview_scrollbarX.set)
        self.active_category_overview_scrollbarY = Scrollbar(self.active_category_overview_lframe, orient=VERTICAL)
        self.active_category_overview_scrollbarY.config(command=self.active_category_overview_listbox.yview)
        self.active_category_overview_listbox.configure(yscrollcommand=self.active_category_overview_scrollbarY.set)
        self.active_category_overview_listbox.bind("<<ListboxSelect>>", lambda onClick: self.on_active_bc_click(self.active_category_overview_listbox.curselection()[0]))
        

        self.active_category_overview_scrollbarX.pack(side=BOTTOM,fill=X,in_=self.active_category_overview_lframe)
        self.active_category_overview_scrollbarY.pack(side=RIGHT,fill=Y,in_=self.active_category_overview_lframe)
        self.active_category_overview_listbox.pack(anchor="nw",expand=True,side="left",fill="both")
       
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

        dummy_properties = [{
            "id_":str(guid()).upper(),
            "label":"Testing Prop",
            "isRequired":1,
            "isEnabled":0,
            "dataType":"Blood sample",
            "code":"C2389",
            "notes":["beep boop","Bla bla\n bla", "Bla bla \n akj;sdf a;klsdjf ;akdjfa;leksjfa;kldjf;a kljsef;alksejf;aklsjef;aksjfj a;ske;fjkasd;fjk asej;fkasjf;lkasej;fkl asjef;k lasefj a;kslefj asklef ja;skejfa;klsfj a;selkj ;fjkasd;fjk asej;fkasjf;lkasej;fkl asjef;k lasefj a;kslefj asklef ja;skejfa;klsfj a;selkj f", "this is super important too"],
            "responseCode":[{
                "id":str(guid()).upper(),
                "name":"Blood letting",
                "label":"Blood letting2",
                "isEnabled":1,
                "code":"C651654",
            },{
                "id":str(guid()).upper(),
                "name":"Blood letting",
                "label":"Blood letting2",
                "isEnabled":0,
                "code":"C651654",
            },],
        },
        {
            "id_":str(guid()).upper(),
            "label":"Testing Prop 2",
            "isRequired":1,
            "isEnabled":0,
            "dataType":"Bs",
            "code":"C651549",
            "notes":["Bla bla bla", "This is a crutial note", "this is super important too"],
            "responseCode":[{
                "id":str(guid()).upper(),
                "name":"Blood letting",
                "label":"Blood letting2",
                "isEnabled":1,
                "code":"C65154",
            }],
        },{
            "id_":str(guid()).upper(),
            "label":"Testing Prop",
            "isRequired":0,
            "isEnabled":1,
            "dataType":"Blood sample",
            "code":"C64165",
            "notes":["Bla bla bla", ],
            "responseCode":[{
                "id":str(guid()).upper(),
                "name":"Blood letting",
                "label":"Blood letting2",
                "isEnabled":1,
                "code":"C65416541",
            }],
        }]
        self.properties_frame = Properties_Container(self.active_biomedical_concept_overview_lframe,frame_title="Properties:", properties=dummy_properties)
        self.properties_frame.pack(side=TOP, fill=BOTH, expand=True)


    def _on_category_select(self, event, *args, **kwargs):
        self.on_category_click(event.widget.curselection()[0])

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

    def set_active_category(self, category_name:str, bc_names:list[str]):
        self.active_category_overview_lframe.configure(text=f"{category_name}")
        self.biomedical_concepts_in_category.set(bc_names)

    # Functions:
    def on_category_click(self, category_index):
        try:
            index = category_index

            result = self.__main_app.select_category(index)
            # result = self.__app_instance.select_category("age")
            self.set_active_category(result["category_name"],result["bc_names"])

        except ValueError:
            print(ValueError)

    def on_active_bc_click(self, *args):
        try:
            bc_selection_index = args[0]

            self.__main_app.select_bc(bc_selection_index)
        except ValueError:
            pass
    # def on_biomedical_concept_click(self,*args):
    #         try:
    #             value = current_bcs[Listbox.curselection(bcs_in_current_category)[0]]
    #         except ValueError:
    #             pass
