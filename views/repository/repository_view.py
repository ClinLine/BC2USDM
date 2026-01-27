from tkinter import Entry, IntVar, Label, LabelFrame, Listbox, Scrollbar, StringVar, Variable
from tkinter.constants import *
from uuid import uuid4 as guid

from models.USDM.therapeutic_area import TherapeuticArea



class RepositoryView(LabelFrame):
    __TITLE_TEXT:str = "Your respository: "
    therapeutic_area_conainer = None
    category_container = None
    added_biomedical_concepts_container = None


    def __init__(self, parent, **kwargs):
        x = kwargs["x"]
        del kwargs["x"]

        if "title" in kwargs.keys():
            title = kwargs["title"]
            del kwargs["title"]
        else:
            title = RepositoryView.__TITLE_TEXT

        super().__init__(parent.root, text=title, **kwargs)
        # super().pack(anchor=NE,expand=TRUE, fill=BOTH,side=RIGHT)
        
        self.therapeutic_area_conainer = TherapeuticAreaView(self)
        self.categories_container = RepositoryCategoryView(self)
        self.added_biomedical_concepts_container = RepositoryBiomedicalConceptsContainer(self)
        
        super().place(anchor="nw",width=kwargs["width"], x=x, relheight=1)

class TherapeuticAreaView(LabelFrame):
    __TITLE_TEXT:str = "Therapeutic Area: "
    def __init__(self, parent, **kwargs):
        
        if "title" in kwargs.keys():
            title = kwargs["title"]
            del kwargs["title"]
        else:
            title = TherapeuticAreaView.__TITLE_TEXT
        super().__init__(parent, text=title, **kwargs)
        super().pack(anchor=N, expand=TRUE, fill=X, side=TOP)

        _row = 0
        # Initialize UI elements:
        #   - "id": "$(uuid4)"                                                          -> Generated Value
        Label(self, text="Id:").grid(row=_row,column=0, sticky=W)
        self.id_var = StringVar(value=f"{guid()}")
        id_entry = Entry(self,justify=LEFT,textvariable=self.id_var)
        id_entry.grid(row=(_row:=_row+1)-1,column=1,sticky=(N,W,S,E))
        id_entry.config(state=DISABLED)
        
        #   - "Code": "TA_$(id)"                                                        -> Entry
        Label(self, text="Code:").grid(row=_row, column=0, sticky=W)
        self.code_var = StringVar(value=f"TA_{self.id_var.get()}")
        code_entry = Entry(self, justify=LEFT, textvariable=self.code_var, state=DISABLED)
        code_entry.grid(row=(_row:=_row+1)-1, column=1, sticky=NSEW)

        #   - "codeSystem": "CUSTOM"                                                    -> Const Value
        # Label(self, text="Code system:").grid(row=_row, column=0, sticky=W)
        # self.code_system_var = StringVar(value="CUSTOM")
        # code_system_entry = Entry(self, justify=LEFT, textvariable=self.code_system_var, state=DISABLED)
        # code_system_entry.grid(column=1, row=(_row:=_row+1)-1, sticky=NSEW)

        #   - "codeSystemVersion": "$(DocumentVersion)"                                 -> Generated Value
        Label(self, text="Version:").grid(row=_row, column=0, sticky=W)
        self.document_version_var = StringVar(value="0.0.0")
        code_system_entry = Entry(self, justify=LEFT, textvariable=self.document_version_var)
        code_system_entry.grid(column=1, row=(_row:=_row+1)-1, sticky=NSEW)

        
        #   - "instanceType":"Code"                                                     -> Const Value
        # Label(self, text="Instance type:").grid(row=_row, column=0, sticky=W)
        # self.document_version_var = StringVar(value="Code")
        # code_system_entry = Entry(self, justify=LEFT, textvariable=self.document_version_var, state=DISABLED)
        # code_system_entry.grid(column=1, row=(_row:=_row+1)-1, sticky=NSEW)
        
        #   - "decode": "$(..Entered value..)"                                          -> Entry
        Label(self, text="Description").grid(row=_row, column=0, sticky=W)
        self.decode_var = StringVar(value="")
        code_system_entry = Entry(self, justify=LEFT, textvariable=self.decode_var)
        code_system_entry.grid(column=1, row=(_row:=_row+1)-1, sticky=NSEW)
        
        self.columnconfigure(index=1, weight=1)
        self.columnconfigure(index=0, uniform=1)


    def set_id(self, new_id:str):
        self.id_var.set(new_id)

    def set_therapeutic_area(self, therapeutic_area:TherapeuticArea):
        ...
        raise NotImplementedError()
    


class RepositoryCategoryView(LabelFrame):
    __TITLE_TEXT:str = "Your categories: "
    def __init__(self, parent, **kwargs):
        
        if "title" in kwargs.keys():
            title = kwargs["title"]
            del kwargs["title"]
        else:
            title = RepositoryCategoryView.__TITLE_TEXT
        super().__init__(parent, text=title, **kwargs)

        super().pack(anchor=NW, expand=TRUE, fill=BOTH, side=TOP)
    # Add container to edit (custom) Category
    # (For now only one category)
    #   - "id": "$(guid)"                                                           -> Generated Value
    #   - "name": "$(label)_$(id)"                                                  -> Generated Value
    #   - "description": "$(.. entered description, if in tool available ..)",      -> Entry (and/or lookup)
    #   - "label" "$(.. copied and/or changed label from BC library)",              -> Entry
    #   - "code":"...Code from BC library if label not changed"                     -> Entry (and/or lookup)
    #   - "childIds":[]                                                             -> const (empty Array)
    #   - "memberIds": [$(BimodecidalConcept1), $(BiomedicalConcept2)],             -> Derived value
    #   - "instanceType": "BiomedicalConceptCategory",                              -> Const Value
    #   - "notes": []                                                               -> const (empty Array)

class RepositoryBiomedicalConceptsContainer(LabelFrame):
    __TITLE_TEXT:str = "Your Biomedical Concepts:"

    def __init__(self, parent, **kwargs):
        if "title" in kwargs.keys():
            title = kwargs["title"]
            del kwargs["title"]
        else:
            title = RepositoryBiomedicalConceptsContainer.__TITLE_TEXT
        super().__init__(parent, text=title, **kwargs)
        self.bcs_var = Variable(value=["test1", "test2", "test3"])
        bc_scrollbarY = Scrollbar(self,orient=VERTICAL)
        bc_scrollbarY.grid(column=1,row=0,sticky=(N,E,S))
        self.bc_list = Listbox(self, justify=LEFT, listvariable=self.bcs_var, yscrollcommand=bc_scrollbarY.set)
        self.bc_list.grid(column=0, row=0, sticky=NSEW)
        bc_scrollbarY.config(command=self.bc_list.yview)
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)



        super().pack(anchor=NE, expand=TRUE, fill=BOTH, side=BOTTOM)

    
    # Add container with list with added BCs
    #   - List(box) / customn listbox
    #       + code                                                          -> Known value (selection/lookup)
    #       + label                                                         -> Known value (selection/lookup)
    #   code + label = btn