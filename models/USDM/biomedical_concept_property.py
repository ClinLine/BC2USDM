# from dataclasses import dataclass, field
from uuid import UUID, uuid4 as guid

# from logic.local_storage import LocalStorage
# from models.USDM.BiomedicalConcept import BiomedicalConcept
from models.USDM.code import Code
from models.USDM.code.alias_code import AliasCode
from models.USDM.comment_annotation import CommentAnnotation
from models.USDM.response_code import ResponseCode


# @dataclass
class BiomedicalConceptProperty:
    id_: UUID
    name: str
    is_required: bool = False
    is_enabled: bool = False
    # TODO: check if datatype can be an enum or hash for optimizing
    datatype: str
    code:AliasCode
    label: str = None
    notes: list[CommentAnnotation] = None
    response_codes: list[ResponseCode] = None

    def __init__(self, *args, **kwargs):
        self.id_ = guid()
        if isinstance(args[0], dict):
            self.__init_from_dict(**args[0], **kwargs)
        else:
            self.__init_from_parameters(**kwargs)

    def __init_from_parameters(self, name:str, datatype:str, code:Code, notes:CommentAnnotation = None, response_codes:ResponseCode = None, label:str=None, conceptId:str=None, required:bool=False, enabled:bool=False):
        print("init from parameters got used") # TODO: Remove after testing is done
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

    def __init_from_dict(self, *args, **kwargs):
        if len(args) > 0:
            raise NotImplementedError()
        for key, value in kwargs.items():
            match key:
                # TODO: CHECK THIS
                case "conceptId":
                    if kwargs["ncitCode"] is not None:
                        if value != kwargs["ncitCode"]:
                            # if ncitCode doesn't match conceptId
                            self.code = AliasCode(standard_code=Code(kwargs["ncitCode"], code_system="ncit"),aliases=[Code(value)])
                        else:
                            self.code = AliasCode(value)
                    self.code = AliasCode(value)
                case "ncitCode": pass # already handled by conceptId
                case "coding":
                    self.code.add_alias(
                        standard_code=kwargs["coding"]["code"],
                        code_system=kwargs["coding"]["systemName"]
                    )
                case "shortName":
                    self.label = value
                    self.name = f"{value}_{self.id_}"
                case "href":
                    self.reference = value
                case "dataType":
                    self.datatype = value
                case "exampleSet":
                    # map exampleSet to response codes
                    self.response_codes = [ResponseCode(label=rcName) for rcName in value ]
                case "isRequired":
                    self.is_required = bool(value)
                case "isEnabled":
                    self.is_enabled = bool(value)
                case _: # Default case
                    print(f"using default case to map for key: {key}")
                    try:
                        self.key = value
                    except Exception as e: # TODO replace with more specific exception.
                        raise NotImplementedError(f"[{e.__qualname__}]No exact match found for key:{key}")
                    
            
            
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

