from dataclasses import dataclass

__package__ = "models.CDISC"

@dataclass
class Link():
    href: str
    title: str
    type: str

    def __init__(self, *args):
        if isinstance(args, tuple):
            # print(args)
            self.href = args[0]["href"]
            self.title = args[0]["title"]
            self.type = args[0]["type"]
        else:
            self.href = dict(args)["href"]
            self.href = dict(args)["title"]
            self.href = dict(args)["type"]

    def from_json(self, json:str):
        return Link((
            json["href"],
            json["title"],
            json["type"])
        )

@dataclass
class BiomedicalConceptLink():
    parentBiomedicalConcept: Link = None
    parentPackage: Link = None
    self_: Link = None

    def __init__(self, parent_bc:Link=None, parent_package:Link=None, self_:Link=None):
        self.parentBiomedicalConcept = parent_bc
        self.parentPackage = parent_package
        self.self_ = self_

    @staticmethod
    def from_json(json_string: str):
        '''Take in a json string and converts returns a (CDISC) Biomedical Concept Category
        '''
        if "parentBiomedicalConcept" in json_string.keys():
            parent_biomedical_concept = Link(json_string["parentBiomedicalConcept"])
        else:
            parent_biomedical_concept = None
        if "parentPackage" in json_string.keys():
            package = Link(json_string["parentPackage"])
        else:
            package = None
        if "self" in json_string.keys():
            self_ = Link(json_string["self"])
        else:
            self_=None

        return BiomedicalConceptLink(
            parent_bc=parent_biomedical_concept,
            parent_package=package,
            self_=self_
        )
