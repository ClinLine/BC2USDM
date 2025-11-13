from uuid import uuid4 as guid


# @dataclass
class Code():
    '''Base class for reference codes used by USDM.
    '''
    # The USDM id for this code
    # code.standardCode.code
    id_:guid
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
            raise ValueError()
        else:
            self.code = code

        if code_system is None or code_system == "":
            self.code_system = "USDM"
        else:
            self.code_system = code_system

        if code_system_version == "" or code_system_version is None:
            code_system_version = None
        else: self.code_system_version = code_system_version

    def __decode(self):
        '''Not supported in USDM.BiomedicalConcept'''
        raise NotImplementedError("Decode currently not avialbe in Biomedical Concept outputs.")
    