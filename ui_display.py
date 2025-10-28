from tkinter import *
from tkinter import ttk

from props_testing import PropertyDisplay



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

    __app_instance:"App"

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



    def __init__(self, app_instance: "App", title, category_names:list[str],bc_names=None):
        # super().__init__(master)
        # self.app_instance = app
        self.__app_instance = app_instance
        if bc_names is None:
            bc_names = ["testName"]
        self.setup_ui(title)
        self.category_names.set(category_names)
        # self.root.pack()

        self.root.mainloop()
       
    def setup_ui(self, app_title:str):
        self.root = Tk()
        self.root.title(app_title)
        self.root.config(height=UIDisplay.__default_height,width=UIDisplay.__default_width)
        self.root.geometry(f"{UIDisplay.__default_width}x{UIDisplay.__default_height}")
        
        testWindow = Toplevel(self.root)
        
        # Move the window to the screen left from the primary monitor
        self.root.update_idletasks() # force geometry calc, otherwise all values will be 0
        testWindow.geometry(f"+{testWindow.winfo_rootx()-testWindow.winfo_screenwidth()}+{testWindow.winfo_rooty()}")
        PropertyDisplay(testWindow, "PropertyTesting!!")
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
        self.categories_overview_listbox.bind("<<ListboxSelect>>",lambda onClick: self.on_category_click(self.categories_overview_listbox.curselection()[0]))
        
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
        self.active_biomedical_concept_overview_lframe = ttk.LabelFrame(self.mainframe,text=f"Active BC:")
        self.active_biomedical_concept_overview_lframe.place(anchor="nw", relheight=1, width=UIDisplay.__data_column_width[2],x=UIDisplay.__data_column_width[0]+UIDisplay.__data_column_width[1], in_=self.mainframe)
        self.active_biomedical_concept_overview_mainframe = ttk.Frame(self.active_biomedical_concept_overview_lframe)
        self.active_biomedical_concept_overview_mainframe.pack(anchor="nw",fill="x",expand=False)
        
        
        masterFrame = self.active_biomedical_concept_overview_mainframe
        
        self.bc_name_label = Label(masterFrame, text="Name: ")
        self.bc_name_label.grid(row=0,column=0,sticky="W",in_=masterFrame)
        self.bc_name_value = StringVar(value="Dummy BC")
        self.bc_name_entry = Entry(masterFrame, textvariable=self.bc_name_value)
        self.bc_name_entry.grid(row=0,column=1,sticky="WE",in_=masterFrame,padx=1)
        masterFrame.columnconfigure(1,weight=1)
        

        # label_label:Label         label:Textbox
        # ID_Label:Label            ID:Disabled_Text
        self.bc_id_label = Label(masterFrame,text="Id: ")
        self.bc_id_value = StringVar(value="C60354")
        self.bc_id_label.grid(row=1,column=0,sticky="W", in_=masterFrame)
        self.bc_id_entry = Entry(masterFrame,textvariable=self.bc_id_value)
        self.bc_id_entry.configure(state=DISABLED)
        self.bc_id_entry.grid(row=1,column=1, sticky="WE", in_=masterFrame,padx=1)
        
        # reference_label:Label     url:Disabled_Text
        self.bc_reference_value = StringVar(value="/mdr/bc/biomedicalconcepts/C445997")
        self.bc_reference_label = Label(masterFrame, text="Reference: ")
        self.bc_reference_label.grid(row=2,column=0,sticky="W", in_=masterFrame)
        self.bc_reference_entry = Entry(masterFrame,textvariable=self.bc_reference_value)
        self.bc_reference_entry.configure(state=DISABLED)
        self.bc_reference_entry.grid(row=2,column=1, sticky="WE", in_=masterFrame,padx=1)

        # code_label:Label          code:Disabled_Text
        self.bc_aliasCode_value = StringVar(value="C445997")
        self.bc_aliasCode_label = Label(masterFrame, text="AliasCode: ")
        self.bc_aliasCode_label.grid(row=3,column=0,sticky="W", in_=masterFrame)
        self.bc_aliasCode_entry = Entry(masterFrame,textvariable=self.bc_aliasCode_value)
        self.bc_aliasCode_entry.configure(state=DISABLED)
        self.bc_aliasCode_entry.grid(row=3,column=1, sticky="WE", in_=masterFrame,padx=1)
        # synonyms:Label            synonyms:Lisbox
        self.bc_synonyms_frame = Frame(masterFrame)
        self.bc_synonyms_frame.grid(row=3, column=1,sticky="WE",padx=1)
        self.dummySynonyms = ["David","Goliath","Synonym 3",]
        self.bc_synonyms_value = StringVar(value=self.dummySynonyms)
        self.bc_synonyms_label = Label(masterFrame, text="Synonyms: ")
        self.bc_synonyms_label.grid(row=3,column=0,sticky="W", in_=masterFrame)
        self.bc_synonyms_listbox = Listbox(self.bc_synonyms_frame,listvariable=self.bc_synonyms_value)
        self.bc_synonyms_yscrollbar = Scrollbar(self.bc_synonyms_frame,orient=VERTICAL,command=self.bc_synonyms_listbox.yview)
        self.bc_synonyms_yscrollbar.pack(anchor="ne",fill="y",side="right")
        self.bc_synonyms_listbox.configure(yscrollcommand=self.bc_synonyms_yscrollbar.set)
        if len(self.dummySynonyms) < 6:
            lbHeight = len(self.dummySynonyms)
            self.bc_synonyms_yscrollbar.config(width=-1)
        else:
            lbHeight = 5
            self.bc_synonyms_yscrollbar.config(width=12)
        self.bc_synonyms_listbox.config(height=lbHeight)
        self.bc_synonyms_listbox.pack(anchor="nw",fill="both", expand=True, side="left")
        #                           new_synonym:Entry   add_Button:Button
        self.bc_synonyms_entry_frame = Frame(masterFrame)
        self.bc_synonyms_entry_frame.grid(row=5,column=1,sticky="EW")
        self.bc_synonyms_entry_value = StringVar()
        self.bc_synonyms_entry = Entry(self.bc_synonyms_entry_frame,textvariable=self.bc_synonyms_entry_value)
        self.bc_synonyms_entry.pack(anchor="w",side="left",fill="x",expand=True)
        self.bc_synonyms_entry_button = Button(self.bc_synonyms_entry_frame,text="add", command=lambda:self.synonym_add_cmd(self.bc_synonyms_entry.get()))
        self.bc_synonyms_entry_button.pack(anchor="w", fill="none",side="right",before=self.bc_synonyms_entry)
        
        self.bc_synonyms_entry.bind("<Return>", lambda event: self.synonym_add_cmd(self.bc_synonyms_entry.get()))

        dummyProperties = [{
            "id_":"C2389",
            "label":"Testing Prop",
            "isRequired":1,
            "isEnabled":0,
            "dataType":"Blood sample",
            "notes":[f"Bla bla\n bla", "This is a crutial note", "this is super important too"]
        # },
        # {
        #     "id_":"C2349",
        #     "label":"Testing Prop 2",
        #     "isRequired":1,
        #     "isEnabled":0,
        #     "dataType":"Bs",
        #     "notes":["Bla bla bla", "This is a crutial note", "this is super important too"]
        # },{
        #     "id_":"C2239",
        #     "label":"Testing Prop",
        #     "isRequired":0,
        #     "isEnabled":1,
        #     "dataType":"Blood sample",
        #     "notes":["Bla bla bla", "This is a crutial note", "this is super important too"]
        }]
        # h_bar = ttk.Separator(masterFrame,orient="horizontal")
        # h_bar.grid(column=0,columnspan=2,row=6,sticky="WE",pady=5)

        # testLabel = Label(self.active_biomedical_concept_overview_lframe,text="Properties:")
        # testLabel.grid(column=0,row=7)
        # testLabel.pack(anchor="n",after=self.active_biomedical_concept_overview_mainframe,expand=True,side="left", fill="x")
        self.propertiesFrame = LabelFrame(self.active_biomedical_concept_overview_lframe,text="Properties:",)
        self.propertiesFrame.pack(anchor="nw", after=self.active_biomedical_concept_overview_mainframe,side=TOP,fill="both",expand=True,in_=self.active_biomedical_concept_overview_lframe)
        # self.propertiesFrame.grid(column=0,columnspan=2,row=8,sticky="WSE",padx=3,pady=3)
        
        self.properties_scrollbar_x = Scrollbar(self.propertiesFrame, orient=HORIZONTAL)
        self.properties_scrollbar_y = Scrollbar(self.propertiesFrame, orient=VERTICAL)
        self.propertiesCanvas = Canvas(self.propertiesFrame, yscrollcommand=self.properties_scrollbar_y.set, xscrollcommand=self.properties_scrollbar_x.set)
        self.properties_frame_inside=Frame(self.propertiesCanvas)
        self.propertiesCanvas.create_window((0,0),anchor="nw",window=self.properties_frame_inside)
        self.propertiesCanvas.config(bg="red")
        self.properties_frame_inside.config(background="green")
        # self.properties_frame_inside.pack(anchor="nw",fill=BOTH, expand=True,side=TOP)
        # self.active_biomedical_concept_overview_lframe = ttk.LabelFrame(self.mainframe,text=f"Active BC:\n")
        # self.propertiesCanvas.pack(anchor="nw", width=UIDisplay.__data_column_width[2],x=UIDisplay.__data_column_width[0]+UIDisplay.__data_column_width[1], in_=self.mainframe)
        self.propertiesCanvas.grid(column=0, row=0, sticky="NWES")
        self.properties_scrollbar_x.grid(column=0, row=1, sticky="WE")
        self.properties_scrollbar_y.grid(column=1, row=0, sticky="NS")
        self.propertiesFrame.rowconfigure(0,weight=1)
        self.propertiesFrame.columnconfigure(0,weight=1)

        
        
        self.properties_frame_inside.bind("<Configure>",lambda event: self.propertiesCanvas.configure(scrollregion=self.propertiesCanvas.bbox("all")))
        # self.properties_scrollbar_y.pack(anchor="se",expand=False, fill="y",side="right")
        # self.propertiesCanvas.pack(anchor="sw",expand=True,fill="both",side="left",after=self.properties_scrollbar_y)
        # self.propertiesCanvas.grid(column=0,columnspan=2,row=8,sticky="NESW")
        # print(self.propertiesCanvas.winfo_y()) # 0

        self.properties_scrollbar_y["command"] = self.propertiesCanvas.yview
        self.properties_scrollbar_x["command"] = self.propertiesCanvas.xview
        # self.propertiesCanvas.config(yscrollcommand=self.properties_scrollbar_y.set)
        # self.properties_scrollbar_y.pack(column=1,row=8,sticky="NSE")
        
        prop_index = 0
        attributes = 5
        attribute_index=0

        self.prop_name_label:list[Label] = []
        self.prop_name_var:list[StringVar] = []
        self.prop_name_entry:list[Entry] = []

        self.prop_id_var:list[StringVar] = []
        self.prop_id_label:list[Label] = []
        self.prop_id_entry:list[Entry] = []

        self.prop_isRequired_var:list[IntVar] = []
        self.prop_isRequired_label:list[Label] = []
        self.prop_isRequired_checkBox:list[Checkbutton] = []

        self.prop_isEnabled_var:list[IntVar] = []
        self.prop_isEnabled_label:list[Label] = []
        self.prop_isEnabled_checkBox:list[Checkbutton] = []

        self.prop_datatype_var:list[StringVar] = []
        self.prop_datatype_label:list[Label] = []
        self.prop_datatype_entry:list[Entry] = []

        self.prop_notes_var:list[list[StringVar]] = [[]]
        self.prop_notes_label:list[Label] = []
        # self.prop_notes_frames:list[Frame] = []
        self.prop_notes_Textbox:list[list[Text]] = [[]]
        self.textbox_rows:list[int] = []


        for prop in dummyProperties:
            # Label
            self.prop_name_label.append(Label(self.properties_frame_inside,text="Property:"))
            self.prop_name_label[prop_index].grid(column=0,row=prop_index*attributes+attribute_index,sticky="W")
            self.prop_name_var.append(StringVar(value=prop["label"]))
            self.prop_name_entry.append(Entry(self.properties_frame_inside,textvariable=self.prop_name_var[prop_index]))
            self.prop_name_entry[prop_index].grid(column=1,row=prop_index*attributes+attribute_index,sticky="WE")
            attribute_index+=1
            # ID
            self.prop_id_var.append(StringVar(value=prop["id_"]))
            self.prop_id_label.append(Label(self.properties_frame_inside, text="Property Id: "))
            self.prop_id_label[prop_index].grid(column=0,row=prop_index*attributes+attribute_index,sticky="W",)
            self.prop_id_entry.append(Entry(self.properties_frame_inside,textvariable=self.prop_id_var[prop_index]))
            self.prop_id_entry[prop_index].grid(column=1,row=prop_index*attributes+attribute_index,sticky="WE",)
            self.prop_id_entry[prop_index].configure(state="disabled")
            attribute_index+=1
            # Is Required
            self.prop_isRequired_var.append(IntVar(value=prop["isRequired"]))           # print(prop["isRequired"])
            self.prop_isRequired_label.append(Label(self.properties_frame_inside,text="Required:"))
            self.prop_isRequired_label[prop_index].grid(column=0,row=prop_index*attributes+attribute_index,sticky="W")
            self.prop_isRequired_checkBox.append(Checkbutton(self.properties_frame_inside,variable=self.prop_isRequired_var[prop_index]))
            self.prop_isRequired_checkBox[prop_index].grid(column=1,row=prop_index*attributes+attribute_index,sticky="W")
            attribute_index+=1
            # Is Enabled
            self.prop_isEnabled_var.append(IntVar(value=prop["isEnabled"]))           # print(prop["isEnabled"])
            self.prop_isEnabled_label.append(Label(self.properties_frame_inside,text="Enabled:"))
            self.prop_isEnabled_label[prop_index].grid(column=0,row=prop_index*attributes+attribute_index,sticky="W")
            self.prop_isEnabled_checkBox.append(Checkbutton(self.properties_frame_inside,variable=self.prop_isEnabled_var[prop_index]))
            self.prop_isEnabled_checkBox[prop_index].grid(column=1,row=prop_index*attributes+attribute_index,sticky="W")
            attribute_index+=1

            # Datatype
            self.prop_datatype_var.append(StringVar(value=prop["dataType"]))
            self.prop_datatype_label.append(Label(self.properties_frame_inside, text="Property Datatype: "))
            self.prop_datatype_label[prop_index].grid(column=0,row=prop_index*attributes+attribute_index,sticky="W",)
            self.prop_datatype_entry.append(Entry(self.properties_frame_inside,textvariable=self.prop_datatype_var[prop_index]))
            self.prop_datatype_entry[prop_index].grid(column=1,row=prop_index*attributes+attribute_index,sticky="WE",)
            attribute_index+=1


            # Notes
            self.prop_notes_label.append(Label(self.properties_frame_inside, text="Property Notes: "))
            self.prop_notes_label[prop_index].grid(column=0,row=prop_index*attributes+attribute_index,sticky="NW",)
            self.prop_notes_var.append([])
            self.prop_notes_Textbox.append([])
            for note_index, note in enumerate(prop["notes"]):
                self.prop_notes_var[prop_index].append(note)
                self.prop_notes_Textbox[prop_index].append(Text(self.properties_frame_inside))
                self.prop_notes_Textbox[prop_index][note_index].insert('end',self.prop_notes_var[prop_index][note_index])
                # lines = self.prop_notes_Textbox[prop_index][noteIndex].count("1.0", "end","lines")[0]+1
                self.prop_notes_Textbox[prop_index][note_index].configure(height=4,insertwidth=5) # Reduced with, so it isn't massive

                self.prop_notes_Textbox[prop_index][note_index].grid(column=1,row=prop_index*attributes+attribute_index+note_index,sticky="W",)
                self.textbox_rows.append(prop_index*attributes+attribute_index+note_index)

            # self.prop_notes_var.append(StringVar(value=prop["notes"]))
            # self.prop_notes_Textbox.append(Text(self.propertiesCanvas,textvariable=self.prop_notes_var[prop_index]))

            attribute_index+=1
            # Separator
            # ttk.Separator(self.propertiesCanvas,orient="horizontal").grdatatype(column=0, columnspan=2,row=prop_index*attributes+attribute_index,sticky="WE",pady=2)
            prop_index+=1
            attribute_index=0
        # self.properties_frame_inside.rowconfigure(self.textbox_rows,weight=1,uniform=1)
        self.properties_frame_inside.columnconfigure(1,weight=1)
        self.properties_frame_inside.columnconfigure(0,weight=1)


        # self.propertiesCanvas.grid(column=0,row=6)








        # properties:LabelFrame:    // Treeview?   
        # [
        # property_label:TextField  property_enabled:CheckButton(prop.enabled)
        # required_label:Label      property_required:CheckButton(prop.required)
        
        # code_label:Label          code_field:Entry
        # type_label:Label          type_value:Entry
        # Notes_list:Listbox        Notes_field:TextBox
        # ]





    def synonym_add_cmd(self, *args):
        self.dummySynonyms.append(args[0])
        self.bc_synonyms_value.set(self.dummySynonyms)
        lbHeight = 0
        if len(self.dummySynonyms) < 6:
            lbHeight = len(self.dummySynonyms)
            self.bc_synonyms_yscrollbar.config(width=-1)
        else:
            lbHeight = 5
            self.bc_synonyms_yscrollbar.config(width=12)

        self.bc_synonyms_listbox.config(height=lbHeight)
        self.bc_synonyms_entry_value.set("")

    def set_active_category(self, category_name:str, bc_names:list[str]):
        self.active_category_overview_lframe.configure(text=f"{category_name}")
        self.biomedical_concepts_in_category.set(bc_names)

    # Functions:
    def on_category_click(self, *args):
        try:
            category_index = args[0]

            result = self.__app_instance.select_category(category_index)
            # result = self.__app_instance.select_category("age")
            print(result["bc_names"])
            self.set_active_category(result["category_name"],result["bc_names"])

        except ValueError:
            print(ValueError)

    def on_active_bc_click(self, *args):
        try:
            bc_selection_index = args[0]

            self.__app_instance.select_bc(bc_selection_index)
        except ValueError:
            pass
    # def on_biomedical_concept_click(self,*args):
    #         try:
    #             value = current_bcs[Listbox.curselection(bcs_in_current_category)[0]]
    #         except ValueError:
    #             pass

