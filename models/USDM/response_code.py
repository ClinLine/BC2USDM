from dataclasses import dataclass
from uuid import uuid4 as guid

from models.USDM.code.code import Code


@dataclass
class ResponseCode():
    id_:guid
    name: str
    is_enabled: bool
    code:Code
    label: str = None

    def __init__(self, id_:guid=None, name:str=None, enabled:bool=None, code:Code=None, label:str=None):
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
            print("Grabbing exampleset details is not yet supported, only setting label, name and id")
            self.label = name
        self.id_ = guid()
            
        # if id_ is None or id_ == "":
        #     self.code = Code(id_)
        self.name = f"{name}_{self.id_}"
        self.label = label
        self.is_enabled = enabled
        if isinstance(code,str):
            self.code = Code(code)
        else: self.code = Code

    @staticmethod
    def from_example_set(json_str:list[str]):
        # result:ResponseCode = []
        # for name in jsonStr:
        #     result.append( ResponseCode(name=name))
        # return result

        return [ResponseCode(name=string) for string in json_str]
