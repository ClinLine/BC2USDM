from tkinter import *
from uuid import UUID, uuid4 as guid
from tkinter import ttk

from views.notes_frame import NotesFrame
from views.property.response_codes_container_frame import ResponseCodesContainerFrame




class PropertyFrame(Frame):
    def __init__(self, parent, property = None, *args, **kwargs):
        
        super().__init__(parent, name=kwargs["name"])
        row_index = 0

        # Property Label
        self.label_var = StringVar(value=property.label)
        Label(self,text="Property:").grid(row=row_index,column=0,sticky="NWS")
        # Note: (i:=i+1)-1 equates to i++ in c-like languages (++i would be (i:=i+1))
        Entry(self,textvariable=self.label_var).grid(row=(row_index:=row_index+1)-1,column=1,sticky="NESW")

        # Property Id
        self.id_var = StringVar(value=property.id_)
        Label(self,text="Property Id:").grid(row=row_index,column=0,sticky="NWS")
        Entry(self, state=DISABLED, textvariable=self.id_var).grid(row=(row_index:=row_index+1)-1,column=1,sticky="NESW")
        
        # Property Code
        self.code_var = StringVar(value=property.code.standard_code.code)
        Label(self,text="Code:").grid(row=row_index,column=0,sticky="NWS")
        Entry(self, state=DISABLED, textvariable=self.code_var).grid(row=(row_index:=row_index+1)-1,column=1,sticky="NESW")

        # isRequired
        Label(self,text="Required").grid(row=row_index,column=0,sticky="NWS")
        required_btn = Checkbutton(self)
        self.required_var = BooleanVar(master=required_btn, value=property.is_required)
        # self.required_properties_vars.append(required_var)
        required_btn.configure(variable=self.required_var)
        required_btn.grid(row=(row_index:=row_index+1)-1,column=1,sticky="NSW")

        # isEnabled
        Label(self,text="Enabled").grid(row=row_index,column=0,sticky="NWS")
        enabled_button = Checkbutton(self, name=f"!property_enabled_cbtn_{str(property.id_).replace("-","_")}")
        self.enabled_var = BooleanVar(master=enabled_button, value=property.is_enabled)
        # self.enabled_properties_vars.append(enabled_var)
        enabled_button.configure(variable=self.enabled_var)
        enabled_button.grid(row=(row_index:=row_index+1)-1, column=1, sticky="NSW")

        # Property data-type
        self.type_var = StringVar(value=property.datatype)
        Label(self,text="Data-type:").grid(row=row_index,column=0,sticky="NWS")
        Entry(self,textvariable=self.type_var).grid(row=(row_index:=row_index+1)-1,column=1,sticky="NESW")

        self.pack(side=TOP, fill=BOTH, expand=TRUE)

        # Property Notes
        self.notes_frame = NotesFrame(self, notes=property.notes)
        self.notes_frame.grid(row=(row_index:=row_index+1)-1, column=0, columnspan=2, sticky=NSEW)
        # prop_window.add(notes_frame)

        # Property Response Codes:
        self.response_code_frame = ResponseCodesContainerFrame(self, response_codes=property.response_codes)
        self.response_code_frame.grid(row=(row_index:=row_index+1)-1, column=0, columnspan=2, sticky=NSEW)

        self.columnconfigure(1,weight=1)

    def get_property_dict(self):
        label = self.label_var.get()
        id_:UUID = self.id_var.get()
        code = self.code_var.get()
        required = self.required_var.get()
        enabled = self.enabled_var.get()
        instance_type = self.type_var.get()
        notes = self.notes_frame.get_notes()
        response_codes = self.response_code_frame.get_response_codes()

        prop = {
            "label":label,
            "id_":id_,
            "code":code,
            "is_required":required,
            "is_enabled":enabled,
            "datatype":instance_type,
            "notes":notes,
            "response_codes":response_codes,
        }

        return prop



