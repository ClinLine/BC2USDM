from __future__ import annotations
from utils.b_colors import BColors

from uuid import uuid4 as guid
from uuid import UUID

class Code():
    '''Base class for reference codes used by USDM.
    '''
    #region constants
    
    CustomBiomedicalConceptFlag:str="USDM"
    CustomPropertyFlag:str="USDM"
    CustomCommentAnnotationFlag:str="USDM"
    CustomCategoryFlag:str="USDM"
    # CODE_SYSTEM_CUSTOM:str="CUSTOM"
    DEFAULT_CODE_SYSTEM_VERSION:str="00"
    INSTANCE_TYPE = __qualname__

    class CodeSystem(str):
        CDISC = "http://www.cdisc.org"
        NCIT = "http://www.ncit.org"
        CUSTOM = "CUSTOM"

    #endregion

    # The USDM id for this code
    # code.standardCode.code
    id_:UUID
    # code.standardCodeAliases.codeSystem
    # string representation of the related code alias
    code:str = ""
    # code.standardCodeAliases.codeSystemVerson
    code_system:str = ""
    code_system_version:str = ""
    decode:str = None

    def __init__(self, code:str, id_:str = None, code_system:str="", code_system_version:str=None, decode:str=""):
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
                    # self.code_system = "ncit"
                    self.code_system = self.CodeSystem.NCIT
            elif isinstance(code, Code):
                if code.code[:0] == 'C':
                    # self.code_system = "ncit"
                    self.code_system = self.CodeSystem.NCIT
            else:
                self.code_system = self.CodeSystem.CUSTOM
        else:
            self.code_system = code_system

        if code_system_version == "" or code_system_version is None:
            self.code_system_version = None
        else: self.code_system_version = code_system_version

        self.decode = decode
    
    def decode_setter(self, decode_string: str = None):
        '''
        Docstring for decode_setter
        
        :param self: Self reference to this Code object
        :param decode_string: "Decode description of associated code"
        :type decode_string: str
        '''
        if decode_string is None or "":
            #TODO Add Decode!!
            raise NotImplementedError("Looking up decode with api is not yet supported.")
        self.decode = decode_string
        return self
    
    @staticmethod
    def get_version_from_reference(reference:str):
        """
        (static) Method returning <code>code_system_version</code> baised on package version in reference string
            :param reference: reference string - version source 
            :type reference: str
            :return output: extracted version
            :output: str
            :raises ValueError: Raise value error when reference does not include substring 'packages'

        """
        version_index = None
        substrings = reference.split('/')
        if substrings[1] == 'mdr': # Test if CDISC reference
            for index, substring in enumerate(substrings):
                if substring == "packages":
                    version_index = index + 1
                    break
        elif substrings[2] == 'evsexplore.semantics.cancer.gov': # If NCIT Link
            print(f"{BColors.WARNING} Unable to extract package number from ncit reference{BColors.ENDC} \n Is this a property?")
            return None
        if version_index is None:
            raise ValueError(f"{BColors.FAIL} Excpected to find package version in reference.{BColors.ENDC}")
        return substrings[version_index]
    
    # def __str__(self):
    #     return self.decode

    def __eq__(self, value):
        # Skipping id since it can't be modified by the user
        if self.code != value.code: return False
        if self.code_system != value.code: return False
        if self.decode != value.decode: return False
        return True

    # def __repr__(self):
    #     id_substring = f"{"id"}:{type(self.id_)}={self.id_}"
    #     # self.__class__.code.__qualname__
    #     code_substring = f"'code':{type(self.code)}={self.code}"
    #     code_system_substring = f"code_system:{type(self.code_system)}={self.code_system}"
    #     code_system_version_substring = f"code_system_version:{type(self.code_system_version)}={self.code_system_version}"
    #     decode_substring = f"decode:{type(self.decode)}={self.decode}"
    #     return f"Code({id_substring}, {code_substring}, {code_system_substring}, {code_system_version_substring}, {decode_substring})"
    
#TODO Set code_system_versions & decodes for constants
DEFINITION:Code = Code("C43680", code_system=Code.CodeSystem.NCIT, code_system_version="2009-11-23",decode="Definition")
RESULT_SCALE:Code = Code("C221799", code_system=Code.CodeSystem.NCIT, code_system_version="2026-02-23",decode="Result scale")
Example:Code = Code(code="C48175", code_system=Code.CodeSystem.NCIT, code_system_version="2009-11-23", decode="Example")
RESPONSE_CODE:Code = Code(code="C201347", code_system=Code.CodeSystem.CDISC, code_system_version="2024-04-29", decode="A symbol or combination of symbols representing the response to the question.")
Error:Code = Code(code="C43369", code_system=Code.CodeSystem.NCIT, code_system_version="2009-11-23",decode='Error')
SOFTWARE_RUNTIME_ERROR:Code = Code(
    code="C92115",
    code_system=Code.CodeSystem.NCIT,
    code_system_version="2013-06-24")
APPROVAL_DATE:Code = Code(
    code="C132352",
    code_system=Code.CodeSystem.CDISC,
    code_system_version="2025-09-29").decode_setter("Sponsor Approval Date")
