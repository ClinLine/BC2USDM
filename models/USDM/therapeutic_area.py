from uuid import UUID, uuid4 as guid

from models.USDM.code import Code

class TherapeuticArea():
    # id_:guid = None => Stored in Code
    code:Code = None
    # INSTANCE_TYPE:str = Code.__qualname__
    __CODE_SYSTEM:str = "CUSTOM"
    __CODE_SYSTEM_VERSION:str = "00"

    def __init__(self, id_:guid=None, code:Code=None, **kwargs):
        
        if id_ is None:
            id_=guid()

        if code is not None:
            self.code = code
        else:
            self.code = Code(code=f"TA_{id_}",
                            id_=id_,
                            code_system=TherapeuticArea.__CODE_SYSTEM,
                            code_system_version=TherapeuticArea.__CODE_SYSTEM_VERSION)
            if self.code is None:
                print(f"Set therapeutic area code to {self.code}, (id={id_})")

        if "decode" in kwargs.keys():
            self.code.decode = kwargs["decode"]
    
    def set_decode(self, value:str=""):
        self.code.decode = value

    def get_decode(self):
        return self.code.decode