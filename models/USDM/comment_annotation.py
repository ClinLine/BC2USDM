from dataclasses import dataclass, field
from uuid import UUID, uuid4 as guid
from models.USDM.code.code import Code


@dataclass
class CommentAnnotation:
    '''Comment annotations for Biological Concepts or Biological Concept Properties'''
    id_:UUID
    text:str
    codes: list[Code] = field(default_factory=list['Code'])

    def __init__(self, text:str, id_:str = None, codes:list[Code] = None):
        '''CommentAnnotation constructor'''
        if id_ is None or id_ == "":
            self.id_ = guid()
        else:
            self.id_ = id_
        self.text = text
        if codes is not None and len(codes)>0:
            if isinstance(codes[0],str):
                self.codes = [Code(code) for code in codes]
            elif isinstance(codes[0], Code):
                self.codes = list(codes)
