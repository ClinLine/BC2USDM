from dataclasses import dataclass, field
from uuid import uuid4 as guid

# from logic.local_storage import LocalStorage
# from models.USDM.BiomedicalConcept import BiomedicalConcept
from models.USDM.code.alias_code import AliasCode
from models.USDM.code.code import Code
from models.USDM.comment_annotation import CommentAnnotation
from models.USDM.response_code import ResponseCode


@dataclass
class BiomedicalConceptProperty:
    id_: guid
    name: str
    is_required: bool
    is_enabled: bool
    # TODO: check if datatype can be an enum or hash for optimizing
    datatype: str
    code:AliasCode
    label: str = None
    notes: list[CommentAnnotation] = field(default_factory=list[CommentAnnotation],)
    response_codes: list[ResponseCode] = field(default_factory=list[ResponseCode])

    def __init__(self, *args, **kws):
        if isinstance(args[0], dict):
            self.__init_from_parameters(**args[0])
        else:
            self.__init_from_parameters(**kws)

    def __init_from_dictionary(self, dictionary:dict):
        self.id_ = dictionary["id"]
        self.name = dictionary["name"]
        if dictionary["label"] is not None and dictionary["label"] != "":
            self.label = dictionary["label"]
        else: self.label = None
        self.is_required = dictionary["isRequired"]
        self.is_enabled = dictionary["isEnabled"]
        self.datatype = dictionary["datatype"]
        # self.code = AliasCode(dictionary["code"])
        # self.notes = CommentAnnotation(dictionary["notes"])
        self.response_codes = dictionary["responseCodes"] # probs fails


    # def __init_from_parameters(self, id_:str, name:str, required:bool, enabled:bool, datatype:str, code:Code, notes:CommentAnnotation, response_codes:ResponseCode, label:str=None):
    def __init_from_parameters(self, name:str, required:bool, enabled:bool, datatype:str, code:Code, notes:CommentAnnotation, response_codes:ResponseCode, label:str=None):
        self.id_ = guid()
        self.name = name
        self.label = label
        self.is_required = required
        self.is_enabled = enabled
        self.datatype = datatype
        self.code = code
        self.notes = notes
        self.response_codes = response_codes

    @staticmethod
    def package_from_json(json):
        return BiomedicalConceptProperty(
            href = json["href"],
            label = json["title"],
            type = "Biomedical Concept Package",
            code = json["href"].split('/')[4],
            datatype = "parentPackage",
            required = True,
        )

