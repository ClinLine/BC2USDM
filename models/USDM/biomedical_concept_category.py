from __future__ import annotations

from dataclasses import dataclass
from uuid import uuid4 as guid, UUID
from models.CDISC.BiomedicalConceptCategory import BiomedicalConceptCategory as cdisk_category
from models.USDM.code.alias_code import AliasCode
from models.USDM.comment_annotation import CommentAnnotation
from utils.b_colors import BColors
# from utils.utils import Encoding

@dataclass
class BiomedicalConceptCategory():
    INSTANCE_TYPE = __qualname__
    id_:UUID
    name:str
    label:str = None
    description: str = None
    code:AliasCode = None
    notes:list[CommentAnnotation] = None
    notes:list[str] = None
    # Child categories:
    children:list[BiomedicalConceptCategory] = None
    # member concepts: -> Use dict instead?
    members:list["BiomedicalConcept"] = None
    # categories:list[object] = None


    def __init__(self, id_, name:str=None, label:str = None, description:str=None, code=None, notes=None, children=None):
        # Default populated params are: label, description & code, where description title
        self.id_ = guid()
        if label is None or label != "":
            self.label = label
        self.name = f"{label.replace(" ","")}_{self.id_.int}"
        self.description = description
        if isinstance(code, str):
            print(f"Didn't expect code to be a string ({code}), using label instead")
            #CDISK categories don't have a code currently, they use the encoded name as id
            self.code = AliasCode(label.encode(), check_code=False)
        else: 
            if isinstance(code, (AliasCode)):
                self.code = code
            else:
                print(f"Code differed from expected type ({AliasCode.__qualname__}), type = {type(code)}")
        self.notes = notes
        self.categories = children
        self.code.decode = label
        self.members:list["BiomedicalConcept"] = []

    def get_code(self):
        if self.code.standard_code.code is not None:
            return self.code.standard_code.code

    @staticmethod
    def from_json(json:str):
        '''Function returns a BiomedicalConceptCategory based on a provided json string'''
        return BiomedicalConceptCategory(
            id_=None,
            code=AliasCode(json["_links"]["self"]["href"].split('=')[-1], check_code=False), #Undecoded id
            # id_=json["_links"]["self"]["href"].split('=')[-1], #Undecoded id
            # name=json["name"],
            label=json["name"],
            description=json["_links"]["self"]["title"])

    @staticmethod
    def from_cdisc_category(cdisc_cat: cdisk_category):
        '''Function returning a USDM Biomedical Concept category,
        based on a provided CDISC Biomedical Concept category.
        '''
        id__ = cdisc_cat.links.self_.href.split("=")[-1]
        return BiomedicalConceptCategory(
            id_=id__, # id
            name=cdisc_cat.name, # name
            label=cdisc_cat.get_label(), # label
            description=None # cdisc doesn't store descriptions for categories
        )

    @staticmethod
    def from_short_name(short_name:str):
        print(f"{BColors.WARNING}[Warning]: USDM.BiomedicalConceptCategory: returning categories is not implemented yet, returning string{BColors.ENDC}")
        return short_name