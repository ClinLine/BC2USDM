from dataclasses import dataclass, field
from uuid import UUID, uuid4 as guid

from models.USDM.code import Code
from utils.b_colors import BColors


class CommentAnnotation:
    '''Comment annotations for Biological Concepts or Biological Concept Properties'''
    id_:UUID
    text:str
    codes: list[Code]
    INSTANCE_TYPE = __qualname__

    def __init__(self, text:str, id_:str = None, codes:list[Code] = None):
        '''CommentAnnotation constructor'''
        if id_ is None or id_ == "":
            self.id_ = guid()
        else:
            self.id_ = id_
        self.text = text
        self.codes = []
        if codes is not None and len(codes)>0:
            if isinstance(codes[0],str):
                self.codes = [Code(code) for code in codes]
            elif isinstance(codes[0], Code):
                self.codes = codes

    @staticmethod
    def find_definition(comment_annotations:list["CommentAnnotation"]):
        if comment_annotations is None: 
            return None
        for ca in comment_annotations:
            for code in ca.codes:
                if code.code == code.DEFINITION.code:
                    return ca
        print(f"{BColors.WARNING}[Warning]: Didn't find a Defninition in notes{BColors.ENDC}")
        return None
    
    # def __eq__(self, value):
    #     # TODO: Since Comment annotations are entities, not datatypes, __eq__ should technically only compaire IDs
    #     if self.id_ != value.id_: 
    #         print(f"{BColors.WARNING}Warning: CommentAnnotation.eq: ids are not equal{BColors.ENDC}")
    #         print("Id inequality is currently being disregarded since they can't be changed by the user")
            
    #     if self.text != value.text: return False
    #     if self.codes != value.codes:
    #         # Not testing codes atm since they can't be changed by the user
    #         print(f"{BColors.WARNING}Warning: CommentAnnotation.eq: Codes are not equal{BColors.ENDC}")
    #         print("Code inequality is currently being disregarded since they can't be changed by the user")
    #     return True
