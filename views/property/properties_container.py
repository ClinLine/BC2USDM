from tkinter import ttk
from tkinter.constants import *

from views.property.property_frame import PropertyFrame
from views.scroll_frame import ScrollFrame


class PropertiesContainer(ttk.LabelFrame):
    new_prop_btn = None
    
    
    def __init__(self, parent, frame_title:str="Properties:",properties=None, *args, **kwargs):
        super().__init__(parent, text=frame_title)
        
        self.scroll_frame = ScrollFrame(self, False)
        
        self.property_containers = []
        self.notebook = ttk.Notebook(self.scroll_frame.view_port)
        self.notebook.pack(side=TOP, fill=BOTH, expand=True)
        if properties is None:
            properties = []
        for prop in properties:
            main_frame = PropertyFrame(self.scroll_frame.view_port, property=prop, name=f"main_frame_{prop["id_"]}")
            self.property_containers.append(main_frame)
            self.notebook.add(main_frame, text=prop["label"])
        
        self.notebook.add(new_prop:= ttk.Frame(self.scroll_frame.view_port),sticky=E,text="+")
        new_prop.bind("<Expose>", self.create_new_property_frame)
        ttk.Label(new_prop, text=f"Adding new properties has \n not been implemented yet").pack(side=BOTTOM,fill=BOTH,expand=TRUE)
        
        self.scroll_frame.pack(side=TOP, fill=BOTH, expand=True)
        self.scroll_frame._on_post_init()

    def reset(self):
        self.property_containers = []
        print(self.notebook.index(END))
        print ("resetting properties container")
        print(self.notebook.children)

    def add_property(self, *args):
        prop = args[0]
        new_prop_frame = PropertyFrame(self.scroll_frame.view_port, property=prop, name=f"prop_frame+{prop.id_}")
        self.notebook.add(new_prop_frame, sticky=W)
        # set code
        
        # set datatype
        # set id
        # set is_enabled
        # set is_required
        # set label
        # don't set name
        # set notes
        # set reference
        # set response_codes
        for arg in args:
            print(arg)

    def create_new_property_frame(self, event, *args):
        print("Attempting to add new property")
        ...
        # raise NotImplementedError("Adding new properties is not yet implemented")
        
        # new_main_frame = PropertyFrame(self.scroll_frame.view_port, property="""USDM.Property""", name=f"main_frame_new_#")
        # self.notebook.insert(-1,new_main_frame)
