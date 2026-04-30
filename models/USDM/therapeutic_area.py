from uuid import UUID, uuid4 as guid

from models.USDM.biomedical_concept_category import BiomedicalConceptCategory
from models.USDM.biomedical_concept import BiomedicalConcept
from models.USDM.code import Code

class TherapeuticArea():
    # id_:guid = None => Stored in Code
    code:Code = None
    # INSTANCE_TYPE:str = Code.__qualname__
    __CODE_SYSTEM:str = "CUSTOM"
    __CODE_SYSTEM_VERSION:str = "00"

    child_categories:list[BiomedicalConceptCategory]
    child_bcs:list[BiomedicalConcept]
    
    def __init__(self, id_:UUID=None, code:Code=None, **kwargs):
        
        if id_ is None:
            id_=guid()

        if code is not None:
            self.code = code
        else:
            self.code = Code(code=f"TA_{id_.int}",
                            id_=id_,
                            code_system=TherapeuticArea.__CODE_SYSTEM,
                            code_system_version=TherapeuticArea.__CODE_SYSTEM_VERSION)
            if self.code is None:
                print(f"Set therapeutic area code to {self.code}, (id={id_})")
        self.child_categories:list[BiomedicalConceptCategory]= []
        if BiomedicalConceptCategory.__qualname__ in kwargs.keys():
            self.child_categories = kwargs[BiomedicalConceptCategory.__qualname__]
        
        if BiomedicalConcept.__qualname__ in kwargs.keys():
            self.child_bcs = kwargs[BiomedicalConcept.__qualname__]


        self.child_bcs:list[BiomedicalConcept]= []

        if "decode" in kwargs.keys():
            self.code.decode = kwargs["decode"]
    
    def set_decode(self, value:str=""):
        self.code.decode = value

    def get_decode(self):
        return self.code.decode
    
    def set_categories(self, categories:list[BiomedicalConceptCategory]) -> None:
        self.child_categories = categories
    
    def set_biomedical_concepts(self, biomedical_concepts:list[BiomedicalConcept]) -> None:
        self.child_bcs = biomedical_concepts

    def add_biomedical_concepts(self, biomedical_concepts:list[BiomedicalConcept]) -> None:
        self.child_bcs = self.child_bcs.extend(biomedical_concepts)
    
    def add_categories(self, biomedical_concepts:list[BiomedicalConcept]) -> None:
        self.child_bcs = self.child_bcs.extend(biomedical_concepts)

    @property
    def get_child_ids(self) -> list[UUID]:
        return [
            *[cat.id_ for cat in self.child_categories],
            *[bc.id_ for bc in self.child_bcs]
        ]
    