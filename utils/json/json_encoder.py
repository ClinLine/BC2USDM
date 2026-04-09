
import json
from uuid import UUID
# from models.CDISC.BiomedicalConceptLink import BiomedicalConceptLink
from models.USDM.biomedical_concept import BiomedicalConcept
# from models.USDM.BiomedicalConceptCategory import BiomedicalConceptCategory as USDM_Category
from models.USDM.biomedical_concept_category import BiomedicalConceptCategory
from models.USDM.biomedical_concept_property import BiomedicalConceptProperty
from models.USDM.code.alias_code import AliasCode
from models.USDM.code import Code as USDM_Code, DEFINITION
from models.USDM.comment_annotation import CommentAnnotation
from models.USDM.repository import Repository as USDM_Repository
from models.USDM.response_code import ResponseCode
from models.USDM.therapeutic_area import TherapeuticArea
from utils.b_colors import BColors
# from models.CDISC.BiomedicalConceptCategory import BiomedicalConceptCategory as CDISC_Category

class IterEncoder(json.JSONEncoder):
    def default(self, o):
        print(f"IterEncoder: encoding {o.__class__.__name__}")
        try:
            iterable = iter(o)
        except TypeError as err:
            print(f"{BColors.FAIL}ERROR: {err}{BColors.ENDC}")
            pass
            # return super().default(o)
        else:
            return list(iterable)
        # Let the base class default method raise the TypeError
        return super().default(o)

class UUIDEncoder(json.JSONEncoder):
    def default(self, o):
        print(f"UUIDEncoder: encoding {o.__class__.__name__}")
        if isinstance(o, UUID):
            return str(o)
        # Let the base class default method raise the typeError
        return super().default(o)

class CodeEncoder(json.JSONEncoder):
    def default (self, o):
        print(f"CodeEncoder: encoding {o.__class__.__name__}")
        # if isinstance(o, (Code, AliasCode)):
        if isinstance(o, USDM_Code):
            try:
                code = {}
                code["id"] = super().default(o.id_)
                # code["id"] = json.dumps(o.id_,cls=UUIDEncoder)
                code["code"] = o.code
                if o.code_system is None:
                    code["codeSystem"] = None
                    # ValueError("code system can't be None")
                    print(f"{BColors.WARNING}code system can't be None{BColors.ENDC}")
                code["codeSystem"] = o.code_system
                code["codeSystemVersion"] = o.code_system_version
                code["decode"] = o.decode
                code["instanceType"] = o.INSTANCE_TYPE
            except TypeError:
                print("Encountered a typeError while trying to encode a Code object.")
            else:
                # print(f"Returning Code: {code}")
                return code
        # Let the base class default method raise the typeError
        return super().default(o)

class AliasCodeEncoder(json.JSONEncoder):
    def default(self, o):
        print(f"AliasCodeEncoder: encoding {o.__class__.__name__}")
        if isinstance(o, AliasCode):
            try:
                alias_code = {}
                alias_code["id"] = super().default(o.id_)
                alias_code["standardCode"] = super().default(o.standard_code)
                if o.standard_code_aliases is not None and len(o.standard_code_aliases)>0:
                    alias_code["standardCodeAliases"] = super().default(o.standard_code_aliases)
                else:
                    alias_code["standardCodeAliases"] = []
                alias_code["instanceType"] = o.INSTANCE_TYPE
            except TypeError:
                print("Encountered a typeError while trying to encode a AliasCode object.")
            else:
                # print(f"returning aliasCode: {aliasCode}")
                return alias_code
        # Let the base class default method raise the typeError
        return super().default(o)

class CommentAnnotationEncoder(json.JSONEncoder):
    def default(self, o):
        print(f"CommentAnnotationEncoder: encoding {o.__class__.__name__}")
        
        if isinstance(o, CommentAnnotation):
            print(o)
            comment_annotation = {}
            try:
                if o.codes is not None and DEFINITION not in o.codes:
                    # comment_annotation["id"] = json.dumps(o.id_, UUIDEncoder)
                    comment_annotation["id"] = super().default(o.id_)
                    comment_annotation["text"] = o.text
                    if o.codes is not None:
                        # codes is list of codes
                        comment_annotation["codes"] = super().default(o.codes) 
                    else:
                        comment_annotation["codes"] = []
                    
            except TypeError as err:
                print(f"Encountered a typeError while trying to encode a CommentAnnotation object.\n {err}")
                pass
            else:
                return comment_annotation
        return super().default(o)

class RepositoryEncoder(json.JSONEncoder):
    
    def decode_therapeutic_area(self, therapeutic_area, child_categories, biomedical_concepts)  -> dict[str,str]:
        print(f"{BColors.WARNING}Warning {__name__} ln:60: Currently a max of 1 Business Therapeutic Area(s) is hardcoded in this encoder.{BColors.ENDC}")
        members = [*[str(category.id_) for category in child_categories],
                       *[str(bc.id_) for bc in biomedical_concepts if bc]]
        ta = super().default(therapeutic_area)
        ta["memberIds"] = members
        return ta
    
    def decode_biomedical_concepts(self, biomedical_concepts) -> list[dict[str,str]]:
        decoded_biomedical_concept_list = [super().default(biomedical_concept) for biomedical_concept in biomedical_concepts if biomedical_concept]
        return decoded_biomedical_concept_list
    
    def default(self, o):
        print(f"RepositoryEncoder: encoding {o.__class__.__name__}")
        if isinstance(o, USDM_Repository):
            repo = {}
            repo["bcRepository"] = {}
            repo["bcRepository"]["businessTherapeuticAreas"] = {}
            
            # repo["bcRepository"]["bcCategories"] = [super().default(category) for category in o.bc_categories if category]
            
            # bcs_ = []
            # for bc in o.biomedical_concepts.values():
            #     bcs_.append(super().default(bc))
            
            repo["bcRepository"]["biomedicalConcepts"] = self.decode_biomedical_concepts(o.biomedical_concepts.values())
            # # repo["bcRepository"]["biomedicalConcepts"] = super().default(o.biomedical_concepts)
            
            
           
            
            # repo["bcRepository"]["businessTherapeuticAreas"] = self.decode_therapeutic_area(
            #     o.business_therapeutic_areas[0],
            #     o.bc_categories,
            #     o.biomedical_concepts.values())
            # print(repo)
            
            return repo
        return super().default(o)

class TherapeuticAreaEncoder(json.JSONEncoder):
    def default(self, o):
        print(f"TherapeuticAreaEncoder: encoding {o.__class__.__name__}")
        if isinstance(o, dict) and len(o) == 2:
            bta_code:USDM_Code = o["therapeutric_area"].code
            members = o["members"]
            raise NotImplementedError()
            # therapeutic_area_dict:dict = json.dumps(bta_code,cls=CodeEncoder)
            therapeutic_area_dict:dict = super().default(bta_code)
            
            # code_dict = super().default(o.business_therapeutic_areas[0])
            # therapeutic_area_dict["id"] = super().default(o.business_therapeutic_areas.code.id_)
            # therapeutic_area_dict["code"] o
            
        if isinstance(o,TherapeuticArea):
            
            code = super().default(o.code)
            therapeutic_area_dictionary:dict = {}
            therapeutic_area_dictionary["id"] = code["id"]
            therapeutic_area_dictionary["code"] = code["code"]
            therapeutic_area_dictionary["codeSystem"] = code["codeSystem"]
            therapeutic_area_dictionary["codeSystemVersion"] = code["codeSystemVersion"]
            therapeutic_area_dictionary["decode"] = code["decode"]
            therapeutic_area_dictionary["instanceType"] = o.code.INSTANCE_TYPE
            therapeutic_area_dictionary["memberIds"] = None
            return therapeutic_area_dictionary
            
        return super().default(o)

class BiomedicalConceptCategoryEncoder(json.JSONEncoder):
    def default(self, o):
        print(f"BiomedicalConceptCategoryEncoder: encoding {o.__class__.__name__}")
        if isinstance(o, BiomedicalConceptCategory):
            category = {}
            category["id"] = super().default(o.id_)
            category["name"] = o.name
            if o.notes is None: category["description"] = ""
            else:
                category["description"] = super().default(CommentAnnotation.find_definition(o.notes))
            category["label"] = o.label
            category["code"] = super().default(o.code)
            category["childIds"] = []
            # TODO: add memberIds
            # category["memberIds"] = super().default(o.children)
            category["memberIds"] = []
            category["instanceType"] = o.INSTANCE_TYPE
            if o.notes is not None:
                category["notes"] = super().default(o.notes)
            else: category["notes"] = []

            return category
        return super().default(o)

class BiomedicalConceptEncoder(json.JSONEncoder):
    def do_code(self, alias_code:AliasCode) -> dict:
        print("decoding code")
        result = {}
        _ = super().default(alias_code)
        return result

    def do_notes(self, notes):
        result = []
        print(f"{BColors.WARNING} BC ENCODER: NOT ADDING NOTES!!{BColors.ENDC}")
        print(f"provided notes: {notes}")
        # if o.notes is not None and len(o.notes) > 0:
        #     biomedicalConcept["notes"] = [super().default(note) for note in o.notes if note and o.notes]
        #     biomedicalConcept["notes"] = super().default(o.notes)
        return result
    
    def do_props(self, properties):
        result = []
        # print(f"{BColors.WARNING} BC ENCODER: NOT ADDING propeties yet!!{BColors.ENDC}")
            # if hasattr(o, "properties") and o.properties is not None and len(o.properties) > 0:
                # print("properties found")
        result = [super().default(prop) for prop in properties]
        return result

    def default(self, o):
        print(f"BiomedicalConceptEncoder: encoding {o.__class__.__name__}")
        
        if isinstance(o, BiomedicalConcept):
            biomedicalConcept = {}
            # Dictionaries are technically ordered in python 3.7,
            # So we're setting attributes & Properties in order
            # biomedicalConcept["id"] = super().default(o.id_)
            # biomedicalConcept["name"] = o.name
            # if o.label is not None and o.label != "":
            #     biomedicalConcept["label"] = o.label
            # else:
            #     raise ValueError("Label can't be Empty")
            # biomedicalConcept["synonyms"] = []
            # if o.synonyms is not None and len(o.synonyms) > 0:
            #     biomedicalConcept["synonyms"] = [value for value in o.synonyms if value]
            
            # biomedicalConcept["reference"] = o.reference
            # if o.category is not None and o.category != "":
            #     biomedicalConcept["category"] = o.category
            biomedicalConcept["properties"] = []
            print(f"{BColors.WARNING} BC ENCODER: NOT ADDING propeties yet!!{BColors.ENDC}")
            if hasattr(o, "properties") and o.properties is not None and len(o.properties) > 0:
                print("properties found")
            #     biomedicalConcept["properties"] = [super().default(prop) for prop in o.properties]
            if isinstance(o.code, AliasCode):
                print("Alias code found")
            biomedicalConcept["code"] = self.do_code(o.code)
            # biomedicalConcept["code"] = super().default(o.code)

            biomedicalConcept["notes"] = self.do_notes(o.notes)
            # biomedicalConcept["instanceType"] = o.INSTANCE_TYPE
            return biomedicalConcept
        # Let the base class default method raise the typeError
        return super().default(o)

class BiomedicalConceptPropertyEncoder(json.JSONEncoder):
    def default(self, o:BiomedicalConceptProperty):
        print(f"BiomedicalConceptPropertyEncoder encoding {o.__class__.__name__}")
        
        if isinstance(o, BiomedicalConceptProperty):
            # print(f"properties dict: {o.__dict__}")
            property_ = {}
            property_["id"] = super().default(o.id_)
            property_["name"] = o.name
            if o.label is not None and o.label != "":
                property_["label"] = o.label
            if hasattr(o, "is_required") and o.is_required is not None:
                property_["isRequired"] = o.is_required
            if hasattr(o, "is_enabled") and o.is_enabled is not None:
                property_["isEnabled"] = o.is_enabled
            property_["datatype"] = o.datatype
            property_["code"] = super().default(o.code)
            if hasattr(o, "notes") and o.notes is not None and o.notes.count() > 0:
                property_["notes"] = super().default(o.notes)
            if hasattr(o, "response_code") and o.response_codes is not None and len(o.response_codes) > 0:
                property_["responseCodes"] = super().default(o.response_codes)
            property_["instanceType"] = o.INSTANCE_TYPE
            return property_
        # Let the base class default method raise the typeError
        return super().default(o)

class ResponseCodeEncoder(json.JSONEncoder):
    def default(self, o):
        print(f"ResponseCodeEncoder: encoding {o.__class__.__name__}")
        
        if isinstance(o, ResponseCode):
            responseCode = {}
            responseCode["id"] = super().default(o.id_)
            # responseCode["id"] = json.dumps(o.id_,cl=UUIDEncoder)
            responseCode["name"] = o.name
            if o.label is not None and o.label != "":
                responseCode["label"] = o.label
            responseCode["isEnabled"] = o.is_enabled
            if hasattr(o, "code") and o.code is not None:
                responseCode["code"] = super().default(o.code)
            responseCode["instanceType"] = o.INSTANCE_TYPE
            return responseCode
        return super().default(o)

class USDMEncoder(
    RepositoryEncoder,
    IterEncoder,
    TherapeuticAreaEncoder,
    BiomedicalConceptCategoryEncoder,
    BiomedicalConceptEncoder,
    BiomedicalConceptPropertyEncoder,
    ResponseCodeEncoder,
    AliasCodeEncoder,
    CodeEncoder,
    CommentAnnotationEncoder,
    UUIDEncoder):
    def default(self, o):
        print(f"USDMEncoder: encoding {o.__class__.__name__}")
        return super().default(o)
