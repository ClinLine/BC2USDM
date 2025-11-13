import json
from models.CDISC.BiomedicalConceptLink import BiomedicalConceptLink
from models.USDM.BiomedicalConcept import BiomedicalConcept, BiomedicalConceptProperty, ResponseCode
from models.USDM.BiomedicalConceptCategory import BiomedicalConceptCategory as USDM_Category
from models.CDISC.BiomedicalConceptCategory import BiomedicalConceptCategory as CDISC_Category

class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, USDM_Category):
            return {"id":o.id_, "name":o.name, "label":o.label, "description":o.description}
        if isinstance(o, CDISC_Category):
            return {"name":o.name, "_links": o.links}
        if isinstance(o, BiomedicalConceptLink):
            raise NotImplementedError("Converting BiomedicalConceptLinks to json isn't implemented yet")
        # Let the base class default method raise the typeError
        return super().default(o)
    
class BiomedicalConceptEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, BiomedicalConcept):
            bc_dict = {}
            # Dictionaries are technically ordered in python 3.7,
            # So we're setting attributes & Properties in order
            bc_dict["id"] = o.id_
            bc_dict["name"] = o.name
            # TODO: Check with berber if she prefers empty attr or ommitted attr
            if o.label is not None and o.label != "":
                bc_dict["label"] = o.label
            # TODO: empty or ommited?
            if o.synonyms is not None and len(o.synonyms) > 0:
                bc_dict["synonyms"] = [value for value in o.synonyms]
            bc_dict["reference"] = o.reference
            bc_dict["code"] = json.dumps(o.code)
            if o.notes is not None and o.notes.count > 0:
                bc_dict["notes"] = json.dumps(o.notes)
            if o.category is not None and o.category != "":
                bc_dict["category"] = o.category
            if o.properties is not None and len(o.properties) > 0:
                bc_dict["properties"] = json.dumps(o.properties)
            return bc_dict
        # Let the base class default method raise the typeError
        return super().default(o)

class BiomedicalConceptPropertyEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, BiomedicalConceptProperty):
            prop_dict = {}
            prop_dict["id"] = o.id_
            prop_dict["name"] = o.name
            if o.label is not None and o.label != "":
                prop_dict["label"] = o.label
            prop_dict["isRequired"] = o.is_required
            prop_dict["isEnabled"] = o.is_enabled
            prop_dict["datatype"] = o.datatype
            prop_dict["code"] = json.dumps(o.code)
            if o.notes is not None and o.notes.count() > 0:
                prop_dict["notes"] = [value for value in o.notes]
            if o.response_codes is not None and o.response_codes.count()  > 0:
                prop_dict["responseCodes"] = [
                    json.dumps(code, cls=ResponseCodeEncoder) for code in o
                ]
            return prop_dict
        # Let the base class default method raise the typeError
        return super().default(o)

class ResponseCodeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ResponseCode):
            rc = {}
            rc["id"] = o.id_
            rc["name"] = o.name
            if o.label is not None and o.label != "":
                rc["label"] = o.label
            rc["isEnabled"] = o.is_enabled
            rc["code"] = json.dumps(o.code)
            return rc
        return super().default(o)

class IterableEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            iterable = iter(o)
        except TypeError:
            pass
        else:
            return list(iterable)
        super().default(o)

class GenericAliasEncoder(json.JSONEncoder):
    def default(self, o):
        print(o.__dict__)
        if isinstance(o, type["GenericAlias"]):
            print("HALP!!!!")


# class CodeEncoder(json.JSONEncoder):
#     def default (self, o):
#         # if isinstance(o, (Code, AliasCode)):
#         try:
#             code = {}

                
#         except TypeError:
#             pass
#         else:
#             return code
#         return super().default(o)
