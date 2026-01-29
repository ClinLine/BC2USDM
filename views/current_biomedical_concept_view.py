from tkinter import Button, Entry, Frame, Label, LabelFrame, Listbox, Scrollbar, StringVar
from tkinter.constants import *

from views.notes_frame import NotesFrame
from views.property.properties_view import PropertiesView


# and the UI code is a mess
class CurrentBiomedicalConceptView(LabelFrame):
    DEFAULT_TITLE = "Current Biomedical Concept"
    def __init__(self, parent,  width, x, **kwargs):
        if "title" in kwargs.keys():
            title = kwargs["title"]
        else:
            title = self.DEFAULT_TITLE

        super().__init__(parent.root, text=title, **kwargs)

        # self.active_biomedical_concept_overview_lframe = ttk.LabelFrame(self,text="Active BC:")
        # self.active_biomedical_concept_overview_lframe.place(anchor="nw", relheight=1, width=width,x=x)
        self.place(relheight=1, width=width, x=x)

        self.master_frame = Frame(self)
        self.master_frame.pack(side=TOP, fill=BOTH, expand=False)
        print(self.master_frame.master.widgetName)


        self.bc_name_label = Label(self, text="Name: ")
        self.bc_name_label.grid(row=0,column=0,sticky="W",in_=self.master_frame)
        self.bc_name_value = StringVar(value="")
        self.bc_name_entry = Entry(self, textvariable=self.bc_name_value)
        self.bc_name_entry.grid(row=0,column=1,sticky="WE",in_=self.master_frame,padx=1)
        self.master_frame.columnconfigure(1,weight=1)
        self.master_frame.columnconfigure(0,uniform=TRUE)


        # label_label:Label         label:Textbox
        # ID_Label:Label            ID:Disabled_Text
        self.bc_id_label = Label(self,text="Id: ")
        self.bc_id_value = StringVar(value="")
        self.bc_id_label.grid(row=1,column=0,sticky="W", in_=self.master_frame)
        self.bc_id_entry = Entry(self,textvariable=self.bc_id_value)
        self.bc_id_entry.configure(state="readonly")
        self.bc_id_entry.grid(row=1,column=1, sticky="WE", in_=self.master_frame,padx=1)
        
        # reference_label:Label     url:Disabled_Text
        self.bc_reference_value = StringVar(value="")
        self.bc_reference_label = Label(self, text="Reference: ")
        self.bc_reference_label.grid(row=2,column=0,sticky="W", in_=self.master_frame)
        self.bc_reference_entry = Entry(self,textvariable=self.bc_reference_value)
        self.bc_reference_entry.configure(state="readonly")
        self.bc_reference_entry.grid(row=2,column=1, sticky="WE", in_=self.master_frame,padx=1)

        # code_label:Label          code:Disabled_Text
        self.bc_alias_code_value = StringVar(value="")
        self.bc_alias_code_label = Label(self, text="AliasCode: ")
        self.bc_alias_code_label.grid(row=3,column=0,sticky="W", in_=self.master_frame)
        self.bc_alias_code_entry = Entry(self,textvariable=self.bc_alias_code_value)
        self.bc_alias_code_entry.configure(state="readonly")
        self.bc_alias_code_entry.grid(row=3,column=1, sticky="WE", in_=self.master_frame,padx=1)
        # synonyms:Label            synonyms:Lisbox
        self.bc_synonyms_frame = Frame(self)
        self.bc_synonyms_frame.grid(row=3, column=1,sticky="WE",padx=1, in_=self.master_frame)
        self.bc_synonyms_value = StringVar(value="")
        self.bc_synonyms_label = Label(self, text="Synonyms: ")
        self.bc_synonyms_label.grid(row=3,column=0,sticky="W", in_=self.master_frame)
        self.bc_synonyms_listbox = Listbox(self,listvariable=self.bc_synonyms_value)
        self.bc_synonyms_yscrollbar = Scrollbar(self,orient=VERTICAL,command=self.bc_synonyms_listbox.yview)
        self.bc_synonyms_yscrollbar.pack(anchor="ne",fill="y",side=RIGHT,in_=self.bc_synonyms_frame)
        self.bc_synonyms_listbox.configure(yscrollcommand=self.bc_synonyms_yscrollbar.set)
        temp_synonyms = self.bc_synonyms_value.get()
        if len(temp_synonyms) < 6:
            lbl_height = len(temp_synonyms)
            self.bc_synonyms_yscrollbar.config(width=-1)
        else:
            lbl_height = 5
            self.bc_synonyms_yscrollbar.config(width=12)
        self.bc_synonyms_listbox.config(height=lbl_height)
        self.bc_synonyms_listbox.pack(anchor="nw",fill="both", expand=True, side="left",in_=self.bc_synonyms_frame)
        #                           new_synonym:Entry   add_Button:Button
        self.bc_synonyms_entry_frame = Frame(self)
        self.bc_synonyms_entry_frame.grid(row=5,column=1,sticky="EW", in_=self.master_frame)
        self.bc_synonyms_entry_value = StringVar(value="")
        self.bc_synonyms_entry = Entry(self.bc_synonyms_entry_frame,textvariable=self.bc_synonyms_entry_value)
        self.bc_synonyms_entry.pack(anchor="w",side="left",fill="x",expand=True)
        self.bc_synonyms_entry_button = Button(self.bc_synonyms_entry_frame,text="add", command=lambda:self.synonym_add_cmd(self.bc_synonyms_entry.get()))
        self.bc_synonyms_entry_button.pack(anchor="w", fill="none",side="right",before=self.bc_synonyms_entry)

        self.bc_synonyms_entry.bind("<Return>", lambda event: self.synonym_add_cmd(self.bc_synonyms_entry.get()))
        # self.bc_synonyms_entry.bind("<Return>", self.synonym_add_cmd)
        
        self.notes_frame = NotesFrame(self, notes="")
        # self.notes_frame.pack(side=TOP, fill=BOTH, expand=FALSE)
        self.notes_frame.grid(row=6, column=0, columnspan=2, sticky=NSEW, in_=self.master_frame)
        

        self.properties_frame = PropertiesView(self, frame_title="Properties:", properties=None)
        self.properties_frame.pack(side=TOP, fill=BOTH, expand=True)

        # Add add and remove btn
        self.btn_frame = Frame(self)
        self.btn_frame.pack(side=BOTTOM, fill=BOTH, expand=FALSE, padx=(5,5), pady=(0,5))
        self.apply_txt_var = StringVar(value="Add")
        self.apply_btn = Button(self.btn_frame, textvariable=self.apply_txt_var)
        self.apply_btn.grid(row=0,column=1, sticky=EW)
        
        self.remove_btn = Button(self.btn_frame, text="Remove")
        self.remove_btn.grid(row=0,column=0, sticky=EW)
        self.btn_frame.columnconfigure(0,weight=1)
        self.btn_frame.columnconfigure(1,weight=1)

    def apply_changes_to_repository(self):
        label = self.bc_name_value.get()
        code = self.bc_id_value.get()
        ref = self.bc_reference_value.get()

        synonyms = self.bc_synonyms_value.get()
        print(synonyms)
        # synonyms = self.bc_synonyms_listbox.get()

        notes = self.notes_frame.get_notes()

        properties = self.properties_frame.get_properties()


        
        self.parent.apply_to_repository(label, code, ref, synonyms, notes, properties)

    def remove_bc_from_repository(self):
        self.parent.remove_bc_from_repository(self.bc_id_value)

    def synonym_add_cmd(self, *args):
        temp_synonyms = list(self.bc_synonyms_listbox.get(0,END)) # to list is required as typles are immutable
        if len(temp_synonyms) == 0:
            temp_synonyms = (args[0])
        else:
            temp_synonyms.append(args[0])
        # self.dummy_synonyms.append(args[0])

        self.bc_synonyms_value.set(temp_synonyms)
        label_height = 0
        if len(temp_synonyms) < 6:
            label_height = len(temp_synonyms)
            self.bc_synonyms_yscrollbar.config(width=-1)
        else:
            label_height = 5
            self.bc_synonyms_yscrollbar.config(width=12)

        self.bc_synonyms_listbox.config(height=label_height)
        self.bc_synonyms_entry_value.set("")

    def update_view(self, bc, **kwargs):
        # for kw, arg in kwargs:
        #     print(f"{kw}:{arg}")

        self.bc_reference_value.set(bc.reference)
        self.bc_id_value.set(bc.code.standard_code.code)
        self.bc_name_value.set(bc.label)

        self.notes_frame.add_notes(bc.notes)

        self.bc_synonyms_value.set(bc.synonyms)
        print(self.bc_synonyms_value.get())

        # properties
        self.properties_frame.reset()
        self.properties_frame.add_properties(bc.properties)
        # if bc._properties is not None:
        #     for prop in bc._properties:
        #         self.properties_frame.add_property(prop)
            
