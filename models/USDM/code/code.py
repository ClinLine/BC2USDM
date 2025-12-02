from uuid import uuid4 as guid
from uuid import UUID


# @dataclass
class Code():
    '''Base class for reference codes used by USDM.
    '''
    # The USDM id for this code
    # code.standardCode.code
    id_:UUID
    # code.standardCodeAliases.codeSystem
    # string representation of the related code alias
    code:str
    # code.standardCodeAliases.codeSystemVerson
    code_system:str
    code_system_version:str # Not availabe in output

    def __init__(self, code:str, id_:str = None, code_system:str="", code_system_version:str=None):
        '''constructor method for the Code dataclass\n
        id_: USDM identifier (uuid4 format)</br>
        code: the code associated with the id, raises a ValueError if none is provided<br>
        code_system: the system the alias code originates from, e.g. ncit code<br>
        code_system_version: Not supported in USDM.BC, so defaults to None
        '''
        if id_ is not None and id_!="":
            self.id_ = id_
        else:
            # No given value for id, generating new ID
            # raise ValueError()
            self.id_ = guid()

        if code is None or code=="":
            # self.code = uuid()
            raise ValueError("No value for Code was provided")
        elif not isinstance(code, str):
            raise TypeError("The arguement code should be of type str")
        else:
            self.code = code

        if code_system is None or code_system == "":
            if isinstance(code, str):
                if code[:0] == 'C':
                    self.code_system = "ncit"
            elif isinstance(code, Code):
                if code.code[:0] == 'C':
                    self.code_system = "ncit"
            else:
                self.code_system = "USDM"
        else:
            self.code_system = code_system

        if code_system_version == "" or code_system_version is None:
            self.code_system_version = None
        else: self.code_system_version = code_system_version

    def __decode(self):
        '''Not supported in USDM.BiomedicalConcept'''
        raise NotImplementedError("Decode currently not avialbe in Biomedical Concept outputs.")
    
    # def __str__(self):
    #     result = "{"
    #     if self.id_ is not None:
    #         result += f"\n\r\t\"id\":\"{str(self.id_)}\","
        
    #     if self.code is not None:
    #         result +=f"\n\r\t\"code\":\"{self.code}\","
    #     if self.code_system is not None:
    #         result +=f"\n\r\t\"codeSystem\":\"{self.code_system}\","
    #     if self.code_system_version is not None:
    #         # Should never occur, since self.code_system should always be None in this verison
    #         result +=f"\n\r\t\"codeSystemVersion\":\"{self.code_system_version}\","
    #     result = result[:-2]
    #     result +="\n\r}"

    #     return result

DEFINITION:Code = Code("C43680", code_system="ncit", code_system_version=None)
RESULT_SCALE:Code = Code("C221799", code_system="ncit", code_system_version=None)
Example:Code = Code(code="C48175", code_system="ncit", code_system_version=None)
Error:Code = Code(code="C43369", code_system="ncit", code_system_version=None)
SOFTWARE_RUNTIME_ERROR = Code(code="C92115", code_system="ncit", code_system_version=None)
