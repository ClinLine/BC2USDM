from uuid import UUID, uuid4 as guid

from models.USDM.biomedical_concept_property import BiomedicalConceptProperty
from models.USDM.code import code
from models.USDM.code.code import Code
from models.USDM.comment_annotation import CommentAnnotation
from models.USDM.response_code import ResponseCode
from models.USDM.code.alias_code import AliasCode
from utils.utils import Encoding
from utils.api_utils import get_latest_biomedical_concept

class BiomedicalConceptBase:
    id_:UUID
    reference:str
    name:str
    label:str
    code:AliasCode
    # type_:str
    _populated:bool = False
    category=None
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

    # def __init_from_params__(self, href:str, title:str, type_:str, package=None):
    def __init_from_params__(self, href:str, title:str, package=None):
        self._populated = False
        self.reference = href
        self.code = AliasCode(href.split('/')[-1])
        self.id_ = guid() # TODO: Request guid from local storage
        # self.type = type_
        self.label = Encoding.decode(title)
        self.name = f"{title.replace(" ","")}_{self.id_}"
        # TODO:
        #"name": "AspartateAminotransferaseMeasurement"+id_


class BiomedicalConcept(BiomedicalConceptBase):
    __name__ = "BiomedicalConcept"
    properties: list[BiomedicalConceptProperty]
    response_codes:list[ResponseCode]
    code:AliasCode
    label:str = None
    synonyms:list[str] = None
    reference:str = "" # Not nullable
    notes:list[CommentAnnotation] = None

    # def __call__(self, bc: 'BiomedicalConcept'):
    #     for field_ in bc.fields:
    #         if field_ is not None:
    #             self[field_.name] = bc[field_.name]
    

    # C49676
    # '''properties you get from category (CDISC):
    # href: i.e. /mdr/bc/biomedicalconcepts/C49676
    # title: pH
    # type: Biomedical Concept

    # properties yo uget from GetLatestBiomedicalConcept (CDISC):
    # href: i.e. /mdr/bc/packages/2025-07-01/biomecialconcepts/C45997
    # title: ph
    # type: Biomedical Concept

    # properties you get from getLatestBiomedicalConcept (CDISC):
    # "_links": {
    #     "parentBiomedicalConcept": {
    #         "href": "/mdr/bc/biomedicalconcepts/C158424",
    #         "title": "Physical Property",
    #         "type": "Biomedical Concept"
    #     },
    #     "parentPackage": {
    #         "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts",
    #         "title": "Biomedical Concept Package Effective 2025-07-01",
    #         "type": "Biomedical Concept Package"
    #     },
    #     "self": {
    #         "href": "/mdr/bc/biomedicalconcepts/C45997",
    #         "title": "pH",
    #         "type": "Biomedical Concept"
    #     }
    # },
    # "conceptId": "C45997",
    # "href": "https://evsexplore.semantics.cancer.gov/evsexplore/concept/ncit/C45997",
    # "categories": ["Laboratory Tests", "Urinalysis"],
    # "shortName": "pH",
    # "synonyms": ["PH", "potential of Hydrogen"],
    # "resultScales": ["Quantitative", "Ordinal"],
    # "definition": "Quantity of dimension one used to express on a scale from 0 to 14 the amount-of-substance concentration of hydrogen ion of dilute aqueous solution, calculated as the logarithm of the reciprocal of hydrogen-ion concentration in gram atoms per liter.",
    # "dataElementConcepts": [{
    #     "conceptId": "C70856",
    #     "href": "https://evsexplore.semantics.cancer.gov/evsexplore/concept/ncit/C70856",
    #     "shortName": "Observation Result",
    #     "dataType": "decimal",
    #     "ncitCode": "C70856"
    # }, {
    #     "conceptId": "C93566",
    #     "href": "https://evsexplore.semantics.cancer.gov/evsexplore/concept/ncit/C93566",
    #     "shortName": "Fasting Status Indicator",
    #     "dataType": "boolean",
    #     "ncitCode": "C93566"
    # }, {
    #     "conceptId": "C70713",
    #     "href": "https://evsexplore.semantics.cancer.gov/evsexplore/concept/ncit/C70713",
    #     "shortName": "Biospecimen Type",
    #     "dataType": "string",
    #     "exampleSet": ["Urine", "Blood", "Saliva", "Bronchial Fluid", "Body Fluid", "Eyes", "Skin"],
    #     "ncitCode": "C70713"
    # }, {
    #     "conceptId": "C82515",
    #     "href": "https://evsexplore.semantics.cancer.gov/evsexplore/concept/ncit/C82515",
    #     "shortName": "Collection Date Time",
    #     "dataType": "datetime",
    #     "ncitCode": "C82515"
    # }],
    # "ncitCode": "C45997"'''

    # def __init__(self, id_, name:str, label:str, description:str=None, code=None, notes=None, children=None, *args):
    def __init__(self, *args, **kws):
        if isinstance(args[0], dict) and args[0] is not None:
            # initiated from a json string
            BiomedicalConceptBase.__init__(self,args[0])
        else:
            BiomedicalConceptBase.__init__(self, kws)
        # print(**kws)
        
        self._populate(**kws)



    def _populate(self, **kwargs):
        # Populate fields if they were provided as kwargs
        if len(kwargs) > 0:
            if "ncitCode" in kwargs:
                if kwargs["ncitCode"] is not None and kwargs["conceptId"] != kwargs["ncitCode"]:
                    self.code = AliasCode(kwargs["ncitCode"])
                    self.code.add_alias(Code(kwargs["conceptId"]))
            if "dataElementConcepts" in kwargs and len(kwargs["dataElementConcepts"]) > 0:
                if self.properties is None:
                    self.properties = []
                for date_element_concept in kwargs["dataElementConcepts"]:
                    self.properties.append(BiomedicalConceptProperty(date_element_concept))
            if "categories" in kwargs:
                # TODO: Add categories
                # TODO: Request categories from localStorage, by name
                self.categories = kwargs["categories"]
            if "synonyms" in kwargs:
                self.synonyms = kwargs["synonyms"]
            if "resultScales" in kwargs:
                self.notes.append([CommentAnnotation(rc,codes=[code.RESULT_SCALE]) for rc in kwargs["resultScales"]])
            if "definition" in kwargs:
                self.notes.append(CommentAnnotation(kwargs["definition"],codes=[code.DEFINITION]))
        
        # if no kwargs were provided, fetch them using the API
        elif not self._populated:
            data = get_latest_biomedical_concept(self.code.standard_code.code)
            # print(data)
            """
            {
                "conceptId": "C93566",
                "href": "https://evsexplore.semantics.cancer.gov/evsexplore/concept/ncit/C93566",
                "shortName": "Fasting Status Indicator",
                "dataType": "boolean",
                "ncitCode": "C93566"
            }
            """
            # properties: list[BiomedicalConceptProperty]
            for key,value in data.items():
                # print(f"{key}:{value}")

                match key:
                    case "conceptId":
                        if data["ncitCode"] != value and data["ncitCode"] is not None:
                            self.code = AliasCode(standard_code=(Code(data["ncitCode"],code_system="ncit")),aliases=[Code(value)])
                        else:
                            self.code = AliasCode(value)
                    case "_links":
                        #TODO: Process links
                        # print("LINKS FOUND, but not processed")
                        ...
                    case "href":
                        self.reference = value
                    case "categories":
                        #TODO Add processing of categories
                        # print("Categories found but not processed")
                        ...
                    case "shortName":
                        if value != self.label and self.label is not None:
                            print("Encountered label and shortName missmatch, resetting label")
                        self.label = value
                    case "definition":
                        if self.notes is None: self.notes = [CommentAnnotation(value,codes=[code.DEFINITION])] 
                        else: self.notes.append(CommentAnnotation(value,codes=[code.DEFINITION]))
                    case "ncitCode":
                        pass #already handling ncitCode in conceptId case
                    case "definition":
                            self.notes.append(CommentAnnotation(data["definition"],codes=[code.DEFINITION]))
                            self.notes:CommentAnnotation = [CommentAnnotation(data["definition"],codes=[code.DEFINITION])]
                    case "resultScales":
                        if self.notes is None: self.notes = [CommentAnnotation(rc,codes=[code.RESULT_SCALE]) for rc in data["resultScales"]]
                        else:
                            self.notes.append(CommentAnnotation(rc,codes=[code.RESULT_SCALE]) for rc in data["resultScales"])
                    case "dataElementConcepts":
                        self.properties = [BiomedicalConceptProperty(prop) for prop in data["dataElementConcepts"]]

                    # case "synonyms": should be caught by default case
                    #     self.synonyms = value
                    case _:
                        # print("Attempting matching key to value")
                        # print(f"{key}:{value}")
                        
                        self.key = value
        self._populated = True
            # self.response_codes = [ResponseCode(**rc) for rc in data["responseCode"]]
            # response_codes:list[ResponseCode]
            # code:AliasCode
            # synonyms:list[str] = None



    @staticmethod
    def from_json(json):
        '''Function returns a BiomedicalConceptCategory based on a provided json string'''

        """"_links": {
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
        },"""
        return BiomedicalConcept(
            code=json["_links"]["self"]["href"].split("/")[-1],
            reference=json["_links"]["self"]["href"],
            label=json["_links"]["self"]["title"],
            description=json["description"],
            package=BiomedicalConceptProperty.package_from_json(json["_links"]["parentPackage"])
            )
