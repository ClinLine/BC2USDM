from dataclasses import field
from dataclasses import dataclass
from uuid import uuid4 as uuid
from utils.utils import Encoding
from utils.api_utils import get_latest_biomedical_concept

@dataclass
class Code():#ResponseCode):
    '''Base class for reference codes used by USDM.
    '''
    # The USDM id for this code
    # code.standardCode.code
    id_:str
    # code.standardCodeAliases.codeSystem
    # string representation of the related code alias
    code:str
    # code.standardCodeAliases.codeSystemVerson
    code_system:str
    code_system_version:str # Not availabe in output

    def __init__(self, id_:str, code:str="", code_system:str="", code_system_version:str=None):
        '''constructor method for the Code dataclass\n
        id_: db id if available</br>
        code: the code associated with the id, will generate as uuidv4 if none is provided<br>
        code_system: the system the alias code originates from, e.g. cdisc code<br>
        code_system_version: Not supported in USDM.BC, so defaults to None
        '''
        if id_ is not None and id_!="":
            self.id_ = id_
        else:
            # No given value for id, generating new ID
            raise ValueError()

        if code is None or code=="":
            self.code = uuid()
        else:
            self.code = code

        if code_system is None or code_system == "":
            self.code_system = "USDM"
        else:
            self.code_system = code_system

        self.code_system_version = code_system_version

    def __decode(self):
        '''Not supported in USDM.BC'''
        raise NotImplementedError(f"Decode currently not avialbe in Biomedical Concept outputs.")

@dataclass
class ResponseCode():
    id_:str
    name: str
    is_enabled: bool
    code:Code
    label: str = ""

    def __init__(self, id_:str, name:str, enabled:bool, code:Code, label:str=""):
        self.id_ = id_
        self.name = name
        self.label = label
        self.is_enabled = enabled
        self.code = code

@dataclass
class AliasCode():
    # db id
    # id_ should not be relevent for the model side, only for id based lookups
    id_:str
    # usdm Code
    standard_code:Code
    # list of codes for all aliases
    standard_code_aliases: list[Code] = field(default_factory=list[Code])

    def __init__(self, id_, standard_code: Code, aliases: list[Code]):
        self.id_ = id_
        self.standard_code = standard_code
        self.standard_code_aliases = aliases

    def add_alias(self, alias:Code):
        '''Append provided alias to alias codes list'''
        self.standard_code_aliases.append(alias)

@dataclass
class CommentAnnotation:
    id_:str
    text:str
    codes: list[Code] = field(default_factory=list['Code'])

    def __init__(self, id_:str, text:str, codes:list[Code]):
        self.id_ = id_
        self.text = text
        self.codes = codes

@dataclass
class BiomedicalConceptProperty:
    id_: str
    name: str
    is_required: bool
    is_enabled: bool
    # TODO: check if datatype can be an enum or hash for optimizing
    datatype: str
    code:AliasCode
    label: str = ""
    notes: list[CommentAnnotation] = field(default_factory=list[CommentAnnotation],)
    response_codes: list[ResponseCode] = field(default_factory=ResponseCode)

    def __init__(self, *args, **kws):
        if isinstance(args[0], dict):
            self.__init_from_parameters(**args[0])
        else:
            self.__init_from_parameters(**kws)

    def __init_from_dictionary(self, dictionary:dict):
        self.id_ = dictionary["id"]
        self.name = dictionary["name"]
        self.label = Encoding.decode(dictionary["name"])
        self.is_required = dictionary["isRequired"]
        self.is_enabled = dictionary["isEnabled"]
        self.datatype = dictionary["datatype"]
        # self.code = AliasCode(dictionary["code"])
        # self.notes = CommentAnnotation(dictionary["notes"])
        self.response_codes = dictionary["responseCodes"]

    def __init_from_parameters(self, id_:str, name:str, required:bool, enabled:bool, datatype:str, code:Code, notes:CommentAnnotation, response_codes:ResponseCode, label:str=""):
        self.id_ = id_
        self.name = name
        self.label = label
        self.is_required = required
        self.is_enabled = enabled
        self.datatype = datatype
        self.code = code
        self.notes = notes
        self.response_codes = response_codes

class BiomedicalConceptBase:
    id_:str
    reference:str
    name:str
    label:str
    type_:str
    _populated:bool
    # parent:type["BiomedicalConceptBase"]


    # # def __init__(self, href:str, title:str, type_:str):
    def __init__(self, *args, **kws):
        # print(self)
        # print(args)
        if isinstance(args[0], dict) and args[0] is not None:
            # initiated from a json string
            self.__init_from_dict(args[0])
        else:
            # parameterised initiation
            self.__init_from_params__(kws["href"], kws["title"], kws["type"])

    def __init_from_dict(self, dict_:dict):
        self.__init_from_params__(dict_["href"], dict_["title"], dict_["type"])

    def __init_from_params__(self, href:str, title:str, type_:str):
        self._populated = False
        self.reference = href
        self.id_ = href.split('/')[-1]
        self.type = type_
        self.label = Encoding.decode(title)
        self.name = f"{title.replace(" ","")}{self.id_}"
        # TODO: 
        #"name": "AspartateAminotransferaseMeasurement"+id_


    

class BiomedicalConcept(BiomedicalConceptBase):
    __name__ = "BiomedicalConcept"
    properties: list[BiomedicalConceptProperty]
    response_codes:list[ResponseCode]
    code:AliasCode
    label:str = ""
    synonyms:list[str] = None
    # reference:str = "" # Not nullable

    # def __call__(self, bc: 'BiomedicalConcept'):
    #     for field_ in bc.fields:
    #         if field_ is not None:
    #             self[field_.name] = bc[field_.name]
    

    # C49676
    '''properties you get from category (CDISC):
    href: i.e. /mdr/bc/biomedicalconcepts/C49676
    title: pH
    type: Biomedical Concept

    properties yo uget from GetLatestBiomedicalConcept (CDISC):
    href: i.e. /mdr/bc/packages/2025-07-01/biomecialconcepts/C45997
    title: ph
    type: Biomedical Concept

    properties you get from getLatestBiomedicalConcept (CDISC):
    "_links": {
        "parentBiomedicalConcept": {
            "href": "/mdr/bc/biomedicalconcepts/C158424",
            "title": "Physical Property",
            "type": "Biomedical Concept"
        },
        "parentPackage": {
            "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts",
            "title": "Biomedical Concept Package Effective 2025-07-01",
            "type": "Biomedical Concept Package"
        },
        "self": {
            "href": "/mdr/bc/biomedicalconcepts/C45997",
            "title": "pH",
            "type": "Biomedical Concept"
        }
    },
    "conceptId": "C45997",
    "href": "https://evsexplore.semantics.cancer.gov/evsexplore/concept/ncit/C45997",
    "categories": ["Laboratory Tests", "Urinalysis"],
    "shortName": "pH",
    "synonyms": ["PH", "potential of Hydrogen"],
    "resultScales": ["Quantitative", "Ordinal"],
    "definition": "Quantity of dimension one used to express on a scale from 0 to 14 the amount-of-substance concentration of hydrogen ion of dilute aqueous solution, calculated as the logarithm of the reciprocal of hydrogen-ion concentration in gram atoms per liter.",
    "dataElementConcepts": [{
        "conceptId": "C70856",
        "href": "https://evsexplore.semantics.cancer.gov/evsexplore/concept/ncit/C70856",
        "shortName": "Observation Result",
        "dataType": "decimal",
        "ncitCode": "C70856"
    }, {
        "conceptId": "C93566",
        "href": "https://evsexplore.semantics.cancer.gov/evsexplore/concept/ncit/C93566",
        "shortName": "Fasting Status Indicator",
        "dataType": "boolean",
        "ncitCode": "C93566"
    }, {
        "conceptId": "C70713",
        "href": "https://evsexplore.semantics.cancer.gov/evsexplore/concept/ncit/C70713",
        "shortName": "Biospecimen Type",
        "dataType": "string",
        "exampleSet": ["Urine", "Blood", "Saliva", "Bronchial Fluid", "Body Fluid", "Eyes", "Skin"],
        "ncitCode": "C70713"
    }, {
        "conceptId": "C82515",
        "href": "https://evsexplore.semantics.cancer.gov/evsexplore/concept/ncit/C82515",
        "shortName": "Collection Date Time",
        "dataType": "datetime",
        "ncitCode": "C82515"
    }],
    "ncitCode": "C45997"'''

    # def __init__(self, id_, name:str, label:str, description:str=None, code=None, notes=None, children=None, *args):
    def __init__(self, *args, **kws):
        if isinstance(args[0], dict) and args[0] is not None:
            # initiated from a json string
            BiomedicalConceptBase.__init__(self,args[0])
        else:
            BiomedicalConceptBase.__init__(self, kws)
            # self.code = AliasCode(kws["code"])
            if kws["properties"] is not None and isinstance(kws["properties"][0], BiomedicalConceptProperty):
                self.properties = kws["properties"]
            else:
                props = []
                for p in kws["properties"]:
                    props.append(BiomedicalConceptProperty(p))
            # propertes: list[BiomedicalConceptProperty]
            # response_codes:list[ResponseCode]
            # code:AliasCode
            # label:str = ""
            # synonyms:list[str] = None


    def populate(self):
        if not self._populated:
            data = get_latest_biomedical_concept(self.id_)
            print(data)
            # properties: list[BiomedicalConceptProperty]
            # response_codes:list[ResponseCode]
            # code:AliasCode
            # synonyms:list[str] = None



    @staticmethod
    def from_json(json):
        '''Function returns a BiomedicalConceptCategory based on a provided json string'''
        return BiomedicalConcept(
            json["id_"],
            json["name"],
            json["label"],
            json["description"])
