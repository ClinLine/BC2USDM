from tkinter import *
from tkinter import ttk

from models.CDISC.BiomedicalConceptCategory import BiomedicalConceptCategory as CDISC_Category
from models.USDM.BiomedicalConceptCategory import BiomedicalConceptCategory as USDM_Category
from utils.api_utils import get_latest_biomedical_concept_categories


__application_title: str = "Biomedical Concept selection Tool"
__default_height: int = 500
__default_width: int = 400



root = Tk()
root.title(__application_title)

mainframe = ttk.Frame(root, height=__default_height, width=__default_width, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

json_categories = get_latest_biomedical_concept_categories()

cdisc_categories:list[CDISC_Category] = CDISC_Category.categories_from_json(json_categories)
usdm_categories:list[USDM_Category] = list(map(USDM_Category.from_cdisc_category, cdisc_categories))
# print(usdm_categories)

found_categories = usdm_categories
found_categories.sort(key=lambda usdm_category: usdm_category.name)

categories_frame=ttk.Frame(mainframe)
categories_frame.grid(column=0,row=0,sticky=(N,W,S,E))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0,weight=1)
categories_frame.columnconfigure(0, weight=1)
categories_frame.rowconfigure(0,weight=0)
categories_frame.rowconfigure(1,weight=1)

categories = StringVar(value=found_categories)
categories_listbox = Listbox(categories_frame, listvariable=categories)
categories_listbox.grid(column=0, row=1, sticky=(N,W,S,E))
categories_listbox.columnconfigure(0,weight=1)
ttk.Label(categories_frame, text="BC Categories:").grid(column=0, row=0, sticky=(N,W))

def on_add(*args):
    try:
        value=Listbox.curselection(categories_listbox)
        selection.append(found_categories[value[0]])
        del found_categories[value[0]]
        # print(found_categories[value[0]])
        selected_categories.set(selection)
    except ValueError:
        pass

def on_print(*args):
    try:
        indeces = Listbox.curselection(categories_listbox)
        print(found_categories[indeces[0]])
    except ValueError:
        pass

btn_frame = ttk.Frame(mainframe)
btn_frame.grid(column=1, row=0)
test = StringVar(value="")
add_btn = ttk.Button(btn_frame, text=">>", command=on_add)
add_btn.grid(column=1,row=0, sticky=(N,S))
print_btn = ttk.Button(btn_frame, text="print", command=on_print)
print_btn.grid(column=1,row=1, sticky=(N,S))

# print_btn = ttk.Button(btn_frame, text="print", textvariable=Listbox.curselection(categories_listbox),command=on_print)

selection = []
selected_categories = StringVar(value=selection)
selection_frame = ttk.Frame(mainframe)
selection_frame.grid(column=2, row=0, sticky=(N,W,S,E))
selection_label = ttk.Label(selection_frame, text="Selected Categories")
selection_label.grid(column=0, row=0, sticky=(N,E))
selection_listbox = Listbox(selection_frame, listvariable=selected_categories)
selection_listbox.grid(column=0, row=1, sticky=(N,E,S))
mainframe.columnconfigure(2,weight=1)
selection_listbox.columnconfigure(0,weight=1)



root.mainloop()