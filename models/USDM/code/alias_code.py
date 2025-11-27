# @dataclass
from dataclasses import dataclass
from dataclasses import field
from uuid import uuid4 as guid

from models.USDM.code.code import Code
# from models.USDM.code.code import Code



@dataclass
class AliasCode():
    # usdm_id (guid)
    # id_ should not be relevent for the model side, only for id based lookups
    id_:guid
    # ncit Code
    standard_code:Code
    # list of codes for all aliases
    standard_code_aliases: list[Code] = field(default_factory=list[Code])

    def __init__(self, standard_code, id_=None, aliases: list[Code] = None):
        if(isinstance(id_, str)):
            print(id_)
        if id_ is None or id_ == "":
            self.id = guid()
        else: self.id_ = id_
        if isinstance(standard_code, str):
            self.standard_code = Code(code=standard_code, code_system="ncit")
        else: self.standard_code = standard_code
        self.standard_code_aliases = aliases

    def add_alias(self, alias:Code):
        '''Append provided alias to alias codes list'''
        self.standard_code_aliases.append(alias)
