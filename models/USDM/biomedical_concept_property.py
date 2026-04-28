from __future__ import annotations
from uuid import UUID, uuid4 as guid

# from logic.local_storage import LocalStorage
# from models.USDM.BiomedicalConcept import BiomedicalConcept


# from ...app import App
from models.CDISC import AttributeNames as CDISC_Attributes
from models.DTOs import DataElementConceptDTO
from models.USDM import AttributeNames as USDM_Attributes
from models.USDM.code import Code
from models.USDM.code.alias_code import AliasCode
from models.USDM.comment_annotation import CommentAnnotation
from models.USDM.response_code import ResponseCode
from utils.b_colors import BColors


class BiomedicalConceptProperty:
    id_: UUID
    name: str
    _IS_REQUIRED_DEFAULT = True
    is_required: bool = _IS_REQUIRED_DEFAULT
    _IS_ENABLED_DEFAULT = True
    is_enabled: bool = _IS_ENABLED_DEFAULT
    # TODO: check if datatype can be an enum or hash for optimizing
    datatype: str
    INSTANCE_TYPE = __qualname__
    code:AliasCode
    label: str = None
    notes: list[CommentAnnotation] = None
    response_codes: list[ResponseCode] = None

    def __init__(self, *args,
                    id_:UUID|str = None,
                    label:str = None,
                    name:str=None,
                    is_required:bool = _IS_REQUIRED_DEFAULT,
                    is_enabled:bool = _IS_ENABLED_DEFAULT,
                    datatype:str = None,
                    response_codes: list[ResponseCode]=None,
                    code:AliasCode = None,
                    notes:list[CommentAnnotation] = None,
                    data_element_concept:DataElementConceptDTO= None,
                    parent_bc_id:UUID = None,
                    **kwargs):
        
        if len(args)> 0:
            raise ValueError(f"{BColors.FAIL}[Error]:BiomedicalConceptProperty.init: args can't be > 0{BColors.ENDC}")
        if len(kwargs) > 0:
            for key, value in kwargs:
                print(f"{BColors.FAIL}[Error]:BiomedicalConceptProperty.init: Attribute {key} not found.{BColors.ENDC}")

        if data_element_concept:
            temp_prop = BiomedicalConceptProperty.from_data_element_concept(data_element_concept)
            try:
                self.id_=temp_prop.id_
                self.label=temp_prop.label
                self.name = f"{self.label.replace(" ","")}_{self.id_}"
                self.is_required=temp_prop.is_required
                self.is_enabled=temp_prop.is_enabled
                self.datatype=temp_prop.datatype
                self.response_codes=temp_prop.response_codes
                self.code=temp_prop.code
                self.notes=temp_prop.notes
            except (ValueError,TypeError, AttributeError) as err:
                print(f"{BColors.WARNING}ERROR|[BiomedicalConceptPRoperty].init: {err}{BColors.ENDC}")
                raise err
        else:
            if id_ is not None:
                if isinstance(id_, str):
                    self.id_ = UUID(id_)
                elif isinstance(id_, (UUID)):
                    self.id_ = id_
                else:
                    self.id_ = guid()

            if label:
                self.label = label
            
            self.name = f"{self.label.replace(" ","")}_{self.id_}"
            self.is_required = is_required
            self.is_enabled= is_enabled
            self.datatype = datatype
            if response_codes and len(response_codes)> 0 and isinstance(response_codes[0], ResponseCode):
                self.response_codes = response_codes
            else:
                if response_codes:
                    for key, value in response_codes:
                        print(f"[USDM.BiomedicalConceptProperty]: response code: {key}={value}")
                else:
                    self.response_codes = None
            if code and isinstance(code, AliasCode):
                self.code = code
            elif code and isinstance(code, str) and parent_bc_id:
                # Naïve fix, needs rework
                self.code = AliasCode(
                    Code(
                        code=code, code_system=Code.CodeSystem.CDISC,code_system_version=None,decode=self.label
                    )
                )
                # code = DataStore.lookup_property_code(parent_bc_id, code)
            else:
                raise ValueError("Code must be of type {AliasCode.__qualname__} or a parent ID must be provided")
                # self.code = AliasCode(
                #         standard_code=Code(
                #                 code["code"]),
                #         id_=,
                #         aliases=
                #         decode=self.label)
            self.notes = notes

    # def __init_from_parameters(self, name:str, datatype:str, code:Code, notes:CommentAnnotation = None, response_codes:ResponseCode = None, label:str=None, conceptId:str=None, required:bool=False, enabled:bool=False):
    #     print("init from parameters got used") # TODO: Remove after testing is done
    #     self.id_ = guid()
    #     self.name = name
    #     self.label = label
    #     self.is_required = required
    #     self.is_enabled = enabled
    #     self.datatype = datatype
    #     if code is not None:
    #         self.code = code
    #     else:
    #         self.code = Code(conceptId)
    #     self.notes = notes
    #     self.response_codes = response_codes

    def __init_from_dict(self, id_:UUID, dict_:dict, **kwargs):
        self.id_=id_
        self.label = dict_[USDM_Attributes.BiomedicalConcept.Propety.label]
        self.is_required = dict_[USDM_Attributes.BiomedicalConcept.Propety.is_required]
        self.is_enabled = dict_[USDM_Attributes.BiomedicalConcept.Propety.is_enabled]
        self.datatype = dict_[USDM_Attributes.BiomedicalConcept.Propety.data_type]
        self.response_codes= dict_[USDM_Attributes.BiomedicalConcept.Propety.response_codes]
        self.code = dict_[USDM_Attributes.BiomedicalConcept.Propety.code]
        self.notes = dict_[USDM_Attributes.BiomedicalConcept.Propety.notes]
        
       
    @staticmethod            
    def from_data_element_concept(dec:DataElementConceptDTO):
        id_ = guid()
        label = dec.label
        name = f"{label}_{id_}"
        is_required = BiomedicalConceptProperty._IS_REQUIRED_DEFAULT
        is_enabled = BiomedicalConceptProperty._IS_ENABLED_DEFAULT
        reference = dec.href
        data_type=dec.data_type

        if dec.concept_id != dec.ncit_code:
            code:AliasCode = AliasCode(
                standard_code=Code(
                    code=dec.concept_id,
                    id_=None,
                    code_system=Code.CodeSystem.CDISC,
                    code_system_version=Code.get_version_from_reference(reference),
                    decode=label),
                id_=None,
                aliases=[Code(
                    code=dec.ncit_code,
                    id_=None,
                    code_system=Code.CodeSystem.NCIT,
                    code_system_version=Code.get_version_from_reference(reference),
                    decode=label)])
        else:
            code:AliasCode = AliasCode(
                standard_code=Code(
                    code=dec.concept_id,
                    id_=None,
                    code_system=Code.CodeSystem.CDISC,
                    code_system_version=Code.get_version_from_reference(reference),
                    decode=label),
                id_=None)
        notes:list[CommentAnnotation] = []
        if dec.example_set is not None:
            response_codes = ResponseCode.from_example_set(dec.example_set)
        else:
            response_codes = None
        
        return BiomedicalConceptProperty(
            id_=id_,
            label=label,
            name=name,
            is_required=is_required,
            is_enabled=is_enabled,
            datatype=data_type,
            response_codes=response_codes,
            code=code,
            notes=notes)
    
    @staticmethod
    def package_from_json(json):
        return BiomedicalConceptProperty(
            href = json[CDISC_Attributes.BiomedicalConcept.reference],
            label = json["title"],
            type = "BiomedicalConceptProperty",
            code = json["href"].split('/')[4],
            datatype = "parentPackage",
            # required = True,
        )
    
    def has_same_values(self, other:BiomedicalConceptProperty) -> bool:
        ''' Check if the values of two BiomedicalConceptProperty instances match
        '''
        if isinstance(other, BiomedicalConceptProperty):
            if (
                self.id_ != other.id_
                or self.label != other.label
                or self.is_enabled != other.is_enabled
                or self.is_required != other.is_required
                or self.code != other.code
                or self.datatype != other.datatype
                or self.notes.difference(other.notes) == []
                or self.response_codes.difference(other.response_codes) == []
            ):
                return False
            return True
        return False