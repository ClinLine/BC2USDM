from models.USDM.biomedical_concept_category import BiomedicalConceptCategory
from models.USDM.biomedical_concept import BiomedicalConcept
from models.USDM.therapeutic_area import TherapeuticArea


class Repository:

    business_therapeutic_areas:list[TherapeuticArea] = None
    bc_categories:list[BiomedicalConceptCategory] = None
    biomedical_concepts:list[BiomedicalConcept] = None

    def __init__(self, **kwargs):

        keys = kwargs.keys()
        if "business_therapeutic_areas" in keys:
            if isinstance(kwargs["business_therapeutic_areas"], TherapeuticArea):
                self.business_therapeutic_areas = [kwargs["business_therapeutic_areas"]]
            elif isinstance(kwargs["business_therapeutic_areas"], list[TherapeuticArea]):
                self.business_therapeutic_areas = kwargs["business_therapeutic_areas"]
        else:
            self.business_therapeutic_areas = [TherapeuticArea()]

        if "bc_categories" in keys:
            if isinstance(kwargs["bc_categories"], BiomedicalConceptCategory):
                self.bc_categories = [kwargs["bc_categories"]]
            elif isinstance(kwargs["bc_categories"], list[BiomedicalConceptCategory]):
                self.bc_categories = kwargs["bc_categories"]
        else:
            self.bc_categories = []

        if "biomedical_concepts" in keys:
            if isinstance(kwargs["biomedical_concepts"], BiomedicalConcept):
                self.biomedical_concepts = [kwargs["biomedical_concepts"]]
            elif isinstance(kwargs["biomedical_concepts"], list[BiomedicalConcept]):
                self.biomedical_concepts = kwargs["biomedical_concepts"]
        else:
            self.biomedical_concepts = []

    
        