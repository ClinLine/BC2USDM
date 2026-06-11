from tkinter import Button, Entry, Frame, Label, LabelFrame, Listbox, Scrollbar, StringVar, Variable
# from tkinter.constants import *
from tkinter.constants import N, E, S, W # cardinals, sticky
from tkinter.constants import NW, SE, SW # Anchors
from tkinter.constants import VERTICAL # Allignment
from tkinter.constants import X, BOTH # X/Y & Expand
from tkinter.constants import TOP, LEFT, RIGHT # Side

from utils.b_colors import BColors
from models.USDM.biomedical_concept import BiomedicalConcept
from models.USDM.biomedical_concept_category import BiomedicalConceptCategory
from models.USDM.therapeutic_area import TherapeuticArea



class RepositoryView(LabelFrame):
    __TITLE_TEXT:str = "Your respository: "
    therapeutic_area_container = None
    category_container = None
    added_biomedical_concepts_container = None
    parent = None

    def __init__(self, parent, **kwargs):
        self.parent = parent
        x = kwargs[X]
        del kwargs[X]

        if "title" in kwargs.keys():
            title = kwargs["title"]
            del kwargs["title"]
        else:
            title = RepositoryView.__TITLE_TEXT

        super().__init__(parent.root, text=title, **kwargs)
        # super().pack(anchor=NE,expand=TRUE, fill=BOTH,side=RIGHT)
        
        self.get_therapeutic_area = lambda index=0 : self.parent.main_app.get_therapeutic_areas(index)
        self.therapeutic_area_container = TherapeuticAreaView(self)
        
        # self.categories_container = RepositoryCategoryView(self)
        self.added_biomedical_concepts_container = RepositoryBiomedicalConceptsContainer(self)
        
        super().place(anchor=NW,width=kwargs["width"], x=x, relheight=1)

        self.set_document_version = parent.main_app.set_document_version
        self.set_therapeutic_area_decode = parent.main_app.set_therapeutic_area_decode

    def update_bc_list(self, bcs:list[BiomedicalConcept]):
        self.added_biomedical_concepts_container.update_biomedical_concepts_list(bcs)

    # def update_cat_list(self, categories:list[BiomedicalConceptCategory]):
    #     self.categories_container.update_category_list(categories)

    def open_selected_category(self, selection):
        self.parent.open_selected_category(selection)

    def open_selected_biomedical_concept(self, selection):
        self.parent.open_selected_biomedical_concept(selection)

    def remove_bc_from_repository(self, selection:int) -> None:
        self.parent.remove_nth_bc_from_repository(selection)

    def set_editor_apply_btn_text(self, value:str="Add"):
        self.parent.set_editor_apply_btn_text(value)
    
    

class TherapeuticAreaView(LabelFrame):
    __TITLE_TEXT:str = "Therapeutic Area: "
    def __init__(self, parent, **kwargs):
        self.parent = parent
        if "title" in kwargs.keys():
            title = kwargs["title"]
            del kwargs["title"]
        else:
            title = TherapeuticAreaView.__TITLE_TEXT
        super().__init__(parent, text=title, **kwargs)
        super().pack(anchor=N, expand=False, fill=X, side=TOP)

        this_ta = parent.get_therapeutic_area()

        _row = 0
        # Initialize UI elements:
        #   - "id": "$(uuid4)"                                                          -> Generated Value
        Label(self, text="Id:").grid(row=_row,column=0, sticky=W)
        self.id_var = StringVar(value=f"{this_ta.code.id_}")
        id_entry = Entry(self,justify=LEFT,textvariable=self.id_var)
        id_entry.grid(row=(_row:=_row+1)-1,column=1,sticky=(N,W,S,E))
        id_entry.config(state="readonly")
        
        #   - "Code": "TA_$(id)"                                                        -> Entry
        Label(self, text="Code:").grid(row=_row, column=0, sticky=W)
        self.code_var = StringVar(value=this_ta.code.code)
        code_entry = Entry(self, justify=LEFT, textvariable=self.code_var, state="readonly")
        code_entry.grid(row=(_row:=_row+1)-1, column=1, sticky=(N,W,S,E))

        # Skipping UI element since this is a constant value
        #   - "codeSystem": "CUSTOM"                                                    -> Const Value
        # Label(self, text="Code system:").grid(row=_row, column=0, sticky=W)
        # self.code_system_var = StringVar(value="CUSTOM")
        # code_system_entry = Entry(self, justify=LEFT, textvariable=self.code_system_var, state=DISABLED)
        # code_system_entry.grid(column=1, row=(_row:=_row+1)-1, sticky=NSEW)

        #   - "codeSystemVersion": "$(DocumentVersion)"                                 -> Generated Value
        Label(self, text="Version:").grid(row=_row, column=0, sticky=W)
        self.document_version_var = StringVar(value=this_ta.code.code_system_version)
        document_version_entry = Entry(self, justify=LEFT, textvariable=self.document_version_var)
        document_version_entry.grid(column=1, row=(_row:=_row+1)-1, sticky=(N,W,S,E))
        document_version_entry.bind("<FocusOut>",self.on_version_entry_focus_out)
        
        # Skipping ui element since this a contant value
        #   - "instanceType":"Code"                                                     -> Const Value
        # Label(self, text="Instance type:").grid(row=_row, column=0, sticky=W)
        # self.document_version_var = StringVar(value="Code")
        # code_system_entry = Entry(self, justify=LEFT, textvariable=self.document_version_var, state=DISABLED)
        # code_system_entry.grid(column=1, row=(_row:=_row+1)-1, sticky=NSEW)
        
        #   - "decode": "$(..Entered value..)"                                          -> Entry
        Label(self, text="Description").grid(row=_row, column=0, sticky=W)
        self.decode_var = StringVar(value=this_ta.code.decode)
        decode_entry = Entry(self, justify=LEFT, textvariable=self.decode_var)
        decode_entry.grid(column=1, row=(_row:=_row+1)-1, sticky=(N,W,S,E))
        decode_entry.bind("<FocusOut>", self.on_decode_entry_focus_out)
        
        self.columnconfigure(index=1, weight=1)
        self.columnconfigure(index=0, uniform=1)


    def set_id(self, new_id:str):
        self.id_var.set(new_id)

    def set_therapeutic_area(self, therapeutic_area:TherapeuticArea):
        self.id_var.set(therapeutic_area.code.id_)
        self.code_var.set(therapeutic_area.code.code)
        self.document_version_var.set(therapeutic_area.code.code_system_version)
        self.decode_var.set(therapeutic_area.get_decode())

    def on_version_entry_focus_out(self, event, *args):
        self.parent.set_document_version(self.document_version_var.get())
    
    def on_decode_entry_focus_out(self, event, *args):
        self.parent.set_therapeutic_area_decode(self.id_var.get(), self.decode_var.get())
        # print("left description entry")


class RepositoryCategoryView(LabelFrame):
    __TITLE_TEXT:str = "Your categories: "
    parent:RepositoryView = None

    def __init__(self, parent:RepositoryView, **kwargs):
        self.parent = parent
        if "title" in kwargs.keys():
            title = kwargs["title"]
            del kwargs["title"]
        else:
            title = RepositoryCategoryView.__TITLE_TEXT
        super().__init__(parent, text=title, **kwargs)
        
        self.category_names_var = Variable(value=[])
        category_scrollbar_y = Scrollbar(self,orient=VERTICAL)
        category_scrollbar_y.grid(column=1,row=0,sticky=(N,E,S))
        self.category_list = Listbox(
            self,
            justify=LEFT,
            listvariable=self.category_names_var,
            yscrollcommand=category_scrollbar_y.set,
            state="disabled" # Disabling listbox since category editing isn't supported yet
            )
        self.category_list.bind("<ButtonRelease>", self.category_list_select)
        self.category_list.grid(column=0, row=0, sticky=(N,W,S,E))
        category_scrollbar_y.config(command=self.category_list.yview)
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)

        # # Add buttons to manage categories later:
        # btns_frame = Frame(self)
        # # Stick buttons to the bottom of this container
        # btns_frame.grid(column=0, row=1, columnspan=2, sticky=(S,E,W))
        # remove_btn = Button(btns_frame, text="Remove")
        # open_btn = Button(btns_frame, text="Open")

        # remove_btn.pack(anchor="sw", fill=X, side=LEFT, expand=TRUE)
        # open_btn.pack(anchor="se", fill=X, side=RIGHT, expand=TRUE)

        # TODO: Re anable packinging when supporting category customization again
        # super().pack(anchor=N, expand=TRUE, fill=BOTH, side=TOP)

    def category_list_select(self, *args):
        # TODO: Do we still need this, might be better handeled with btns
        print(f"{BColors.WARNING}WARN|[{self.__class__.__name__}].categoryListSelect: Re-selecting categories is not implemented yet.{BColors.ENDC}")
        cur_selection = self.category_list.curselection()
        print(cur_selection)
        try:
            selection = self.category_list.curselection()[0]
        except IndexError as err:
            # TODO add optional verbose/dev logging
            # Assuming listbox is empty when getting an index out of range error
            # So returning
            return
        else:
            self.parent.open_selected_category(selection)
        for arg in args:
            print(f"{arg}")
        raise NotImplementedError()
    
    def update_category_list (self, categories:list[BiomedicalConceptCategory]):
        cat_strings:list[str] = [f"{category.label}" for category in categories]
        self.category_names_var.set(cat_strings)

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
    #   - "notes": []

class RepositoryBiomedicalConceptsContainer(LabelFrame):
    __TITLE_TEXT:str = "Your Biomedical Concepts:"
    _btn_padding:int = 5

    def __init__(self, parent, **kwargs):
        self.parent = parent
        if "title" in kwargs.keys():
            title = kwargs["title"]
            del kwargs["title"]
        else:
            title = RepositoryBiomedicalConceptsContainer.__TITLE_TEXT
        super().__init__(parent, text=title, **kwargs)
        self.bcs_var = Variable(value=[])
        bc_scrollbar_y = Scrollbar(self,orient=VERTICAL)
        bc_scrollbar_y.grid(column=1,row=0,sticky=(N,E,S))
        self.bc_list = Listbox(self, justify=LEFT, listvariable=self.bcs_var,
                               yscrollcommand=bc_scrollbar_y.set, selectmode="single")
        # self.bc_list.bind() # Using button to open instead
        self.bc_list.grid(column=0, row=0, sticky=(N,W,S,E))
        bc_scrollbar_y.config(command=self.bc_list.yview)
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)

        # Add container for buttons
        btn_container = self._add_buttons()
        btn_container.grid(column=0, row=1, columnspan=2, sticky=(W,S,E) ,padx=self._btn_padding)
        # self.rowconfigure(1,weight=0)
        
        super().pack(anchor=N, expand=True, fill=BOTH, side=TOP)

    def _add_buttons(self):
        btn_box = Frame(self)
        
        remove_button = Button(btn_box, text="Remove")
        remove_button.pack(side=LEFT, anchor=SW, expand=True, fill=X)
        open_button = Button(btn_box, text="Open")
        open_button.pack(side=RIGHT, anchor=SE, expand=True, fill=X)
        open_button.bind("<ButtonRelease-1>", self._open_btn_handler)
        remove_button.bind("<ButtonRelease-1>", self._remove_btn_handler)
        
        return btn_box
    
    
    def _open_btn_handler(self, event):
        if not len(self.bcs_var.get()) > 0:
            return
        
        # print(self.bc_list.curselection())
        if len(self.bc_list.curselection()):
            selection:int = self.bc_list.curselection()[0]
        else:
            selection:int = 0
        self.parent.open_selected_biomedical_concept(selection)

    def _remove_btn_handler(self, event):
        if not len(self.bcs_var.get()) > 0 or not self.bc_list.curselection():
            print(f"{BColors.OKGREEN}No bcs to select or no bc selected, exiting.{BColors.ENDC}")
            
            return
        
        # print(self.bc_list.curselection())
        if len(self.bc_list.curselection()):
            selection:int = self.bc_list.curselection()[0]
        else:
            selection:int = 0
        
        print(f"{BColors.OKGREEN}index: {selection}{BColors.ENDC}")
        self.parent.set_editor_apply_btn_text("Add")
        self.parent.remove_bc_from_repository(selection)
        temp_var =list(self.bcs_var.get()) #cast to list, since tuples are immutable
        temp_var.pop(selection)
        self.bcs_var.set(temp_var)


    
    def update_biomedical_concepts_list (self, bcs:list[BiomedicalConcept]):
        bc_strings:list[str] = [f"{bc.code.standard_code.code} - {bc.label}" for bc in bcs]
        self.bcs_var.set(bc_strings)


    
    # Add container with list with added BCs
    #   - List(box) / customn listbox
    #       + code                                                          -> Known value (selection/lookup)
    #       + label                                                         -> Known value (selection/lookup)
    #   code + label = btn