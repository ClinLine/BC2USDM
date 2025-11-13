from dataclasses import dataclass, field
from uuid import uuid4 as guid
from models.USDM.code.code import Code


@dataclass
class CommentAnnotation:
    '''Comment annotations for Biological Concepts or Biological Concept Properties'''
    id_:str
    text:str
    codes: list[Code] = field(default_factory=list['Code'])

    def __init__(self, id_:str, text:str, codes:list[Code]):
        '''CommentAnnotation constructor'''
        if id_ is None or id_ == "":
            self.id_ = guid()
        else:
            self.id_ = id_
        self.text = text
        self.codes = [Code(code) for code in codes]
