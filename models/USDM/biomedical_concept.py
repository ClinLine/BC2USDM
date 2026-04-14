from __future__ import annotations
from uuid import UUID, uuid4 as guid

# from models.CDISC import AttributeNames as CDISC_Attributes
from models.CDISC.BiomedicalConceptLink import Link as CDISC_Link
# from models.CDISC.BiomedicalConceptLink import BiomedicalConceptLink as CDISC_Links
from models.CDISC import AttributeNames as CDISC_Attributes
from models.DTOs import DataElementConceptDTO
from models.USDM import AttributeNames as USDM_Attributes
from models.USDM.biomedical_concept_category import BiomedicalConceptCategory as USDM_category
from models.USDM.biomedical_concept_property import BiomedicalConceptProperty
from models.USDM.code import DEFINITION, RESULT_SCALE, Code
from models.USDM.comment_annotation import CommentAnnotation
from models.USDM.response_code import ResponseCode
from models.USDM.code.alias_code import AliasCode
# from utils.utils import Encoding
from utils.api_utils import get_latest_biomedical_concept
from utils.b_colors import BColors

class BiomedicalConceptBase:
    id_:UUID
    reference:str
    name:str
    label:str
    code:AliasCode
    datatype:str = "Biomedical Concept"
    _populated:bool = False
    categories=None
    # parent:type["BiomedicalConceptBase"]


    def __init__(self, *args, **kws):
        if isinstance(args[0], dict) and args[0] is not None:
            # initiated from a json string
            self.__init_from_dict(args[0])
        elif len(args) > 1:
            self.init_from_args(args)
        else:
            # parameterised initiation
            self.__init_from_params__(kws["href"], kws["title"], kws["type"])

    def __init_from_dict(self, dict_:dict):
        if "href" in dict_.keys():
            self.__init_from_params__(dict_["href"], dict_["title"], dict_["type"])
        elif "reference" in dict_.keys():
            self.__init_from_params__(dict_["reference"], dict_["title"], dict_["type"])



    def __init_from_args(self, *args):
        id_ = args[0]
        name = args[1]
        label = args[2]
        synonyms = args[3]
        reference = args[4]
        properties = args[5]
        code = args[6]
        notes = args[7]
        instance_type = args[8]

        '''dict_ = 
        {
            'id_': 'b458d281-2654-4552-a662-5dbffce2b58f', 
            'label': '6MWT - Distance at 1 Minute', 
            'code': 'C115800', 
            'reference': 'https://evsexplore.semantics.cancer.gov/evsexplore/concept/ncit/C115800', 
            'synonyms': "('SIXMW101', 'SIXMW1-Distance at 1 Minute')", 
            'notes': [
                'Ordinal',
                'Brief Psychiatric Rating Scale-Anchored (BPRS-A) Guilt feelings.',
                'Ordinal',
                'Brief Psychiatric Rating Scale-Anchored (BPRS-A) Somatic concern.',
                'Quantitative',
                '6 Minute Walk Test (6MWT) Distance at 1 minute.'
            ], 
            'properties': {
                '4f68ac5d-f0af-4a99-8ed2-eea1b287b8ef': {...},
                'b89bb357-83ee-4b58-99e4-73b2fcd268b3': {...},
                'c03c7953-95d4-48f4-a1e6-86e6a9a1bed6': {...},
                '2b34697d-2721-44d9-bf28-5b5ee28ebee7': {...},
                'f24ff648-caed-4c7b-bdbe-ce3d6957a790': {...}
            }
        }
'''

    # def __init_from_params__(self, href:str, title:str, type_:str, package=None):
    def __init_from_params__(self, reference:str, title:str, package=None):
        self._populated = False
        self.reference = reference
        self.code = AliasCode(reference.split('/')[-1])
        self.id_ = guid() # TODO: Request guid from local storage
        self.label = title
        self.name = f"{title.replace(" ","")}_{self.id_}"
        # TODO:
        #"name": "AspartateAminotransferaseMeasurement"+id_


# class BiomedicalConcept(BiomedicalConceptBase):
class BiomedicalConcept:
    # __name__ = "BiomedicalConcept"
    # DATA_TYPE = "Biomedical Concept"
    properties: list[BiomedicalConceptProperty] = None
    code:AliasCode
    _package_version:str
    label:str = None
    synonyms:list[str] = None
    reference:str = "" # Not nullable
    notes:list[CommentAnnotation] = None
    INSTANCE_TYPE = __qualname__
    categories = list[USDM_category]
    _links:str = None
    _modified:bool = False
    _populated = False

    def __init__(self,
                id_:UUID|str|None=None,
                # name:str="",
                label:str="",
                # title:str="",
                synonyms:list[str]=None,
                # href:str="",
                reference:str="",
                properties:list[dict]|list[BiomedicalConceptProperty]=None,
                code:str|Code=None,
                notes:list[str]|list[CommentAnnotation]=None,
                instance_type:str=INSTANCE_TYPE,
                biomedical_concept:BiomedicalConcept=None,
                category=None,
                *args, **kws):
        if biomedical_concept:
            self.__setattr__("self", biomedical_concept)
        # if kws["_links"]: print(kws["_links"])
        if isinstance(id_,(UUID,str)):
            self.id_ = UUID(id_)
        else:
            self.id_ = guid()
        if label is not None and label != "":
                self.label = label
        else:
            # Print error if no lable and no title were found
            print(f"{BColors.FAIL}Error: BC({self.id_}) has no label{BColors.ENDC}")
        self.name = '_'.join([self.label.replace(" ",""),str(self.id_)])
        
        if synonyms:
            self.synonyms = synonyms,

        if reference != "" and reference is not None:
            self.reference = reference
        else:
            raise ValueError(f"{BColors.FAIL}Reference can't be None or empty{BColors.ENDC}")
        if notes is not None and len (notes) > 0:
            if self.notes is None:
                self.notes = []
            for note in notes:
                if isinstance(note, CommentAnnotation):
                    self.notes = notes
                else:
                    
                    self.notes.append(CommentAnnotation(note, codes = [Code]))
        if not isinstance(properties,type(None)):
            print(f"{BColors.OKCYAN}bc concstructor: (PARAM) properties := {type(properties)}{BColors.ENDC}")
        if self.properties is None:
            self.properties = []
        if properties is not None:
            if len(properties) > 0:
                for prop_id, prop in properties.items():
                    if isinstance(prop, BiomedicalConceptProperty):
                        self.properties = properties
                        break
                    elif isinstance(prop, dict):
                        self.properties.append(BiomedicalConceptProperty(**prop, parent_bc_id=id_))
                    else:
                        print(f"type is: {type(prop)}")
            # elif isinstance(properties, dict) and len(properties) > 0:
            # self.properties = [BiomedicalConceptProperty(prop) for prop in properties]
        else:
            self.properties = None

        if isinstance(code, Code|AliasCode):
            self.code = code
        elif code is not None:
            print(f"{BColors.WARNING}[Warning]{__name__}.init: {Code.__name__} is not none but not af type {Code.__name__} or {AliasCode.__name__}{BColors.ENDC}")
            print(f"code: {code}")
            self.code = AliasCode(
                standard_code=Code(
                    code=code,
                    code_system=Code.CodeSystem.CUSTOM,
                    code_system_version=Code.DEFAULT_CODE_SYSTEM_VERSION
                )
            )
        elif code is None:
            self.code = None
            self._populated = False


        # TODO: Add more sophisticated notes handling (tagging notes with id / descriptor / codes)
        if notes is not None and len(notes) > 1:
            if isinstance(notes[0], CommentAnnotation):
                self.notes = notes
            elif isinstance(notes[0], str):
                self.notes = [CommentAnnotation(note) for note in notes]

        if instance_type is not None and instance_type.replace(' ','') != self.INSTANCE_TYPE:
            # if instance_type == BiomedicalConcept.DATA_TYPE and (self.INSTANCE_TYPE is None or self.INSTANCE_TYPE == ""):
            #     self.INSTANCE_TYPE = BiomedicalConcept.DATA_TYPE
            # elif instance_type != BiomedicalConcept.DATA_TYPE:
            raise AttributeError(f"The type of {self.__qualname__} cannot be set")
            


    def populate(self, **kwargs):
        """ Populates BiomedicalConcept's satelite data based on provided kwargs
        Requests data from API if no keyword-args were provided
        """
        
        if len(kwargs) < 1:
            print([f"{BColors.WARNING}[Warning] {__name__}.{BiomedicalConcept.populate.__name__}populate: Populating with empty params is going to be deprecated{BColors.ENDC}"])
        print(f"Populating following keys: {kwargs.keys()}")
        
        # The following are already handled at BC creation:
        # self.reference = kwargs["href"]
        # self.label = kwargs["title"]
        # self.instance_type = kwargs["type"]

        keys = kwargs.keys()
        if self.label is None or self.label == "":
            if CDISC_Attributes.BiomedicalConcept.short_name in keys:
                self.label = kwargs[CDISC_Attributes.BiomedicalConcept.short_name]
        
        # parentBC
        if CDISC_Attributes.BiomedicalConcept.links in keys:
            package_link:CDISC_Link = CDISC_Link(**kwargs[CDISC_Attributes.BiomedicalConcept.links][CDISC_Attributes.BiomedicalConcept.BiomedicalConceptLinks.parent_package])
            self._package_version = Code.get_version_from_reference(package_link.href)

        if USDM_Attributes.BiomedicalConcept.code in keys and isinstance(kwargs[USDM_Attributes.BiomedicalConcept.code],AliasCode):
            self.code = kwargs[USDM_Attributes.BiomedicalConcept.code]
        else:
            if CDISC_Attributes.BiomedicalConcept.ncit_code in keys and CDISC_Attributes.BiomedicalConcept.concept_id in keys:
                if kwargs[CDISC_Attributes.BiomedicalConcept.ncit_code] != kwargs[CDISC_Attributes.BiomedicalConcept.concept_id]:
                    # Handle different codes
                    # Create Code for ncit_code
                    ncit_code = Code(kwargs[CDISC_Attributes.BiomedicalConcept.ncit_code], code_system=Code.CodeSystem.NCIT, code_system_version=Code.get_version_from_reference(self.reference),decode=self.label)
                    # create Code for found conceptId
                    conceptid_code = Code(kwargs[CDISC_Attributes.BiomedicalConcept.concept_id], code_system=Code.CodeSystem.CDISC, code_system_version=Code.get_version_from_reference(self.reference),decode=self.label)
                    # Set AliasCode alias with ncitCode as standard and concept as alias
                    self.code = AliasCode(standard_code=ncit_code, aliases=[conceptid_code])
                else: # ncitCode == conceptId
                    # Assure code is not None
                    if kwargs[CDISC_Attributes.BiomedicalConcept.ncit_code] is not None:
                        self.code = AliasCode(
                            standard_code= Code(
                                    code=kwargs[CDISC_Attributes.BiomedicalConcept.ncit_code],
                                    code_system=Code.CodeSystem.NCIT,
                                    code_system_version=Code.get_version_from_reference(
                                        kwargs[CDISC_Attributes.BiomedicalConcept.links]
                                        [CDISC_Attributes.BiomedicalConcept.BiomedicalConceptLinks.parent_package]
                                        [CDISC_Attributes.BiomedicalConceptPackage.reference]),
                                    decode=self.label))
        
        if CDISC_Attributes.BiomedicalConcept.coding in keys and kwargs[CDISC_Attributes.BiomedicalConcept.coding]:
            coding_dict_list = kwargs[CDISC_Attributes.BiomedicalConcept.coding] # is list with codings
            for coding_dict in coding_dict_list:

                _code:str = coding_dict[CDISC_Attributes.BiomedicalConcept.Coding.code] # is list
                code_system:str = coding_dict[CDISC_Attributes.BiomedicalConcept.Coding.system]
                # code_system_name:str = coding_dict[CDISC_Attributes.BiomedicalConcept.Coding.system_name] # Not used
                code_system_version:str = Code.get_version_from_reference(self.reference)
                alias:Code = Code(code=_code,code_system=code_system,code_system_version=code_system_version)
                self.code.add_alias(alias=alias)
        
        


        
        


        # shortName x 

        # synonyms x
        if not self.synonyms:
            # note: CDISC_Attributes.BiomedicalConcept.synonyms == USDM_Attributes.BiomedicalConcept.synonyms
            if CDISC_Attributes.BiomedicalConcept.synonyms in keys:
                if kwargs[CDISC_Attributes.BiomedicalConcept.synonyms] and isinstance(kwargs[CDISC_Attributes.BiomedicalConcept.synonyms],str):
                    # TODO implement storing synonyms
                    print(CDISC_Attributes.BiomedicalConcept.synonyms)
                    _synonyms = kwargs[CDISC_Attributes.BiomedicalConcept.synonyms].split(',')
                    self.synonyms = [synonym.trim() for synonym in _synonyms if synonym.trim()]
                elif kwargs[USDM_Attributes.BiomedicalConcept.synonyms] and isinstance(kwargs[USDM_Attributes.BiomedicalConcept.synonyms], list):
                    self.synonyms = kwargs[USDM_Attributes.BiomedicalConcept.synonyms]
        else:
            print("Synonyms seems to already have been populated")
            new_synonyms = []
            if CDISC_Attributes.BiomedicalConcept.synonyms in keys and kwargs[CDISC_Attributes.BiomedicalConcept.synonyms]:
                if isinstance(kwargs[CDISC_Attributes.BiomedicalConcept.synonyms],str):
                    new_synonyms = kwargs[CDISC_Attributes.BiomedicalConcept.synonyms].map()
                    new_synonyms = map(lambda s: s.trim() ,kwargs[CDISC_Attributes.BiomedicalConcept.synonyms].split(','))
                elif isinstance(kwargs[USDM_Attributes.BiomedicalConcept.synonyms], list) and len(kwargs[USDM_Attributes.BiomedicalConcept.synonyms]) > 0:
                    new_synonyms = kwargs[USDM_Attributes.BiomedicalConcept.synonyms]
                else:
                    raise TypeError(f"{BColors.FAIL} synonyms parameter can only be of type str or list{BColors.ENDC}")
            if len(new_synonyms) > 0:
                self.synonyms = new_synonyms

        # definition & resultScales x
        should_have_result_scale = CDISC_Attributes.BiomedicalConcept.result_scales in keys
        if CDISC_Attributes.BiomedicalConcept.definition in keys:
            # if not DEFINITION in [codes. for *codes in [note.codes for note in self.notes]]:
            if self.notes is None:
                self.notes = [CommentAnnotation(kwargs[CDISC_Attributes.BiomedicalConcept.definition],codes=[DEFINITION])]
                if should_have_result_scale:
                    for scale in kwargs[CDISC_Attributes.BiomedicalConcept.result_scales]:
                        self.notes.append(CommentAnnotation(scale, codes=[RESULT_SCALE]))
            else:
                has_definition = False
                has_result_scale = False
                
                for note in self.notes:
                    if DEFINITION.code in [note_code.code for note_code in note.codes]:
                        has_definition = True
                    if should_have_result_scale:
                        if RESULT_SCALE.code in [note_code.code for note_code in note.codes]:
                            has_result_scale = True

                if not has_definition:
                    self.notes.append(CommentAnnotation(text=kwargs[CDISC_Attributes.BiomedicalConcept.definition],codes=[DEFINITION]))
                if not has_result_scale and should_have_result_scale:
                    for scale in kwargs[CDISC_Attributes.BiomedicalConcept.result_scales]:
                        self.notes.append(CommentAnnotation(scale, codes=[RESULT_SCALE]))
        if USDM_Attributes.BiomedicalConcept.notes in keys:
            raise NotImplementedError(f"{BColors.FAIL}BiomedicalConcept.Populate does not take notes yet{BColors.ENDC}")
                
        # dataElementConcepts
        if CDISC_Attributes.BiomedicalConcept.data_element_concepts in keys:
            # [f(x) if condition else g(x) for x in sequence] // List comprehension
            # {f(x) if condition else g(x) for x in sequence} // dict comprehension
            self.properties = [BiomedicalConceptProperty(data_element_concept=DataElementConceptDTO(**dto)) for dto in kwargs[CDISC_Attributes.BiomedicalConcept.data_element_concepts]]
            # self.properties = [BiomedicalConceptProperty(prop.id_, prop) for prop in kwargs[CDISC_Attributes.BiomedicalConcept.data_element_concepts] if prop.id_]
        # properties
        elif USDM_Attributes.BiomedicalConcept.properties in keys:
            raise NotImplementedError(f"{BColors.FAIL}[BiomedcalConcept.populate]: Parsing {USDM_Attributes.BiomedicalConcept.properties} is not implemented yet.{BColors.ENDC}")
        

       
            
            # parent_link:CDISC_Link = CDISC_Link(**kwargs[CDISC_Attributes.BiomedicalConcept.links][CDISC_Attributes.BiomedicalConcept.BiomedicalConceptLinks.parent_biomedical_concept])
            # self_link:CDISC_Link = CDISC_Link(kwargs[CDISC_Attributes.BiomedicalConcept.links][CDISC_Attributes.BiomedicalConcept.BiomedicalConceptLinks.self])
            # self_link:CDISC_Link = CDISC_Link(kwargs[CDISC_Attributes.BiomedicalConcept.links][CDISC_Attributes.BiomedicalConcept.BiomedicalConceptLinks.self])
            
            # self._links = CDISC_Links(parent_link, package_link, self_link)
            # self.parent_biomedical_concept = BiomedicalConcept(parent_link.href, parent_link.title)
            
        # self.categories
        if CDISC_Attributes.BiomedicalConcept.categories in keys:
            self.categories = [USDM_category.from_short_name(cat) for cat in kwargs[CDISC_Attributes.BiomedicalConcept.categories]]

        # # Populate fields if they were provided as kwargs
        # if len(kwargs) > 0:
        #     if "ncitCode" in kwargs:
        #         if kwargs["ncitCode"] is not None and kwargs["conceptId"] != kwargs["ncitCode"]:
        #             self.code = AliasCode(kwargs["ncitCode"])
        #             self.code.add_alias(Code(kwargs["conceptId"]))
        #     if "dataElementConcepts" in kwargs and len(kwargs["dataElementConcepts"]) > 0:
        #         if self.properties is None:
        #             self.properties = []
        #         for data_element_concept in kwargs["dataElementConcepts"]:
        #             print(f"Data_element_concept:{data_element_concept}")
        #             self.properties.append(BiomedicalConceptProperty(data_element_concept))
        #     if "categories" in kwargs:
        #         # TODO: Add categories
        #         # TODO: Request categories from localStorage, by name
        #         self.categories = kwargs["categories"]
        #     if "synonyms" in kwargs:
        #         self.synonyms = kwargs["synonyms"]
        #     if "resultScales" in kwargs:
        #         self.notes.append([CommentAnnotation(rc,codes=[RESULT_SCALE]) for rc in kwargs["resultScales"]])
        #     if "definition" in kwargs:
        #         self.notes.append(CommentAnnotation(kwargs["definition"],codes=[DEFINITION]))
        
        # # if no kwargs were provided, fetch them using the API
        # elif not self._populated:
        #     #TODO REWORK THIS, it's slowing it down massively
        #     json_data = get_latest_biomedical_concept(self.code.standard_code.code)

        #     for key,value in json_data.items():
        #         match key:
        #             case "conceptId":
        #                 if not "ncitCode" in json_data.keys():
        #                     pass
        #                 elif json_data["ncitCode"] is not None and json_data["ncitCode"] != value:
        #                     self.code = AliasCode(standard_code=(Code(json_data["ncitCode"],code_system="ncit")),aliases=[Code(value)])
        #                 else:
        #                     self.code = AliasCode(value)
        #             # already handling ncitCode in conceptId case
        #             case "ncitCode": pass # already handling ncitCode in conceptId case
        #             case "coding":
        #                 for coding_ in json_data["coding"]:
        #                     self.code.add_alias(Code(
        #                         code=coding_["code"],
        #                         code_system=coding_["systemName"]
        #                     ))
        #                 # self.code.add_alias(Code(
        #                 #     code=json_data["coding"]["code"],
        #                 #     code_system=json_data["coding"]["systemName"]))
        #             case "_links":
        #                 self._links = value
        #                 #TODO: Process links
        #                 # print("LINKS FOUND, but not processed")
        #                 ...
        #             case "href":
        #                 self.reference = value
        #             case "reference":
        #                 self.reference = value
        #             case "categories":
        #                 #TODO Add processing of categories
        #                 # print("Categories found but not processed")
        #                 pass # not allowed to have empty case
        #             case "shortName":
        #                 if value != self.label and self.label is not None:
        #                     print("Encountered label and shortName missmatch, resetting label")
        #                 self.label = value
        #             case "definition":
        #                 if self.notes is None:
        #                     self.notes = [CommentAnnotation(value,codes=[DEFINITION])] 
        #                 else: self.notes.append(CommentAnnotation(value,codes=[DEFINITION]))
        #             # case "definition":
        #             #         self.notes.append(CommentAnnotation(json_data["definition"],codes=[code.DEFINITION]))
        #             #         self.notes:CommentAnnotation = [CommentAnnotation(json_data["definition"],codes=[code.DEFINITION])]
        #             case "resultScales":
        #                 if self.notes is None:
        #                     self.notes = [CommentAnnotation(rc,codes=[RESULT_SCALE]) for rc in json_data["resultScales"]]
        #                 else:
        #                     self.notes.append(CommentAnnotation(rc,codes=[RESULT_SCALE]) for rc in json_data["resultScales"])
        #             case "dataElementConcepts":
        #                 print("ADDING PROPERTIES")

        #                 self.properties = [BiomedicalConceptProperty(prop) for prop in json_data["dataElementConcepts"]]

        #             # case "synonyms": should be caught by default case
        #             #     self.synonyms = value
        #             case _:
        #                 # print("Attempting matching key to value")
        #                 #TODO:
        #                 # Deal with this:
        #                 #                     'key': [{
        #                 #         'code': '64098-7',
        #                 #         'system': 'http://loinc.org/',
        #                 #         'systemName': 'LOINC'
        #                 #     }
        #                 # ],
        #                 self.__dict__[key] = value
        #                 if key != "synonyms":
        #                     print(f"Attempting to match key to value: {key}")
        #                 # self.misc[key] = value
        self._populated = True

    def __eq__(self, other) -> bool:
        if isinstance(other, BiomedicalConcept):
            if other.id_ == self.id_:
                return True
            else:
                return False
        raise NotImplementedError()
    
        #  if self.code and other.code:
        #     if self.code.standard_code.code != other.code.standard_code.code: return False
        # if self.label != other.label: return False
        # if self.synonyms is not None and other.synonyms is not None:
        #     if len(self.synonyms) != len(other.synonyms): return False
        # if self.notes is None and other.notes is not None: return False
        # if self.notes is not None and other.notes is None: return False
        # if self.notes and other.notes:
        #     if len(self.notes) != len(other.notes): return False
        # for note in self.notes:
        #     if note not in other.note: return False
        # for i, prop in enumerate(self.properties):
        #     if prop != other.properties[i]: return False
        # return True

    def set_label(self, label:str):
        self.label = label
        self._set_modified(True)
            

    def _set_modified(self, value:bool):
        if self._modified and value:
            # was already marked as modified
            return
        if not self._modified and value:
            # Generate new Alias code, 
            # since bc has been modified from library
            old_alias:AliasCode = self.code
            self.code = AliasCode(
                standard_code=Code(
                    code=f"{Code.CustomBiomedicalConceptFlag}-{str(self.id_)[-7:-1]}", # BiomedicalConceptUSDM-Last 6 digits of ID
                    id_=guid(),
                    code_system=Code.CodeSystem.CUSTOM,
                    code_system_version="00",
                    decode=old_alias.standard_code.decode
                )
            )
        self._modified = value

    

    @staticmethod
    def from_json(json):
        return BiomedicalConcept(
            code=json["_links"]["self"]["href"].split("/")[-1],
            reference=json["_links"]["self"]["href"],
            label=json["_links"]["self"]["title"],
            description=json["description"],
            package=BiomedicalConceptProperty.package_from_json(json["_links"]["parentPackage"])
            )
    
    def __hash__(self):
        # id_
        # properties: list[BiomedicalConceptProperty] = None
        # code:AliasCode
        # _package_version:str
        # label:str = None
        # synonyms:list[str] = None
        # reference:str = "" # Not nullable
        # notes:list[CommentAnnotation] = None
        # INSTANCE_TYPE = __qualname__
        # categories = list[USDM_category]
        # _links:str = None
        # _modified:bool = False
        # _populated = False
        
        # args = (self.id_, 
        #         self.label,
        #         self.synonyms,
        #         )
        
        
        raise NotImplementedError()
    
    @staticmethod
    def sync(origin:BiomedicalConcept, target:BiomedicalConcept) -> BiomedicalConcept:
        #     # __name__ = "BiomedicalConcept"
        # # DATA_TYPE = "Biomedical Concept"
        # match = True
        # id_ = None
        
        # match = hash(origin) == hash(target)
        # label = target.label
        

        # if match:
        #     id_ = origin.id_
        # else:
        #     id_ = guid()
        # name = "_".join((target.label.replace(" ",""),id_))
        raise NotImplementedError()