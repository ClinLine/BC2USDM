import json
from uuid import UUID
# from models.CDISC.BiomedicalConceptLink import BiomedicalConceptLink
from models.USDM.biomedical_concept import BiomedicalConcept
# from models.USDM.BiomedicalConceptCategory import BiomedicalConceptCategory as USDM_Category
from models.USDM.biomedical_concept_property import BiomedicalConceptProperty
from models.USDM.code.alias_code import AliasCode
from models.USDM.code.code import Code
from models.USDM.comment_annotation import CommentAnnotation
from models.USDM.response_code import ResponseCode
# from models.CDISC.BiomedicalConceptCategory import BiomedicalConceptCategory as CDISC_Category

class UUIDEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, UUID):
            return str(o)
        # Let the base class default method raise the typeError
        return super().default(o)

class CommentAnnotationEncoder(json.JSONEncoder):
    def default(self,o):
        if isinstance(o, CommentAnnotation):
            commentAnnotation = {}
            commentAnnotation["id"] = str(o.id_)
            commentAnnotation["text"] = o.text
            commentAnnotation["codes"] = super().default(o.codes)

            return commentAnnotation
        return super().default(o)

class IterEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            iterable = iter(o)
        except TypeError:
            pass
        else:
            return list(iterable)
        # Let the base class default metehod raise the TypeError
        return super().default(o)


class BiomedicalConceptEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, BiomedicalConcept):
            biomedicalConcept = {}
            # Dictionaries are technically ordered in python 3.7,
            # So we're setting attributes & Properties in order
            biomedicalConcept["id"] = str(o.id_)
            biomedicalConcept["name"] = o.name
            # TODO: Check with berber if she prefers empty attr or ommitted attr
            if o.label is not None and o.label != "":
                biomedicalConcept["label"] = o.label
            # TODO: empty or ommited?
            if o.synonyms is not None and len(o.synonyms) > 0:
                biomedicalConcept["synonyms"] = [value for value in o.synonyms]
            biomedicalConcept["reference"] = o.reference
            biomedicalConcept["code"] = super().default(o.code)
            if o.notes is not None and len(o.notes) > 0:
                biomedicalConcept["notes"] = super().default(o.notes)
            if o.category is not None and o.category != "":
                biomedicalConcept["category"] = o.category
            if hasattr(o, "properties") and o.properties is not None and len(o.properties) > 0:
                biomedicalConcept["properties"] = super().default(o.properties)
            return biomedicalConcept
        # Let the base class default method raise the typeError
        return super().default(o)

class BiomedicalConceptPropertyEncoder(json.JSONEncoder):
    def default(self, o:BiomedicalConceptProperty):
        if isinstance(o, BiomedicalConceptProperty):
            # print(f"properties dict: {o.__dict__}")
            property_ = {}
            property_["id"] = str(o.id_)
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
            return property_
        # Let the base class default method raise the typeError
        return super().default(o)

class ResponseCodeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ResponseCode):
            responseCode = {}
            responseCode["id"] = str(o.id_)
            responseCode["name"] = o.name
            if o.label is not None and o.label != "":
                responseCode["label"] = o.label
            responseCode["isEnabled"] = o.is_enabled
            if hasattr(o, "code") and o.code is not None:
                responseCode["code"] = super().default(o.code)
            return responseCode
        return super().default(o)

class CodeEncoder(json.JSONEncoder):
    def default (self, o):
        # if isinstance(o, (Code, AliasCode)):
        if isinstance(o, Code):
            try:
                code = {}
                code["id"] = str(o.id_)
                code["code"] = o.code
                if o.code_system is not None:
                    code["codeSystem"] = o.code_system
            except TypeError:
                print("Encountered a typeError while trying to encode a Code object.")
            else:
                # print(f"Returning Code: {code}")
                return code
        # Let the base class default method raise the typeError
        return super().default(o)

class AliasCodeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, AliasCode):
            try:
                aliasCode = {}
                aliasCode["id"] = str(o.id_)
                aliasCode["standardCode"] = super().default(o.standard_code)
                if o.standard_code_aliases is not None and len(o.standard_code_aliases)>0:
                    aliasCode["standardCodeAliases"] = super().default(o.standard_code_aliases)
            except TypeError:
                print("Encountered a typeError while trying to encode a AliasCode object.")
            else:
                # print(f"returning aliasCode: {aliasCode}")
                return aliasCode
        # Let the base class default method raise the typeError
        return super().default(o)

class USDMEncoder(
    BiomedicalConceptEncoder,
    BiomedicalConceptPropertyEncoder,
    ResponseCodeEncoder,
    AliasCodeEncoder,
    CodeEncoder,
    CommentAnnotationEncoder,
    UUIDEncoder,
    IterEncoder):
    
    def default(self, o):
        return super().default(o)
