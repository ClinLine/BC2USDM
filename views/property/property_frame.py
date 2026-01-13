from tkinter import *
from uuid import uuid4 as guid
from tkinter import ttk

from views.property.notes_frame import NotesFrame
from views.property.response_codes_container_frame import ResponseCodesContainerFrame




class PropertyFrame(Frame):
    def __init__(self, parent, property = {}, *args, **kwargs):
        super().__init__(parent, name=kwargs["name"])
        row_index = 0

        # Property Label
        label_var = StringVar(value=property["label"])
        Label(self,text="Property:").grid(row=row_index,column=0,sticky="NWS")
        # Note: (i:=i+1)-1 equates to i++ in c-like languages (++i would be (i:=i+1))
        Entry(self,textvariable=label_var).grid(row=(row_index:=row_index+1)-1,column=1,sticky="NESW")

        # Property Id
        id_var = StringVar(value=property["id_"])
        Label(self,text="Property Id:").grid(row=row_index,column=0,sticky="NWS")
        Entry(self, state=DISABLED, textvariable=id_var).grid(row=(row_index:=row_index+1)-1,column=1,sticky="NESW")
        
        # Property Code
        id_var = StringVar(value=property["code"])
        Label(self,text="Code:").grid(row=row_index,column=0,sticky="NWS")
        Entry(self, state=DISABLED, textvariable=id_var).grid(row=(row_index:=row_index+1)-1,column=1,sticky="NESW")

        # isRequired
        Label(self,text="Required").grid(row=row_index,column=0,sticky="NWS")
        required_btn = Checkbutton(self)
        self.required_var = BooleanVar(master=required_btn, value=property["isRequired"])
        # self.required_properties_vars.append(required_var)
        required_btn.configure(variable=self.required_var)
        required_btn.grid(row=(row_index:=row_index+1)-1,column=1,sticky="NSW")

        # isEnabled
        Label(self,text="Enabled").grid(row=row_index,column=0,sticky="NWS")
        enabled_button = Checkbutton(self, name=f"!property_enabled_cbtn_{str(property["id_"]).replace("-","_")}")
        self.enabled_var = BooleanVar(master=enabled_button, value=property["isEnabled"])
        # self.enabled_properties_vars.append(enabled_var)
        enabled_button.configure(variable=self.enabled_var)
        enabled_button.grid(row=(row_index:=row_index+1)-1, column=1, sticky="NSW")

        # Property data-type
        label_var = StringVar(value=property["dataType"])
        Label(self,text="Data-type:").grid(row=row_index,column=0,sticky="NWS")
        Entry(self,textvariable=label_var).grid(row=(row_index:=row_index+1)-1,column=1,sticky="NESW")

        self.pack(side=TOP, fill=BOTH, expand=TRUE)

        # Property Notes
        notes_frame = NotesFrame(self, notes=property["notes"])
        notes_frame.grid(row=(row_index:=row_index+1)-1, column=0, columnspan=2, sticky=NSEW)
        # prop_window.add(notes_frame)

        # Property Response Codes:
        response_code_frame = ResponseCodesContainerFrame(self, response_codes=property["responseCode"])
        response_code_frame.grid(row=(row_index:=row_index+1)-1, column=0, columnspan=2, sticky=NSEW)

        self.columnconfigure(1,weight=1)


