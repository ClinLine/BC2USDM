from models.CDISC import AttributeNames
from utils.b_colors import BColors

class DataElementConceptDTO:
    concept_id:str
    label:str

    ncit_code:str = None
    href:str = None
    data_type:str = None
    example_set:list[str] = None

    def __init__(self, conceptId:str, shortName:str, **kwargs):
        keys = kwargs.keys()
        if conceptId is None or conceptId == "":
            raise AttributeError(f"{BColors.FAIL}conceptId attribute is required{BColors.ENDC}")
        else:
            self.concept_id = conceptId
        if AttributeNames.BiomedicalConcept.DataElementConcepts.ncit_code in keys:
            self.ncit_code = kwargs[AttributeNames.BiomedicalConcept.DataElementConcepts.ncit_code]
        if shortName is None or shortName == "":
            raise AttributeError(f"{BColors.FAIL}shortName attribute is required{BColors.ENDC}")
        else:
            self.label = shortName
        if AttributeNames.BiomedicalConcept.DataElementConcepts.reference in keys:
            self.href = kwargs[AttributeNames.BiomedicalConcept.DataElementConcepts.reference]
        if AttributeNames.BiomedicalConcept.DataElementConcepts.data_type in keys:
            self.data_type = kwargs[AttributeNames.BiomedicalConcept.DataElementConcepts.data_type]
        if AttributeNames.BiomedicalConcept.DataElementConcepts.example_set in keys:
            self.example_set = kwargs[AttributeNames.BiomedicalConcept.DataElementConcepts.example_set]
