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
            self.__init_x(**args[0], **kws)
            # self.__init_from_parameters(**args[0])
        else:
            self.__init_from_parameters(**kws)

    def __init_from_dictionary(self, dictionary:dict):
        self.id_ = guid()
        if "ncitCode" in dictionary:
            self.code = AliasCode(dictionary["ncitCode"])
            if dictionary["ncitCode"] != dictionary["coneptId"]:
                self.code.add_alias(Code(dictionary["coneptId"]))
        self.name = f"{dictionary["shortName"]}_{self.id_}"
        if dictionary["shortName"] is not None and dictionary["label"] != "":
            self.label = dictionary["label"]
        else: self.label = None
        self.is_required = dictionary["isRequired"]
        self.is_enabled = dictionary["isEnabled"]
        self.datatype = dictionary["dataType"]
        # self.code = AliasCode(dictionary["code"])
        # self.notes = CommentAnnotation(dictionary["notes"])
        if "exampleSet" in dictionary:
            # Actual importing those is currently not implenented yet
            self.response_codes = ResponseCode.from_example_set(dictionary["exampleSet"])

    # def __init_from_parameters(self, id_:str, name:str, required:bool, enabled:bool, datatype:str, code:Code, notes:CommentAnnotation, response_codes:ResponseCode, label:str=None):
    def __init_from_parameters(self, name:str, required:bool, enabled:bool, datatype:str, code:Code, notes:CommentAnnotation, response_codes:ResponseCode, label:str=None, conceptId:str=None):
        
        self.id_ = guid()
        self.name = name
        self.label = label
        self.is_required = required
        self.is_enabled = enabled
        self.datatype = datatype
        if code is not None:
            self.code = code
        else:
            self.code = Code(conceptId)
        self.notes = notes
        self.response_codes = response_codes

    def __init_x(self, *args, **kwargs):
        
        if len(args) > 0:
            print("args is not 0")
            raise NotImplementedError()
        for key, value in kwargs.items():
            print(f"{key}:{kwargs[key]}")
            match key:

                case "conceptId":
                    if kwargs["ncitCode"] is not None:
                        if value != kwargs["ncitCode"]:
                            # if ncitCode doesn't match conceptId
                            self.code = AliasCode(standard_code=Code(kwargs["ncitCode"], code_system="ncit"),aliases=[Code(value)])
                        else:
                            self.code = AliasCode(value)

                    self.code = AliasCode(value)
                case "shortName":
                    self.label = value
                case "href":
                    self.reference = value
                case "dataType":
                    self.datatype = value
                case "exampleSet":
                    # map exampleSet to response codes
                    # TODO implement actual ResonseCode support
                    self.response_codes = [ResponseCode(label=rcName) for rcName in value ]
                case _: # One to one mappings
                    try:
                        self.key = value
                    except Exception as e:
                        raise NotImplementedError(f"No exact match found for key:{key}")
                    
            
            
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

