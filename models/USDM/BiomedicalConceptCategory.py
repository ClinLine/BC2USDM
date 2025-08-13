from dataclasses import dataclass
from models.CDISC.BiomedicalConceptCategory import BiomedicalConceptCategory as cdisk_category

@dataclass
class BiomedicalConceptCategory():
    id_:str
    name: str
    label:str = None
    description: str = None
    # code: AliasCode = None
    # notes: list[CommentAnnotation] = None
    # categories: list[BiomedicalConceptCategory] = None

    def __init__(self, id_, name, label, description):
        self.id_ = id_
        self.name = name
        self.label = label
        self.description = description
        # self.code = code
        # self.notes = notes
        # self.categories = categories

    @staticmethod
    def from_json(json:str):
        return BiomedicalConceptCategory(
            json["id_"],
            json["name"],
            json["label"],
            json["description"])

    @staticmethod
    def from_cdisc_category(cdisc_cat: cdisk_category):
        '''Function returning a USDM Biomedical Concept category,
        based on a provided CDISC Biomedical Concept category.

        '''
        return BiomedicalConceptCategory(
            cdisc_cat.links.self_.href.split("/")[-1], # id
            cdisc_cat.name, # name
            cdisc_cat.get_label(), # label
            "", # cdisc doesn't store descriptions for categories
            # code: ncit code here
            # TODO ask Berber if category type should go into notes
            # notes: I guess type would go here?
        )
