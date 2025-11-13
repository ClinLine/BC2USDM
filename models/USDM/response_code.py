from dataclasses import dataclass
from uuid import uuid4 as guid

from models.USDM.code.code import Code


@dataclass
class ResponseCode():
    id_:guid
    name: str
    is_enabled: bool
    code:Code
    label: str = None

    def __init__(self, id_:guid, name:str, enabled:bool, code, label:str=None):
        if id_ is None or id_ == "":
            self.id_ = guid()
        else: self.id_ = id_
        self.name = f"{name}"
        self.label = label
        self.is_enabled = enabled
        if isinstance(code,str):
            self.code = Code(code)
        else: self.code = Code
