from dataclasses import dataclass
import json

from models.CDISC.BiomedicalConceptLink import BiomedicalConceptLink
# from BiomedicalConceptLink import BiomedicalConceptLink
__package__ = "models.CDISC"

@dataclass
class BiomedicalConceptCategory:
    name: str
    links: BiomedicalConceptLink

    def __init__(self, name, bcl: BiomedicalConceptLink):
        self.name = name
        self.links = bcl

    def get_label(self):
        return f"Biomedical Concept Category ({self.name})"
    
    def get_description(self):
        raise NotImplementedError("No description has been found for this Category")
        return f"No description has been found for this Category"
    
    @staticmethod
    def categories_from_json(json):
        categories:list[BiomedicalConceptCategory] = []
        for category in json:
            result = BiomedicalConceptCategory(
                name=category["name"],
                bcl = BiomedicalConceptLink.from_json(category["_links"])
            )
            categories.append(result)
        return categories
