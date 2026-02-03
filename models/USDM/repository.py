from uuid import UUID, uuid4
from models.USDM.biomedical_concept_category import BiomedicalConceptCategory
from models.USDM.biomedical_concept import BiomedicalConcept
from models.USDM.code.code import Code
from models.USDM.comment_annotation import CommentAnnotation
from models.USDM.therapeutic_area import TherapeuticArea


class Repository:

    business_therapeutic_areas:list[TherapeuticArea] = None
    bc_categories:list[BiomedicalConceptCategory] = None
    biomedical_concepts:dict[UUID,BiomedicalConcept] = None

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

    def add_category(self, category:BiomedicalConceptCategory):
        if self.bc_categories is None or len(self.bc_categories) == 0:
            self.bc_categories = []
        self.bc_categories.append(category)

    def add_biomedical_concept(self, biomedical_concept:BiomedicalConcept):
        self.biomedical_concepts.insert(biomedical_concept.id_,biomedical_concept)

    def set_biomedical_concept(self, bc_id:UUID, biomedical_concept:BiomedicalConcept):
        self.biomedical_concepts.update(bc_id, biomedical_concept)

    def update_biomedical_concept(self, data:dict[UUID, dict[str,any]], id_:UUID):
        old_bc = self.biomedical_concepts[id_]
        old_bc.name=data[id_]["name"]
        if len(old_bc.synonyms) == len(data[id_]["synonyms"]):
            old_bc.synonyms = data[id_]["synonyms"]
        else:
            raise NotImplementedError("New synonyms aren't implemented yet")
        
        if len(old_bc.notes) == len (data[id_]["notes"]):
            for index, value in old_bc.notes:
                if value.text != data[id_]["notes"][index]:
                    # change text
                    value.text = data[id_]["notes"][index]
                    # Create new custom code from last 8 digits of previous ID and give new ID
                    value.code = Code(code=f"BCN-{value.id_[-9:-1]}", code_system="CUSTOM", id_=uuid4()) # create code
                    value.id_ = uuid4()
        
        else:
            # Walk notes
            match_index:int = 0
            notes:CommentAnnotation = []
            for index, value in data[id_]["notes"]:
                for i in range(match_index,old_bc.notes):
                    if value.text == old_bc.notes[i].text:
                        notes.append(old_bc.notes[i])
                        match_index = i
                    else:
                        new_id = uuid4()
                        notes.append(CommentAnnotation(
                            text=value.text, 
                            id_=new_id,
                            codes=[
                                Code(
                                    code=f"BCN-{str(new_id)[-9:-1]}",
                                    id_=uuid4(),
                                    code_system="CUSTOM",
                                    code_system_version=self.business_therapeutic_areas[0].code.code_system_version)]))
                        

                    
                
                
                

        old_bc.properties
        # compair property
        # set property
