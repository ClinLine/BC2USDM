from dataclasses import dataclass
from models.CDISC.BiomedicalConceptCategory import BiomedicalConceptCategory as cdisk_category
from utils.utils import Encoding

@dataclass
class BiomedicalConceptCategory():
    id_:str
    name: str
    label:str = None
    description: str = None
    # code: AliasCode = None
    code:str = ""
    # notes: list[CommentAnnotation] = None
    notes:list[str] = None
    categories: list['BiomedicalConceptCategory'] = None
    categories:list[object] = None


    def __init__(self, id_, name:str, label:str, description:str=None, code=None, notes=None, children=None):
        self.id_ = id_
        self.name = "".join([name,id_])
        if label is None or label == "":
            self.label = Encoding.decode(name)
        else: self.label = label
        self.description = description
        self.code = code
        self.notes = notes
        self.categories = children


    @staticmethod
    def from_json(json:str):
        '''Function returns a BiomedicalConceptCategory based on a provided json string'''
        return BiomedicalConceptCategory(
            id_=json["_links"]["self"]["href"].split('=')[-1], #Undecoded id
            name=json["name"],
            label=json["name"],
            description="")

    @staticmethod
    def from_cdisc_category(cdisc_cat: cdisk_category):
        '''Function returning a USDM Biomedical Concept category,
        based on a provided CDISC Biomedical Concept category.
        '''
        id__=cdisc_cat.links.self_.href.split("=")[-1]
        return BiomedicalConceptCategory(
            id_=id__, # id
            name=cdisc_cat.name, # name
            label=cdisc_cat.get_label(), # label
            description=None # cdisc doesn't store descriptions for categories
            # TODO ask Berber if category type should go into notes
        )

    def to_csv(self, seperator:str=",", line_ending:str="\n\r"):
        '''Method to convert BiomedicalConceptCategory to cvs
        Optional parameter seperator determines what the properties are seperated by
        Optional parameter line_ending adds a line ending to the returned string.
        returns a string with all properties of the category seperated by seperator (default ',')
        '''
        # TODO: add code, notes and children
        result =  f"{self.id_}{seperator}{self.name}{seperator}{self.label}{seperator}{self.description}"
        if line_ending is not None and line_ending != "":
            result =  f"{result}{line_ending}"
        return result
