from __future__ import annotations

from uuid import UUID, uuid4 as guid

from models.USDM.biomedical_concept import BiomedicalConcept
from models.USDM.biomedical_concept_category import BiomedicalConceptCategory
from utils.b_colors import BColors

class AbstractRepository(abc.ABC):
    @abc.abstractmeethod
    def add(self, batch:model.Batch):
        ...

    @abc.abstractmethod
    def get(self, reference) -> model.Batch:
        ...