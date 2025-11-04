import json
from models.CDISC.BiomedicalConceptLink import BiomedicalConceptLink
from models.USDM.BiomedicalConceptCategory import BiomedicalConceptCategory as USDM_Category
from models.CDISC.BiomedicalConceptCategory import BiomedicalConceptCategory as CDISC_Category
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, USDM_Category):
            return {"id":obj.id_, "name":obj.name, "label":obj.label, "description":obj.description}
        if isinstance(obj, CDISC_Category):
            return {"name":obj.name, "_links": obj.links}
        if isinstance(obj, BiomedicalConceptLink):
            raise NotImplementedError("Converting BiomedicalConceptLinks to json isn't implemented yet")
        # Let the base class default method raise the typeError
        return super().default(obj)