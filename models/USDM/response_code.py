from __future__ import annotations
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
    __IS_ENABLED_DEFAULT_VALUE = True

    # def __init__(self, id_:UUID=None, name:str=None, enabled:bool=False, code:Code=None, label:str=None):
    def __init__(self, id_:UUID=None, name:str=None, is_enabled:bool=__IS_ENABLED_DEFAULT_VALUE, label:str=None, **kwargs):
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
            self.name = f"{label.replace(" ","")}_{self.id_}"
        print(f"{BColors.WARNING}WARN|[ResponseCode].init: Retreiving Code for individual response codes is not supported by cdisc api, setting static 'responsecode' code instead{BColors.ENDC}")
        self.code = R_CODE
        self.is_enabled = is_enabled

        for key  in iter(kwargs):
            if key == "code":
                self.code = kwargs["code"]
        


    @staticmethod
    def from_example_set(example_set:str|list[str], separator=';') -> list[ResponseCode]:
        '''
        response codes:
        Each value in the ExampleSet (delimited by ;) will be a new instance in the responseCode entity. No codes provided.
        '''
        result:list[ResponseCode] = []
        # if example set is a singular string, split it by separator (default =;)
        if isinstance(example_set, str):
            labels = example_set.split(separator)
        #else if example_set is a set of strings
        elif isinstance(example_set, list): #TODO: check if I already split it somewhere, because I'm getting an array of strings (might be done by json lib too)
            labels = example_set
        else:
            raise ValueError()
        # result:list[ResponseCode] = []
        for label in labels:
            result.append(ResponseCode(label=label))
        if result is None:
            raise ValueError("[ResponseCode].from_example_set: result should never be None here!!")
        return result
    
    # def __eq__(self, other):
    #     if not isinstance(other, ResponseCode):
    #         return False
    #     if self.label != other.label: return False
    #     # Not checking code since all response codes should have the same code
    #     if self.is_enabled != other.is_enabled: return False
    #     return True
