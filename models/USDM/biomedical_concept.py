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


    def __init__(self, *args, **kws):
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
        self.label = title
        self.name = f"{title.replace(" ","")}_{self.id_}"
        # TODO:
        #"name": "AspartateAminotransferaseMeasurement"+id_


class BiomedicalConcept(BiomedicalConceptBase):
    __name__ = "BiomedicalConcept"
    properties: list[BiomedicalConceptProperty] = None
    response_codes:list[ResponseCode] = None
    code:AliasCode
    label:str = None
    synonyms:list[str] = None
    reference:str = "" # Not nullable
    notes:list[CommentAnnotation] = None
    _links:str = None

    def __init__(self, *args, **kws):
        # for arg in args:
        #     print(arg)
        # for kw, val in kws:
        #     print(f"{kw}: {val}")
        
        if isinstance(args[0], dict) and args[0] is not None:
            # initiated from a json string
            super().__init__(args[0])
        else:
            super().__init__(kws)
        self.populate(**kws)
        if self.reference == "" or self.reference is None:
            raise ValueError("Reference can't be None or empty")

    def populate(self, **kwargs):
        """ Populates BiomedicalConcept's satelite data based on provided kwargs
        Requests data from API if no keyword-args were provided
        """
        # Populate fields if they were provided as kwargs
        if len(kwargs) > 0:
            if "ncitCode" in kwargs:
                if kwargs["ncitCode"] is not None and kwargs["conceptId"] != kwargs["ncitCode"]:
                    self.code = AliasCode(kwargs["ncitCode"])
                    self.code.add_alias(Code(kwargs["conceptId"]))
            if "dataElementConcepts" in kwargs and len(kwargs["dataElementConcepts"]) > 0:
                if self.properties is None:
                    self.properties = []
                for data_element_concept in kwargs["dataElementConcepts"]:
                    print(f"dec:{data_element_concept}")
                    self.properties.append(BiomedicalConceptProperty(data_element_concept))
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
            #TODO REWORK THIS, it's slowing it down massively
            json_data = get_latest_biomedical_concept(self.code.standard_code.code)

            for key,value in json_data.items():
                match key:
                    case "conceptId":
                        if not "ncitCode" in json_data.keys():
                            pass
                        elif json_data["ncitCode"] is not None and json_data["ncitCode"] != value:
                            self.code = AliasCode(standard_code=(Code(json_data["ncitCode"],code_system="ncit")),aliases=[Code(value)])
                        else:
                            self.code = AliasCode(value)
                    # already handling ncitCode in conceptId case
                    case "ncitCode": pass # already handling ncitCode in conceptId case
                    case "coding":
                        for coding_ in json_data["coding"]:
                            self.code.add_alias(Code(
                                code=coding_["code"],
                                code_system=coding_["systemName"]
                            ))
                        # self.code.add_alias(Code(
                        #     code=json_data["coding"]["code"],
                        #     code_system=json_data["coding"]["systemName"]))
                    case "_links":
                        self._links = value
                        #TODO: Process links
                        # print("LINKS FOUND, but not processed")
                        ...
                    case "href":
                        self.reference = value
                    case "categories":
                        #TODO Add processing of categories
                        # print("Categories found but not processed")
                        pass # not allowed to have empty case
                    case "shortName":
                        if value != self.label and self.label is not None:
                            print("Encountered label and shortName missmatch, resetting label")
                        self.label = value
                    case "definition":
                        if self.notes is None:
                            self.notes = [CommentAnnotation(value,codes=[code.DEFINITION])] 
                        else: self.notes.append(CommentAnnotation(value,codes=[code.DEFINITION]))
                    # case "definition":
                    #         self.notes.append(CommentAnnotation(json_data["definition"],codes=[code.DEFINITION]))
                    #         self.notes:CommentAnnotation = [CommentAnnotation(json_data["definition"],codes=[code.DEFINITION])]
                    case "resultScales":
                        if self.notes is None:
                            self.notes = [CommentAnnotation(rc,codes=[code.RESULT_SCALE]) for rc in json_data["resultScales"]]
                        else:
                            self.notes.append(CommentAnnotation(rc,codes=[code.RESULT_SCALE]) for rc in json_data["resultScales"])
                    case "dataElementConcepts":
                        print("ADDING PROPERTIES")

                        self.properties = [BiomedicalConceptProperty(prop) for prop in json_data["dataElementConcepts"]]

                    # case "synonyms": should be caught by default case
                    #     self.synonyms = value
                    case _:
                        # print("Attempting matching key to value")
                        #TODO:
                        # Deal with this:
                        #                     'key': [{
                        #         'code': '64098-7',
                        #         'system': 'http://loinc.org/',
                        #         'systemName': 'LOINC'
                        #     }
                        # ],
                        self.__dict__[key] = value
                        if key != "synonyms":
                            print(f"Attempting to match key to value: {key}")
                        # self.misc[key] = value
        self._populated = True



    @staticmethod
    def from_json(json):
        return BiomedicalConcept(
            code=json["_links"]["self"]["href"].split("/")[-1],
            reference=json["_links"]["self"]["href"],
            label=json["_links"]["self"]["title"],
            description=json["description"],
            package=BiomedicalConceptProperty.package_from_json(json["_links"]["parentPackage"])
            )
