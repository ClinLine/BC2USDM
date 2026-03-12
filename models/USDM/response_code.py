from dataclasses import dataclass
from uuid import uuid4 as guid

from models.USDM.code import Code, Example as ExampleCode


@dataclass
class ResponseCode():
    id_:guid
    name: str
    is_enabled: bool
    code:Code
    label: str = None

    def __init__(self, id_:guid=None, name:str=None, enabled:bool=False, code:Code=None, label:str=None):
        """
        curl -X 'GET' \
            'https://api-evsrest.nci.nih.gov/api/v1/concept/search?terminology=ncit&term=Blood&type=contains&include=minimal&fromRecord=0&pageSize=10' \
            -H 'accept: application/json
        responseBody: #Code: 200
            {
                "total": 5512,
                "timeTaken": 39,
                "parameters": {
                    "term": "Blood",
                    "type": "contains",
                    "include": "minimal",
                    "fromRecord": 0,
                    "pageSize": 10,
                    "terminology": [
                    "ncit"
                    ]
                },
                "concepts": [
                    {
                    "code": "C12434",
                    "name": "Blood",
                    "terminology": "ncit",
                    "version": "25.10d",
                    "conceptStatus": "DEFAULT",
                    "leaf": true,
                    "active": true
                    },
                    {
                    "code": "C22559",
                    "name": "Mouse Blood",
                    "terminology": "ncit",
                    "version": "25.10d",
                    "conceptStatus": "DEFAULT",
                    "leaf": true,
                    "active": true
                    },
                    {
                    "code": "C17610",
                    "name": "Blood Sample",
                    "terminology": "ncit",
                    "version": "25.10d",
                    "conceptStatus": "DEFAULT",
                    "leaf": false,
                    "active": true
                    },
                    {
                    "code": "C212554",
                    "name": "Blood Service Type",
                    "terminology": "ncit",
                    "version": "25.10d",
                    "conceptStatus": "DEFAULT",
                    "leaf": true,
                    "active": true
                    },
                    {
                    "code": "C19448",
                    "name": "Blood and Blood Products",
                    "terminology": "ncit",
                    "version": "25.10d",
                    "conceptStatus": "DEFAULT",
                    "leaf": false,
                    "active": true
                    },
                    {
                    "code": "C15657",
                    "name": "Blood Treatment",
                    "terminology": "ncit",
                    "version": "25.10d",
                    "conceptStatus": "DEFAULT",
                    "leaf": false,
                    "active": true
                    },
                    {
                    "code": "C172593",
                    "name": "Blood Ultrafiltration",
                    "terminology": "ncit",
                    "version": "25.10d",
                    "conceptStatus": "DEFAULT",
                    "leaf": true,
                    "active": true
                    },
                    {
                    "code": "C219068",
                    "name": "Blood Unit",
                    "terminology": "ncit",
                    "version": "25.10d",
                    "conceptStatus": "DEFAULT",
                    "leaf": true,
                    "active": true
                    },
                    {
                    "code": "C27083",
                    "name": "Blood Clot",
                    "terminology": "ncit",
                    "version": "25.10d",
                    "conceptStatus": "DEFAULT",
                    "leaf": false,
                    "active": true
                    },
                    {
                    "code": "C61009",
                    "name": "Blood Type",
                    "terminology": "ncit",
                    "version": "25.10d",
                    "conceptStatus": "DEFAULT",
                    "leaf": true,
                    "active": true
                    }
                ]
}
"""
        if name is not None and (enabled is None and code is None and label is None):
            # print("Grabbing exampleset details is not yet supported, only setting label, name and id")
            self.label = name
        self.id_ = guid()
        self.label = label
        if name is not None and self.label is None:
            self.label = name
        if name is not None and label is not None:
            print(f"[ResponseCode.init]: Expected name or label to be {None}")
            raise ValueError(f"[ResponseCode.init]: Expected name or label to be {None}")
        self.name = f"{self.label}_{self.id_}"
        self.is_enabled = enabled
        if isinstance(code,str):
            self.code = Code(code)
        elif isinstance(code, Code):
            self.code = Code
        else: self.code = None
    @staticmethod
    def from_example_set(json_str:list[str]):
        return [ResponseCode(name=string,code=ExampleCode) for string in json_str]