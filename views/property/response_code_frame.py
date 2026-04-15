from tkinter import Frame, Label, Entry, Checkbutton
from tkinter import StringVar, IntVar
from tkinter.constants import *

from uuid import uuid4 as guid

class ResponseCodeFrame(Frame):
    rc_index:int # response code index

    # Attributes:
    label_var:StringVar
    id_var:StringVar
    # name_var:StringVar # hidden & inferred
    is_enabled_var:IntVar
    code_var:StringVar


    def __init__(self, parent, response_code=None, index:int=0, *args, **kwargs):
        super().__init__(parent,*args, **kwargs)
        self.response_code=response_code
        self.rc_index = index
        # self.response_code_frame_id = __class__.NOT_SET
        self.create()
        self.pack(side=TOP, fill=BOTH, expand=True)
        self.columnconfigure(index=1, weight=1, uniform=TRUE)
        self.populate(response_code)

    def create(self):
        i:int=0
        self.initialize_vars()

        # Label:
        l_label = Label(self, text="Label:")
        l_label.grid(row=i, column=0, sticky="NSW")
        e_label = Entry(self, textvariable=self.label_var)
        e_label.grid(row=(i:=i+1)-1, column=1, sticky=NSEW)
        
        # Id:
        l_id = Label(self,text="Response code id:")
        l_id.grid(row=i, column=0, sticky="NSW")

        e_id = Entry(self, textvariable=self.id_var, state=DISABLED)
        e_id.grid(row=(i:=i+1)-1, column=1, sticky=NSEW)
        # Code:
        l_code = Label(self, text="Code:")
        l_code.grid(row=i, column=0, sticky="NSW")
        e_code = Entry(self, textvariable=self.code_var)
        e_code.grid(row=(i:=i+1)-1, column=1, sticky=NSEW)

        # Enabled:
        l_enabled = Label(self, text="Enabled:")
        l_enabled.grid(row=i, column=0, sticky="NWS")
        enabled_button = Checkbutton(self, variable=self.is_enabled_var)
        enabled_button.grid(row=(i:=i+1)-1, column=1, sticky="NSW")

    def initialize_vars(self):
        self.id_var = StringVar(value="", )
        self.label_var = StringVar(value="",)
        # self.name_var = StringVar(value="") # inferred
        self.is_enabled_var = IntVar(value=0, )
        self.code_var = StringVar(value="", )

    def populate(self, response_code=None):
        if response_code is not None:
            # Attributes:
            self.label_var.set(response_code.label)
            self.id_var.set(response_code.id_)
            # name_var:StringVar # hidden & inferred
            self.is_enabled_var.set(response_code.is_enabled)
            if response_code.code is not None:
                self.code_var.set(response_code.code.code)
            # TODO Add Code support?
        else:
            self.id_var.set(guid())