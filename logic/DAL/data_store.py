from __future__ import annotations

# import abc
# from uuid import UUID, uuid4 as guid

# from models.USDM.biomedical_concept import BiomedicalConcept
# from models.USDM.biomedical_concept_category import BiomedicalConceptCategory
# from utils.b_colors import BColors

# class AbstractRepository(abc.ABC):
#     @abc.abstractmethod
#     def add(self, entity:object):
#         raise NotImplementedError

#     @abc.abstractmethod
#     def get(self, reference:str) -> object:
#         raise NotImplementedError
    
class DataStore:
    def __init__(self, path:str):
        print("Initializing datastore")