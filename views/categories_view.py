from tkinter import Label, LabelFrame, Listbox, Scrollbar, StringVar
from tkinter.constants import *


CATEGORY_LISTBOX_NAME = "category-listbox"

class CategoriesView(LabelFrame):
    category_names:StringVar
    categories_overview_frame:LabelFrame
    TITLE_TEXT:str = "Biomedical Categories:"
    categories_label:Label
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
        The returned tuple has a length of 1 if the listbox's selectmode is set to browse or single.
        """
        # select_mode = self.categories_overview_listbox.__getattribute__("selectMode")
        
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

        if isinstance(selection, tuple) and len(selection) == 0:
            print(f"[CategoriesView._listbox_onclick:] no index found in selection")
            selection = (0,)
            return

        # return [self.parent.main_app.get_biomedical_concept_names_in_category(index) for index in selection][0]
        # return self.parent.main_app.get_biomedical_concept_names_in_category(selection[0])
        # current_cats = [self.parent.main_app.get_biomedical_concept_category_by_index(index) for index in selection]
        self.parent.set_current_category(selection[0])
        self.parent.current_category_container.grab_focus()