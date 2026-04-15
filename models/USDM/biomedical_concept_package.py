import json
from uuid import uuid4 as guid

from models.USDM.code import Code
from models.USDM.code.alias_code import AliasCode
from models.USDM.biomedical_concept import BiomedicalConcept

class BiomedicalConceptPackage:
    id_:guid
    _biomedical_concepts:list["BiomedicalConcept"]

    _bc_codes:list[Code]
    #_name:str
    #_label:str
    #_title:str
    version:str
    #_effectiveDate:str
    reference:str
    INSTANCE_TYPE=__qualname__

    def __init__(self, json:str):
        self.guid = guid() # TODO: request guid from localStorage / DataManager
        self.reference = json["_links"]["self"]["href"]
        self.version = json["_links"]["self"]["href"].split('/')[-2]

        if len(json["_links"]["biomedicalConcepts"]) > 0:
            codes:list[Code] = []
            for bc in json["_links"]["biomedicalConcepts"]:
                code_string = bc["href"].split('\\')[-1]
                code_system = None
                if code_string[0] == "C":
                    code_system = "ncit"
                codes.append(Code(code_string,code_system=code_system))
            self._bc_codes = codes
            # self._biological_concepts = LocalStorage.get_bcs_by_code(codes)
        
    def get__biological_concepts(self):
        print("[BiologicalConceptPackage]: Are you sure you're setting the bcs?")
        raise NotImplementedError("This function is not implemented yet")

    def get_name(self):
        return f"Biomedical Concept Package {self.version}"

    def get_title(self):
        return f"Biomedical Concept Package Effective {self.version}"
    get_label = get_title

    def get_effectiveDate(self):
        return self.version
    
    def set_effective_date(self, version:str):
        self.version = version

    def get_biomedical_concepts(self, ids:list[guid]=None, codes:list[Code|AliasCode]=None):
        """getter for package's biomedical concepts"""
        if ids is None and codes is None:
            raise ValueError("Please provide a list of guids or Codes or AliasCodes")
        
        bcs:list[BiomedicalConcept]
        raise NotImplementedError()