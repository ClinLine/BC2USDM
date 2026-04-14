# from dataclasses import dataclass
from uuid import UUID, uuid4 as guid

from models.USDM.code import Code, RESPONSE_CODE as R_CODE
from utils.b_colors import BColors


class ResponseCode():
    id_:UUID
    name: str
    is_enabled: bool
    code:Code = R_CODE
    label: str = None
    INSTANCE_TYPE = __qualname__

    # def __init__(self, id_:UUID=None, name:str=None, enabled:bool=False, code:Code=None, label:str=None):
    def __init__(self, id_:UUID=None, name:str=None, enabled:bool=False, label:str=None):
        if id_ is None:
            self.id_ = guid()
        elif isinstance(id_,str):
            self.id_ = UUID(id)
        elif isinstance(id_, UUID):
            self.id_=id_
        self.label = label
        if name:
            self.name = name
        else:
            self.name = f"{label}_{self.id_}"
        print(f"{BColors.WARNING}WARN|[ResponseCode].init: Retreiving Code for individual response codes is not supported by cdisc api, setting static 'responsecode' code instead{BColors.ENDC}")
        self.code = R_CODE 
        self.is_enabled = enabled

    @staticmethod
    def from_example_set(json_str:str|list[str]):
        '''
        response codes:
        Each value in the ExampleSet (delimited by ;) will be a new instance in the responseCode entity. No codes provided.
        '''
        if isinstance(json_str, str):
            labels = json_str.split(';')
        elif isinstance(json_str, list): #TODO: check if I already split it somewhere, because I'm getting an array of strings (might be done by json lib too)
            labels = json_str
        else:
            raise ValueError()
        result:list[ResponseCode] = []
        for label in labels:
            result.append(ResponseCode(label=label))
        return result
    
    def __eq__(self, other):
        if self.label != other.label: return False
        # Not checking code since all response codes should have the same code
        if self.is_enabled != other.is_enabled: return False
        return True
