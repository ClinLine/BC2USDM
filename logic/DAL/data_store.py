from __future__ import annotations

from uuid import UUID, uuid4 as guid

from models.USDM.biomedical_concept import BiomedicalConcept
from models.USDM.biomedical_concept_category import BiomedicalConceptCategory

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class DataStore(metaclass=Singleton):
    PATH:str
    biomedical_concepts:dict[UUID,BiomedicalConcept]
    categories:dict[UUID, BiomedicalConceptCategory]

    def __init__(self, path):
        ''' TODO:
        - Check if files exist
        - Read data from files
        - validate cache (use package version?) : /mdr/bc/packages/2022-10-26/biomedicalconcepts/C49676",
        '''
        super().__init__()
        self.PATH = path

        
        #TODO: init Repository
            #TODO: init TherepeuticAreas
            #TODO: init Categories
        
        #TODO: Init cache:
            #TODO: init BiomedicalConcepts
            #TODO: init Categories
            # init Packages? - low prio 

    #region BiomedicalConcept
    
    
    # region

