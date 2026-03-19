from tkinter import Label, LabelFrame, Listbox, Scrollbar, StringVar
from tkinter.constants import *

from views.categories_view import CategoriesView


class CurrentCategoryView(LabelFrame):
    biomedical_concepts_in_category:StringVar
    TITLE_TEXT:str = "BCs in Category:"

    def __init__(self, parent,  width, x, **kwargs):
        self.parent = parent
        if "title" in kwargs.keys():
            title = kwargs["title"]
        else:
            title = CurrentCategoryView.TITLE_TEXT
        self.view_title:StringVar = StringVar(value=title)
        self.frame_label = Label(parent.root, textvariable=self.view_title, justify="left", anchor=N)
        super().__init__(parent.root, text=title, labelwidget=self.frame_label, labelanchor="nw",**kwargs)
        
        self.biomedical_concepts_in_category = StringVar(value=None)

        # self.active_category_overview_lframe = ttk.LabelFrame(self,text=title)
        self.place(anchor="nw", relheight=1, width=width, x=x)
        self.active_category_overview_listbox = Listbox(self, listvariable=self.biomedical_concepts_in_category, name="activeCat-listbox")
        self.active_category_overview_scrollbarX = Scrollbar(self, orient=HORIZONTAL)
        self.active_category_overview_scrollbarX.config(command=self.active_category_overview_listbox.xview)
        self.active_category_overview_listbox.configure(xscrollcommand=self.active_category_overview_scrollbarX.set)
        self.active_category_overview_scrollbarY = Scrollbar(self, orient=VERTICAL)
        self.active_category_overview_scrollbarY.config(command=self.active_category_overview_listbox.yview)
        self.active_category_overview_listbox.configure(yscrollcommand=self.active_category_overview_scrollbarY.set)
        self.active_category_overview_listbox.bind("<<ListboxSelect>>", self.bind_activeCat_onclick)

        self.active_category_overview_scrollbarX.pack(side=BOTTOM,fill=X,in_=self)
        self.active_category_overview_scrollbarY.pack(side=RIGHT,fill=Y,in_=self)
        self.active_category_overview_listbox.pack(anchor="nw",expand=True,side="left",fill="both")
        

    def update_current_category(self, cat_name:str=None, bc_names=None):
        if cat_name is not None and cat_name != "":
            self.view_title.set(f"{CategoriesView.TITLE_TEXT[:-1]}\n{cat_name}:")
        else:
            self.view_title.set(f"{CategoriesView.TITLE_TEXT}")
        self.biomedical_concepts_in_category.set(bc_names)


    # Called in runtime?!
    def bind_activeCat_onclick(self, event, **kwargs):
        self.listbox_onclick(event, **kwargs)

    def listbox_onclick(self, event, **kwargs):
        selection = event.widget.curselection()
        # Lose focus of this listbox
        self.parent.root.focus()

        if len(selection) == 0 and isinstance(selection,tuple):
            # Don't do anything if listbox is empty
            return

        temp_bc = self.parent.main_app.select_bc(selection[0])
        
        self.parent.update_current_bc(temp_bc)
        

    def grab_focus(self):
        self.active_category_overview_listbox.activate(0)

    def set_current_category(self, index:int):
        current_cat = self.parent.main_app.get_category_by_index(index)
        self.view_title.set(f"Current Category: {current_cat.label}")
        self.biomedical_concepts_in_category.set([child.label for child in current_cat.children])
        # TODO: only add current category to active categories list