import json
from uuid import uuid4 as guid

from models.USDM.code.code import Code
from models.USDM.code.alias_code import AliasCode
from models.USDM.BiomedicalConcept import BiomedicalConcept

class BiomedicalConceptPackage:
    id_:guid
    _biomedical_concepts:list["BiomedicalConcept"]

    _bc_codes:list[Code]
    #_name:str
    #_label:str
    #_title:str
    version:str
    #_effectiveDate:str
    reference:str

    def __init__(self, json:str):
        self.guid = guid() # TODO: request guid from localStorage / DataManager
        self.reference = json["_links"]["self"]["href"]
        self.version = json["_links"]["self"]["href"].split('/')[-2]

        if len(json["_links"]["biomedicalConcepts"]) > 0:
            codes:list[Code] = []
            for bc in json["_links"]["biomedicalConcepts"]:
                code_string = bc["href"].split('\\')[-1]
                code_system = None
                if code_string[0] == "C":
                    code_system = "ncit"
                codes.append(Code(code_string,code_system=code_system))
            self._bc_codes = codes
            # self._biological_concepts = LocalStorage.get_bcs_by_code(codes)
        
    def get__biological_concepts(self):
        print("[BiologicalConceptPackage]: Are you sure you're setting the bcs?")


    def get_name(self):
        return f"Biomedical Concept Package {self.version}"

    def get_title(self):
        return f"Biomedical Concept Package Effective {self.version}"
    get_label = get_title

    def get_effectiveDate(self):
        return self.version
    
    def set_effective_date(self, version:str):
        self.version = version

    def get_biomedical_concepts(self, ids:list[guid]=None, codes:list[Code|AliasCode]=None):
        """getter for package's biomedical concepts"""
        if ids is None and codes is None:
            raise ValueError("Please provide a list of guids or Codes or AliasCodes")
        
        bcs:list[BiomedicalConcept]
        raise NotImplementedError()
        # if ids is not None:
        #     bcs = LocalStorage.get_bcs_by_id(ids)
        # else:
        #     bcs = LocalStorage.get_bcs_by_code(codes)
        # return bcs
        
        # raise RuntimeError("Something unexpected went wrong in the Package.get_biomedical_concepts method")

    # @staticmethod
    # def from_json(json, *args, **kws):
    #     # Package default json
    #     """
    #     {
    #         "_links": {
    #             "biomedicalConcepts": [{
    #                 "href": "/mdr/bc/packages/2022-10-26/biomedicalconcepts/C49676",
    #                 "title": "Pulse rate",
    #                 "type": "Biomedical Concept"
    #             }],
    #             "self": {
    #                 "href": "/mdr/bc/packages/2022-10-26/biomedicalconcepts",
    #                 "title": "Biomedical Concepts",
    #                 "type": "Biomedical Concept List"
    #             }
    #         },
    #         "name": "Biomedical Concepts 2022-10-26",
    #         "label": "Biomedical Concept Package Effective 2022-10-26",
    #         "effectiveDate": "2022-10-26",
    #         "version": "2022-10-26"
    #     }
    #     """
    #     # package part of BC:
    #     """
    #      "parentPackage": {
    #         "href": "/mdr/bc/packages/2022-10-26/biomedicalconcepts",
    #         "title": "Biomedical Concept Package Effective 2022-10-26",
    #         "type": "Biomedical Concept Package"
    #     """

        

    #     super().__init__(*args, **kws)
    #     prop =  super().__getstate__()
    #     return 
    

    @staticmethod
    def test():
        jsonstr ="""{
            "_links": {
                "biomedicalConcepts": [{
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100106",
                    "title": "ADAS-Cog CDISC Version Functional Test Question",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100177",
                    "title": "CDISC ADAS-Cog - Word Recall Average Score",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100178",
                    "title": "CDISC ADAS-Cog - Word Recall Trial 1 Subscore",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100179",
                    "title": "CDISC ADAS-Cog - Word Recall Trial 2 Subscore",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100180",
                    "title": "CDISC ADAS-Cog - Word Recall Trial 3 Subscore",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100181",
                    "title": "CDISC ADAS-Cog - Word Recall: Word 1",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100182",
                    "title": "CDISC ADAS-Cog - Word Recall: Word 2",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100762",
                    "title": "Alzheimer's Disease Assessment Scale-Cognitive CDISC Version Functional Test",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C118969",
                    "title": "Clinical or Research Assessment Classification",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C211913",
                    "title": "CDISC QRS Instruments Questions",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C81250",
                    "title": "Functional Assessment",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C91102",
                    "title": "Clinical or Research Assessment Question",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C91105",
                    "title": "Clinical or Research Assessment Questionnaire",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C115409",
                    "title": "6MWT Functional Test Question",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C115789",
                    "title": "6 Minute Walk Functional Test",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C115800",
                    "title": "6MWT - Distance at 1 Minute",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C115801",
                    "title": "6MWT - Distance at 2 Minutes",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C115802",
                    "title": "6MWT - Distance at 3 Minutes",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C115803",
                    "title": "6MWT - Distance at 4 Minutes",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C115804",
                    "title": "6MWT - Distance at 5 Minutes",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C115805",
                    "title": "6MWT - Distance at 6 Minutes",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100183",
                    "title": "CDISC ADAS-Cog - Word Recall: Word 3",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100184",
                    "title": "CDISC ADAS-Cog - Word Recall: Word 4",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100185",
                    "title": "CDISC ADAS-Cog - Word Recall: Word 5",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100186",
                    "title": "CDISC ADAS-Cog - Word Recall: Word 6",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100187",
                    "title": "CDISC ADAS-Cog - Word Recall: Word 7",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100188",
                    "title": "CDISC ADAS-Cog - Word Recall: Word 8",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100189",
                    "title": "CDISC ADAS-Cog - Word Recall: Word 9",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100190",
                    "title": "CDISC ADAS-Cog - Word Recall: Word 10",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100191",
                    "title": "CDISC ADAS-Cog - Naming Objects and Fingers Summary Score",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100192",
                    "title": "CDISC ADAS-Cog - Naming Objects and Fingers: 1",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100193",
                    "title": "CDISC ADAS-Cog - Naming Objects and Fingers: 2",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100194",
                    "title": "CDISC ADAS-Cog - Naming Objects and Fingers: 3",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100195",
                    "title": "CDISC ADAS-Cog - Naming Objects and Fingers: 4",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100196",
                    "title": "CDISC ADAS-Cog - Naming Objects and Fingers: 5",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100197",
                    "title": "CDISC ADAS-Cog - Naming Objects and Fingers: 6",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100198",
                    "title": "CDISC ADAS-Cog - Naming Objects and Fingers: 7",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100199",
                    "title": "CDISC ADAS-Cog - Naming Objects and Fingers: 8",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100200",
                    "title": "CDISC ADAS-Cog - Naming Objects and Fingers: 9",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100201",
                    "title": "CDISC ADAS-Cog - Naming Objects and Fingers: 10",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100202",
                    "title": "CDISC ADAS-Cog - Naming Objects and Fingers: 11",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100203",
                    "title": "CDISC ADAS-Cog - Naming Objects and Fingers: 12",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100204",
                    "title": "CDISC ADAS-Cog - Naming Objects and Fingers: Thumb",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100205",
                    "title": "CDISC ADAS-Cog - Naming Objects and Fingers: Pointer",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100206",
                    "title": "CDISC ADAS-Cog - Naming Objects and Fingers: Middle",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100207",
                    "title": "CDISC ADAS-Cog - Naming Objects and Fingers: Ring",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100208",
                    "title": "CDISC ADAS-Cog - Naming Objects and Fingers: Pinky",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100209",
                    "title": "CDISC ADAS-Cog - Commands Summary Score",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100210",
                    "title": "CDISC ADAS-Cog - Commands: Fist",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100211",
                    "title": "CDISC ADAS-Cog - Commands: Ceiling",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100212",
                    "title": "CDISC ADAS-Cog - Commands: Pencil",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100213",
                    "title": "CDISC ADAS-Cog - Commands: Watch",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100214",
                    "title": "CDISC ADAS-Cog - Commands: Shoulder",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100215",
                    "title": "CDISC ADAS-Cog - Delayed Word Recall Summary Score",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100216",
                    "title": "CDISC ADAS-Cog - Delayed Word Recall: Word 1",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100217",
                    "title": "CDISC ADAS-Cog - Delayed Word Recall: Word 2",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100218",
                    "title": "CDISC ADAS-Cog - Delayed Word Recall: Word 3",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100219",
                    "title": "CDISC ADAS-Cog - Delayed Word Recall: Word 4",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100220",
                    "title": "CDISC ADAS-Cog - Delayed Word Recall: Word 5",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100221",
                    "title": "CDISC ADAS-Cog - Delayed Word Recall: Word 6",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100222",
                    "title": "CDISC ADAS-Cog - Delayed Word Recall: Word 7",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100223",
                    "title": "CDISC ADAS-Cog - Delayed Word Recall: Word 8",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100224",
                    "title": "CDISC ADAS-Cog - Delayed Word Recall: Word 9",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100225",
                    "title": "CDISC ADAS-Cog - Delayed Word Recall: Word 10",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100226",
                    "title": "CDISC ADAS-Cog - Constructional Praxis Summary Score",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100227",
                    "title": "CDISC ADAS-Cog - Constructional Praxis: Circle",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100228",
                    "title": "CDISC ADAS-Cog - Constructional Praxis: 2 Rectangles",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100229",
                    "title": "CDISC ADAS-Cog - Constructional Praxis: Diamond",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100230",
                    "title": "CDISC ADAS-Cog - Constructional Praxis: Cube",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100231",
                    "title": "CDISC ADAS-Cog - Attempt to Draw",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100232",
                    "title": "CDISC ADAS-Cog - Ideational Praxis Summary Score",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100233",
                    "title": "CDISC ADAS-Cog - Ideational Praxis: Fold",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100234",
                    "title": "CDISC ADAS-Cog - Ideational Praxis: Insert",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100235",
                    "title": "CDISC ADAS-Cog - Ideational Praxis: Seal",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100236",
                    "title": "CDISC ADAS-Cog - Ideational Praxis: Address",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100237",
                    "title": "CDISC ADAS-Cog - Ideational Praxis: Stamp",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100238",
                    "title": "CDISC ADAS-Cog - Orientation Summary Score",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100239",
                    "title": "CDISC ADAS-Cog - Orientation: Full Name",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100240",
                    "title": "CDISC ADAS-Cog - Orientation: Month",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100241",
                    "title": "CDISC ADAS-Cog - Orientation: Date",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100242",
                    "title": "CDISC ADAS-Cog - Orientation: Year",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100243",
                    "title": "CDISC ADAS-Cog - Orientation: Day of Week",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100244",
                    "title": "CDISC ADAS-Cog - Orientation: Season",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100245",
                    "title": "CDISC ADAS-Cog - Orientation: Place",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100246",
                    "title": "CDISC ADAS-Cog - Orientation: Time",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100247",
                    "title": "CDISC ADAS-Cog - Word Recognition Summary Score",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100248",
                    "title": "CDISC ADAS-Cog - Word Recognition Trial 1 Summary Score",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100249",
                    "title": "CDISC ADAS-Cog - Word Recognition Trial 2 Summary Score",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100250",
                    "title": "CDISC ADAS-Cog - Word Recognition Trial 3 Summary Score",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100251",
                    "title": "CDISC ADAS-Cog - Word Recognition: Word 1",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100252",
                    "title": "CDISC ADAS-Cog - Word Recognition: Word 2",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100253",
                    "title": "CDISC ADAS-Cog - Word Recognition: Word 3",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100254",
                    "title": "CDISC ADAS-Cog - Word Recognition: Word 4",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100255",
                    "title": "CDISC ADAS-Cog - Word Recognition: Word 5",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100256",
                    "title": "CDISC ADAS-Cog - Word Recognition: Word 6",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100257",
                    "title": "CDISC ADAS-Cog - Word Recognition: Word 7",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100258",
                    "title": "CDISC ADAS-Cog - Word Recognition: Word 8",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100259",
                    "title": "CDISC ADAS-Cog - Word Recognition: Word 9",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100260",
                    "title": "CDISC ADAS-Cog - Word Recognition: Word 10",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100261",
                    "title": "CDISC ADAS-Cog - Word Recognition: Word 11",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100262",
                    "title": "CDISC ADAS-Cog - Word Recognition: Word 12",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100263",
                    "title": "CDISC ADAS-Cog - Word Recognition: Word 13",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100264",
                    "title": "CDISC ADAS-Cog - Word Recognition: Word 14",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100265",
                    "title": "CDISC ADAS-Cog - Word Recognition: Word 15",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100266",
                    "title": "CDISC ADAS-Cog - Word Recognition: Word 16",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100267",
                    "title": "CDISC ADAS-Cog - Word Recognition: Word 17",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100268",
                    "title": "CDISC ADAS-Cog - Word Recognition: Word 18",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100269",
                    "title": "CDISC ADAS-Cog - Word Recognition: Word 19",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100270",
                    "title": "CDISC ADAS-Cog - Word Recognition: Word 20",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100271",
                    "title": "CDISC ADAS-Cog - Word Recognition: Word 21",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100272",
                    "title": "CDISC ADAS-Cog - Word Recognition: Word 22",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100273",
                    "title": "CDISC ADAS-Cog - Word Recognition: Word 23",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100274",
                    "title": "CDISC ADAS-Cog - Word Recognition: Word 24",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100275",
                    "title": "CDISC ADAS-Cog - Remembering Test Instructions",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100276",
                    "title": "CDISC ADAS-Cog - Spoken Language Ability",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100277",
                    "title": "CDISC ADAS-Cog - Word Difficulty in Spontaneous Speech",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100278",
                    "title": "CDISC ADAS-Cog - Comprehension",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100279",
                    "title": "CDISC ADAS-Cog - Concentration/Distractibility",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100280",
                    "title": "CDISC ADAS-Cog - Number Cancellation Summary Score",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100281",
                    "title": "CDISC ADAS-Cog - Number Cancellation: Correct",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100282",
                    "title": "CDISC ADAS-Cog - Number Cancellation: Errors",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100283",
                    "title": "CDISC ADAS-Cog - Number Cancellation: Remind",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100284",
                    "title": "CDISC ADAS-Cog - Executive Function Maze Summary Score",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100285",
                    "title": "CDISC ADAS-Cog - Executive Function Maze: Errors",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100286",
                    "title": "CDISC ADAS-Cog - Executive Function Maze: Time",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C208544",
                    "title": "CDISC ADAS-Cog - Total Score",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C101869",
                    "title": "AIMS Clinical Classification Question",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C102034",
                    "title": "AIMS - Muscles of Facial Expression",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C102035",
                    "title": "AIMS - Lips and Perioral Area",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C102036",
                    "title": "AIMS - Jaw",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C102037",
                    "title": "AIMS - Tongue",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C102038",
                    "title": "AIMS - Upper Extremities",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C102039",
                    "title": "AIMS - Lower Extremities",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C102040",
                    "title": "AIMS - Neck, Shoulders, Hips",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C102041",
                    "title": "AIMS - Severity of Abnormal Movements",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C102042",
                    "title": "AIMS - Incapacitation Due to Abnormal Movements",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C102043",
                    "title": "AIMS - Patient's Awareness of Abnormal Movements",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C102044",
                    "title": "AIMS - Current Teeth/Dentures Problems",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C102045",
                    "title": "AIMS - Patient Usually Wears Dentures",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C102111",
                    "title": "Abnormal Involuntary Movement Scale Clinical Classification",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C120994",
                    "title": "APACHE II Clinical Classification Question",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C121005",
                    "title": "Acute Physiology and Chronic Health Evaluation II Clinical Classification",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C121096",
                    "title": "APACHE II - Temperature, Rectal",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C121097",
                    "title": "APACHE II - Mean Arterial Pressure",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C121098",
                    "title": "APACHE II - Heart Rate",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C121099",
                    "title": "APACHE II - Respiratory Rate",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C121100",
                    "title": "APACHE II - Oxygenation, A-aDO2",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C121101",
                    "title": "APACHE II - Oxygenation, PaO2",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C121102",
                    "title": "APACHE II - Arterial pH",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C121103",
                    "title": "APACHE II - Serum HCO3",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C121104",
                    "title": "APACHE II - Serum Sodium",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C121105",
                    "title": "APACHE II - Serum Potassium",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C121106",
                    "title": "APACHE II - Serum Creatinine",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C121107",
                    "title": "APACHE II - Hematocrit",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C121108",
                    "title": "APACHE II - White Blood Count",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C121109",
                    "title": "APACHE II - 15 Minus Glasgow Coma Score",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C121110",
                    "title": "APACHE II - A, Total Acute Physiology Score",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C121111",
                    "title": "APACHE II - B, Age Points",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C121112",
                    "title": "APACHE II - C, Chronic Health Points",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C121113",
                    "title": "APACHE II - Total APACHE II Score",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C147551",
                    "title": "ATLAS Clinical Classification Question",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C147589",
                    "title": "ATLAS Score Clinical Classification",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C147843",
                    "title": "ATLAS - Age",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C147844",
                    "title": "ATLAS - Treatment With Antibiotics",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C147845",
                    "title": "ATLAS - Leukocyte Count",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C147846",
                    "title": "ATLAS - Albumin",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C147847",
                    "title": "ATLAS - Serum Creatinine",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C147848",
                    "title": "ATLAS - Score",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C37939",
                    "title": "Date and Time",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C82525",
                    "title": "Test Occurrence",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C83217",
                    "title": "Birth Date and Time",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C112221",
                    "title": "Allergen Skin Response Index Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C112222",
                    "title": "Allergen Skin Response Intensity Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C112281",
                    "title": "Antigenic Skin Flare Longest Diameter Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C112282",
                    "title": "Antigenic Skin Flare Mean Diameter Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C112283",
                    "title": "Antigenic Skin Flare Size Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C112429",
                    "title": "Wheal Size Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C15189",
                    "title": "Biopsy Procedure",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C15260",
                    "title": "Immunodiagnostic Procedure",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C156629",
                    "title": "Anticipated Adverse Event (retired)",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C16502",
                    "title": "Diagnostic Imaging Testing",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C177692",
                    "title": "Expression Positive",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C19666",
                    "title": "Age at Menarche",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C25218",
                    "title": "Clinical Intervention or Procedure",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C25298",
                    "title": "Systolic Blood Pressure",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C25305",
                    "title": "Medical Examination Assessment",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C36291",
                    "title": "Finding by Cause",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C50995",
                    "title": "Disease Response",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C70945",
                    "title": "Biospecimen Collection",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C94411",
                    "title": "Genomic Profile",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C101875",
                    "title": "EQ-5D-5L Questionnaire Question",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C102067",
                    "title": "EQ-5D-5L - Mobility",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C102068",
                    "title": "EQ-5D-5L - Self-Care",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C102069",
                    "title": "EQ-5D-5L - Usual Activities",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C102070",
                    "title": "EQ-5D-5L - Pain or Discomfort",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C102071",
                    "title": "EQ-5D-5L - Anxiety or Depression",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C102072",
                    "title": "EQ-5D-5L - EQ VAS Score",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C102117",
                    "title": "European Quality of Life Five Dimension Five Level Scale Questionnaire",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C17208",
                    "title": "Transcription",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C181330",
                    "title": "Copy Number Variation Assessment",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C181331",
                    "title": "Single Nucleotide Variation Assessment",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C181332",
                    "title": "Microsatellite Instability Length Assessment",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C181333",
                    "title": "Gene Signature Assessment",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C181334",
                    "title": "Short Variation Assessment",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C181335",
                    "title": "Tumor Mutation Burden Assessment",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C189439",
                    "title": "Sequence Rearrangement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C189440",
                    "title": "Variable Number Tandem Repeats Assessment",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C189441",
                    "title": "Variant Profile Assessment",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C101876",
                    "title": "HAMA Questionnaire Question",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C102073",
                    "title": "HAMA - Anxious Mood",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C102074",
                    "title": "HAMA - Tension",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C102075",
                    "title": "HAMA - Fears",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C102076",
                    "title": "HAMA - Insomnia",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C102077",
                    "title": "HAMA - Intellectual",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C102078",
                    "title": "HAMA - Depressed Mood",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C102079",
                    "title": "HAMA - Somatic (Muscular)",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C102080",
                    "title": "HAMA - Somatic (Sensory)",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C102081",
                    "title": "HAMA - Cardiovascular Symptoms",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C102082",
                    "title": "HAMA - Respiratory Symptoms",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C102083",
                    "title": "HAMA - Gastrointestinal Symptoms",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C102084",
                    "title": "HAMA - Genitourinary Symptoms",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C102085",
                    "title": "HAMA - Autonomic Symptoms",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C102086",
                    "title": "HAMA - Behavior at Interview",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C102118",
                    "title": "Hamilton Anxiety Rating Scale Clinical Classification",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C155646",
                    "title": "HAMA - Total Score",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C83063",
                    "title": "Inclusion Exclusion Criteria Yes No Indicator",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C112460",
                    "title": "KFSS Questionnaire Question",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C112522",
                    "title": "Kurtzke Functional Systems Scores Clinical Classification",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C112609",
                    "title": "KFSS - Pyramidal Functions",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C112610",
                    "title": "KFSS - Cerebellar Functions",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C112611",
                    "title": "KFSS - Weakness Interferes With Testing",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C112612",
                    "title": "KFSS - Brain Stem Functions",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C112613",
                    "title": "KFSS - Sensory Functions",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C112614",
                    "title": "KFSS - Bowel and Bladder Functions",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C112615",
                    "title": "KFSS - Visual (or Optic) Functions",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C112616",
                    "title": "KFSS - Presence of Temporal Pallor",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C112617",
                    "title": "KFSS - Cerebral (or Mental) Functions",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C113884",
                    "title": "KFSS - Other Functions",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C113885",
                    "title": "KFSS - Other Functions Specify",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100116",
                    "title": "KPS Scale Questionnaire Question",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100417",
                    "title": "KPS Scale - Karnofsky Performance Status",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C100768",
                    "title": "Karnofsky Performance Status Scale Clinical Classification",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C105585",
                    "title": "Glucose Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C105586",
                    "title": "Cholesterol Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C105587",
                    "title": "High Density Lipoprotein Cholesterol Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C105588",
                    "title": "Low Density Lipoprotein Cholesterol Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C105589",
                    "title": "Very Low Density Lipoprotein Cholesterol Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C111207",
                    "title": "Hemoglobin A1C to Hemoglobin Ratio Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C119293",
                    "title": "Partial Pressure Arterial Oxygen to Fraction Inspired Oxygen Ratio Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C122157",
                    "title": "T-Lymphocyte Count",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C125949",
                    "title": "Urea Nitrogen Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C139084",
                    "title": "Carbon Monoxide Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C147355",
                    "title": "Carboxyhemoglobin to Total Hemoglobin Ratio Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C147390",
                    "title": "Macroscopic Blood Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C147403",
                    "title": "Nicotine Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C147406",
                    "title": "Nornicotine Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C170598",
                    "title": "Free Thyroxine Index",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C174314",
                    "title": "B-Lymphocyte Count",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C199683",
                    "title": "Polychromatic Erythrocyte Count",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C200008",
                    "title": "Polychromatic Erythrocytes to Erythrocytes Ratio Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C200249",
                    "title": "Soluble Interleukin-6 Receptor Subunit Alpha Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C201227",
                    "title": "Microcyte to Erythrocyte Ratio Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C45997",
                    "title": "pH",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C51946",
                    "title": "Erythrocyte Count",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C51948",
                    "title": "Leukocyte Count",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C51949",
                    "title": "Lymphocyte Count",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C51950",
                    "title": "Neutrophil Count",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C51951",
                    "title": "Platelet Count",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C63321",
                    "title": "Absolute Neutrophil Count",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C64470",
                    "title": "Absolute Basophil Count",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C64488",
                    "title": "Calcium Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C64495",
                    "title": "Chloride Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C64545",
                    "title": "Carbon Dioxide Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C64546",
                    "title": "Color Assessment",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C64547",
                    "title": "Creatinine Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C64548",
                    "title": "C-Reactive Protein Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C64550",
                    "title": "Eosinophil Count",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C64796",
                    "title": "Hematocrit Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C64797",
                    "title": "Erythrocyte Mean Corpuscular Hemoglobin",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C64798",
                    "title": "Erythrocyte Mean Corpuscular Hemoglobin Concentration",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C64799",
                    "title": "Erythrocyte Mean Corpuscular Volume",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C64803",
                    "title": "Polychromasia",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C64809",
                    "title": "Sodium Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C64810",
                    "title": "Nitrite Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C64812",
                    "title": "Triglyceride Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C64813",
                    "title": "Thyrotropin Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C64814",
                    "title": "Urate Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C64816",
                    "title": "Urobilinogen Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C64817",
                    "title": "Vitamin B12 Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C64821",
                    "title": "Macrocyte Count",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C64822",
                    "title": "Microcyte Count",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C64823",
                    "title": "Monocyte Count",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C64827",
                    "title": "Neutrophil to Leukocyte Ratio Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C64830",
                    "title": "Neutrophil Band Form Count",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C64831",
                    "title": "Neutrophil Band Form to Leukocyte Ratio",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C64832",
                    "title": "Specific Gravity",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C64848",
                    "title": "Hemoglobin Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C64849",
                    "title": "Hemoglobin A1C Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C64851",
                    "title": "Choriogonadotropin Beta Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C64853",
                    "title": "Potassium Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C64854",
                    "title": "Ketone Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C64855",
                    "title": "Lactate Dehydrogenase Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C64857",
                    "title": "Phosphate Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C64858",
                    "title": "Total Protein Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C73495",
                    "title": "Serum HCG Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C74667",
                    "title": "Bicarbonate Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C74676",
                    "title": "Folic Acid Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C74686",
                    "title": "Occult Blood Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C74737",
                    "title": "Ferritin Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C74747",
                    "title": "Triiodothyronine Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C74748",
                    "title": "Triiodothyronine Uptake Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C74760",
                    "title": "Urine Protein Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C74761",
                    "title": "Albumin To Creatinine Protein Ratio Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C74786",
                    "title": "Free Thyroxine Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C74797",
                    "title": "Anisocyte Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C74834",
                    "title": "Interleukin 6 Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C79463",
                    "title": "Protein to Creatinine Ratio Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C79602",
                    "title": "Poikilocyte Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C81997",
                    "title": "Segmented Neutrophil Count",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C82045",
                    "title": "Segmented Neutrophil to Leukocyte Ratio Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C82621",
                    "title": "D-Dimer Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C92249",
                    "title": "Cotinine Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C92290",
                    "title": "Cystatin C Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C96591",
                    "title": "Carboxyhemoglobin Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C98762",
                    "title": "Natural Killer Cell Count",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C38037",
                    "title": "Total Bilirubin Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C62656",
                    "title": "Prothrombin Time",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C64431",
                    "title": "Albumin Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C64432",
                    "title": "Alkaline Phosphatase Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C64433",
                    "title": "Alanine Aminotransferase Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C64467",
                    "title": "Aspartate Aminotransferase Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C64847",
                    "title": "Gamma Glutamyl Transpeptidase Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C98774",
                    "title": "Prothrombin Activity Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C112025",
                    "title": "Mass Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C124598",
                    "title": "Skeletal Examination",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C127774",
                    "title": "Swollen Indicator",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C128986",
                    "title": "Sharp Genant Bone Erosion Score",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C128987",
                    "title": "Sharp Genant Joint Space Narrowing Score",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C128988",
                    "title": "Sharp van der Heijde Bone Erosion Score",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C128989",
                    "title": "Sharp van der Heijde Joint Space Narrowing Score",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C138967",
                    "title": "Isometric Muscle Strength",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C139210",
                    "title": "Grip Strength",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C139211",
                    "title": "Pinch Strength",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C139212",
                    "title": "Range of Motion, Abduction",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C139213",
                    "title": "Range of Motion, Extension",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C139214",
                    "title": "Range of Motion, Dorsiflexion",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C139215",
                    "title": "Isometric Muscle Strength, Extension",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C139216",
                    "title": "Isometric Muscle Strength, Flexion",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C139217",
                    "title": "Bone Mineral Density Z-Score",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C139228",
                    "title": "Medical Research Council Manual Muscle Test Score, Extension",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C139229",
                    "title": "Medical Research Council Manual Muscle Test Score, Plantar Flexion",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C139230",
                    "title": "Medical Research Council Manual Muscle Test Score, Flexion",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C139231",
                    "title": "Medical Research Council Manual Muscle Test Score, Abduction",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C139232",
                    "title": "Medical Research Council Manual Muscle Test Score, Lateral Rotation",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C139233",
                    "title": "Medical Research Council Manual Muscle Test Score, Dorsiflexion",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C139234",
                    "title": "Medical Research Council Manual Muscle Test Score, Inversion",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C139235",
                    "title": "Medical Research Council Manual Muscle Test Score, Eversion",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C147472",
                    "title": "Bone Mineral Content",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C147473",
                    "title": "Bone Mineral Density T-Score",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C154909",
                    "title": "Fontanelle Closure Indicator",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C158256",
                    "title": "Fat Mass",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C158257",
                    "title": "Lean Mass",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C167264",
                    "title": "Musculoskeletal Examination",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C178017",
                    "title": "Skeletal Muscle Mass Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C178018",
                    "title": "Appendicular Skeletal Muscle Mass Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C181496",
                    "title": "Isometric Muscle Strength, Abduction",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C181497",
                    "title": "Isometric Muscle Strength, Dorsiflexion",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C181498",
                    "title": "Isometric Muscle Strength, Internal Rotation",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C181499",
                    "title": "Isometric Muscle Strength, External Rotation",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C181500",
                    "title": "Isometric Muscle Strength, Adduction",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C181501",
                    "title": "Muscle Endurance Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C181502",
                    "title": "Greulich and Pyle Bone Age Estimation",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C191306",
                    "title": "Alpha Angle of the Hip",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C191307",
                    "title": "Beta Angle of the Hip",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C25447",
                    "title": "Characteristic",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C61545",
                    "title": "Bone Mineral Density Test",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C63507",
                    "title": "Range of Motion",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C81307",
                    "title": "Estimation Method",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C82438",
                    "title": "Event Occurrence Indicator",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C83347",
                    "title": "Adverse Event Yes No Indicator",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C85522",
                    "title": "Medical History Yes No Indicator",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C101302",
                    "title": "Therapeutic Area",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C112038",
                    "title": "Trial Indication",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C117960",
                    "title": "Diagnostic Criteria",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C117961",
                    "title": "Relapse Criteria",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C117962",
                    "title": "Severity Criteria",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C119560",
                    "title": "ECG Evaluator Blinding Parameters",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C119561",
                    "title": "ECG Continuous Monitoring Indicator",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C119562",
                    "title": "ECG Planned Primary Lead for Study",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C119563",
                    "title": "ECG Used Same Lead Indicator",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C119564",
                    "title": "ECG Read Method Degree of Automation",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C119565",
                    "title": "ECG Replicates at Baseline Indicator",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C119566",
                    "title": "ECG Replicates On-Treatment Indicator",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C119582",
                    "title": "ECG T Wave Algorithm",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C123629",
                    "title": "FDA-Regulated Device Study Indicator",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C123630",
                    "title": "FDA-Regulated Drug Study Indicator",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C123631",
                    "title": "Pediatric Postmarket Study Indicator",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C123632",
                    "title": "Pediatric Study Indicator",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C124455",
                    "title": "Country of Manufacture",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C126058",
                    "title": "Biospecimen Retained and/or Contains DNA Indicator",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C126059",
                    "title": "EMA Decision Number for Pediatric Investigation Plan",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C126060",
                    "title": "EudraCT Resubmission Indicator",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C126061",
                    "title": "EudraVigilance Sender Identifier",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C126062",
                    "title": "Protocol Keyword",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C126063",
                    "title": "Number of Groups or Cohorts",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C126064",
                    "title": "Observational Model",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C126065",
                    "title": "Observational Time Perspective of Study",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C126066",
                    "title": "Observational Study Population Description",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C126067",
                    "title": "Observational Study Sampling Method",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C126068",
                    "title": "Observational Study Sampling Method Description",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C126069",
                    "title": "Pediatric Investigation Plan Indicator",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C126070",
                    "title": "Rare Disease Indicator",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C126071",
                    "title": "Resubmission Letter",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C126072",
                    "title": "Retained Biospecimen Description",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C126073",
                    "title": "SUSAR Reporting to EudraVigiliance Clinical Trial Module Indicator",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C126074",
                    "title": "SUSAR Reporting to National Competent Authority Indicator",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C126075",
                    "title": "Substudy Details",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C126076",
                    "title": "Substudy Planned Indicator",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C126077",
                    "title": "Planned Follow-Up Duration",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C126090",
                    "title": "EudraVigilance Sender Organization",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C127777",
                    "title": "Retained Biospecimen Contains DNA Indicator",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C127788",
                    "title": "Clinical Study Citation",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C127789",
                    "title": "Sponsor Commercial Status",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C127790",
                    "title": "Data Monitoring Committee Indicator",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C127791",
                    "title": "E-mail Address for XML File Feedback",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C127792",
                    "title": "Clinicaltrials.gov NCT Number for the Expanded Access Record",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C127793",
                    "title": "Trial Expanded Access Status",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C127794",
                    "title": "Multiple Site European Union State Trial Indicator",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C127795",
                    "title": "Number of Trial Sites within European Union State",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C127796",
                    "title": "Planned Trial Duration",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C127797",
                    "title": "PubMed Unique Identifier",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C127798",
                    "title": "Study Saved as XML Indicator",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C127799",
                    "title": "Requires Secure Email Delivery of XML Indicator",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C127800",
                    "title": "Single Site European Union State Trial Indicator",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C127801",
                    "title": "Study Protocol Uniform Resource Locator",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C127802",
                    "title": "Study Protocol Uniform Resource Locator Description",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C135009",
                    "title": "Sponsor Study Reference Identifier",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C135514",
                    "title": "Delayed Graft Function Diagnostic Criteria Name",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C139273",
                    "title": "Clinical Study Report Archive Date",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C139274",
                    "title": "Extension Trial Indicator",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C139275",
                    "title": "Post Authorization Safety Study Indicator",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C139276",
                    "title": "Planned Treatment Duration",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C139277",
                    "title": "Protocol Risk Assessment",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C142175",
                    "title": "Study Type",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C142438",
                    "title": "Clinical Study Functional Role",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C142450",
                    "title": "Clinical Trial Objective",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C146995",
                    "title": "Adaptive Study Design Indicator",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C15206",
                    "title": "Clinical Study",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C15320",
                    "title": "Study Design",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C15367",
                    "title": "Health Risk Assessment",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C156472",
                    "title": "Name and Version",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C156601",
                    "title": "Additional Outcome Measure",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C156602",
                    "title": "CDISC Therapeutic Area User Guide Name and Version",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C156603",
                    "title": "FDA Technical Specification Name and Version",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C156604",
                    "title": "Study Data Tabulation Model Implementation Guide Version",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C156605",
                    "title": "Study Data Tabulation Model Version",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C15697",
                    "title": "Treatment Regimen",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C15787",
                    "title": "Clinical Trials Design",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C16153",
                    "title": "Stratification Factors",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C16275",
                    "title": "Algorithm",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C163559",
                    "title": "Trial Exploratory Objective",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C164620",
                    "title": "Biospecimen Retention Indicator",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C16632",
                    "title": "Geographic Area",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C1708",
                    "title": "Agent",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C171103",
                    "title": "Study Status",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C171505",
                    "title": "Epidemic or Pandemic Related Disruption Indicator",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C171506",
                    "title": "Name of Epidemic or Pandemic",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C172240",
                    "title": "Clinicaltrials.gov Identifier",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C176230",
                    "title": "Contact Name",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C176372",
                    "title": "Study Contact Role",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C176373",
                    "title": "Study Contact Name",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C176374",
                    "title": "Study Contact Telephone Number",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C176375",
                    "title": "Study Contact E-mail Address",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C176376",
                    "title": "Study Contact Postal Address",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C189317",
                    "title": "SDTM Implementation Guide Medical Device Version",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C19238",
                    "title": "Diagnostic, Therapeutic, or Research Equipment",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C199141",
                    "title": "Health Issue Related Group",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C20189",
                    "title": "Property or Attribute",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C204581",
                    "title": "US FDA Tobacco Product Applicant",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C204699",
                    "title": "Ongoing Study Indicator",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C204700",
                    "title": "CDISC Tobacco Implementation Guide Version",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C214750",
                    "title": "Challenge Agent Name",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C21514",
                    "title": "Temporal Qualifier",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C25164",
                    "title": "Date",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C25169",
                    "title": "Route",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C25180",
                    "title": "Indicator",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C25196",
                    "title": "Randomization",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C25257",
                    "title": "Phase",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C25284",
                    "title": "Type",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C25330",
                    "title": "Duration",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C25337",
                    "title": "Number",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C25364",
                    "title": "Identifier",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C25365",
                    "title": "Description",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C25466",
                    "title": "Criterion",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C25488",
                    "title": "Dose",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C25688",
                    "title": "Status",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C25714",
                    "title": "Version",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C38114",
                    "title": "Route of Administration",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C40978",
                    "title": "Telephone Number",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C41161",
                    "title": "Protocol Agent",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C41184",
                    "title": "Indication",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C42614",
                    "title": "Name",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C42636",
                    "title": "Pharmaceutical Dosage Form",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C42743",
                    "title": "Uniform Resource Locator",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C42774",
                    "title": "Title",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C42775",
                    "title": "E-mail Address",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C43513",
                    "title": "Keyword",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C48281",
                    "title": "Trial Phase",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C48355",
                    "title": "Sponsor",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C48470",
                    "title": "Potency Unit",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C49236",
                    "title": "Therapeutic Procedure",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C49647",
                    "title": "Control Type",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C49650",
                    "title": "Diagnosis Group",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C49652",
                    "title": "Clinical Study by Intent",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C49658",
                    "title": "Trial Blinding Schema",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C49660",
                    "title": "Trial Type",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C49692",
                    "title": "Planned Subject Number",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C49693",
                    "title": "Planned Minimum Age of Subjects",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C49694",
                    "title": "Planned Maximum Age of Subjects",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C49695",
                    "title": "Study Subject Group Characteristics",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C49696",
                    "title": "Sex of Study Group",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C49697",
                    "title": "Trial Length",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C49698",
                    "title": "Study Stop Rule",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C49703",
                    "title": "Test Product Added to Existing Treatment",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C49802",
                    "title": "Trial Title",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C50282",
                    "title": "Lead Device",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C54346",
                    "title": "Dose Modification",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C61186",
                    "title": "Applicant",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C62085",
                    "title": "ECG Measurement",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C68609",
                    "title": "Active Comparator",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C68612",
                    "title": "Active Comparator Drug",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C68616",
                    "title": "Start Date",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C68617",
                    "title": "End Date",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C68805",
                    "title": "Character",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C69208",
                    "title": "Study Start Date",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C70663",
                    "title": "Unique Identifier",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C70705",
                    "title": "Component of Study Protocol",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C70772",
                    "title": "Knowledge Field",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C70793",
                    "title": "Clinical Study Sponsor",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C70834",
                    "title": "Study Population Description",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C70946",
                    "title": "Postal Address",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C71137",
                    "title": "Dose Regimen",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C71465",
                    "title": "Intervention Duration",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C71492",
                    "title": "Sampling Method",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C71610",
                    "title": "Quotient",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C73558",
                    "title": "Dosage Form Unit",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C85582",
                    "title": "Current Therapy",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C85826",
                    "title": "Trial Primary Objective",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C85827",
                    "title": "Trial Secondary Objective",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C89081",
                    "title": "Dose Frequency",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C90372",
                    "title": "Class of Trial Agent",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C90462",
                    "title": "Clinical Study End Date",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C93518",
                    "title": "Blinded Description",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C93531",
                    "title": "Citation Description",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C93625",
                    "title": "Planned Duration",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C93638",
                    "title": "Publication Identifier",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C93874",
                    "title": "Organization Name",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C98703",
                    "title": "Actual Subject Number",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C98714",
                    "title": "Clinical Trial Registry Identifier",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C98715",
                    "title": "Confirmed Response Minimum Duration",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C98717",
                    "title": "Data Cutoff Date",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C98718",
                    "title": "Data Cutoff Date Description",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C98724",
                    "title": "Exploratory Outcome Measure",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C98737",
                    "title": "Healthy Subject Indicator",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C98746",
                    "title": "Intervention Model",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C98747",
                    "title": "Intervention Type",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C98768",
                    "title": "Pharmacological Class of Investigational Therapy",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C98770",
                    "title": "Planned Country of Investigational Site",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C98771",
                    "title": "Planned Number of Arms",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C98772",
                    "title": "Primary Outcome Measure",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C98775",
                    "title": "Randomization Quotient",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C98781",
                    "title": "Secondary Outcome Measure",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C98783",
                    "title": "Stable Disease Minimum Duration",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C179175",
                    "title": "Solicited Adverse Event",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C181760",
                    "title": "History of Tobacco Use",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C200145",
                    "title": "Solicited Medical History",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C201990",
                    "title": "Caffeine Use History",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C53630",
                    "title": "Concomitant Therapy",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C81229",
                    "title": "Alcohol Use History",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C82571",
                    "title": "Reported Event Term (delete)",
                    "type": "Biomedical Concept"
                }, {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts/C83118",
                    "title": "Medical History Reported Term (delete)",
                    "type": "Biomedical Concept"
                }],
                "self": {
                    "href": "/mdr/bc/packages/2025-07-01/biomedicalconcepts",
                    "title": "Biomedical Concepts",
                    "type": "Biomedical Concept List"
                }
            },
            "name": "Biomedical Concepts 2025-07-01",
            "label": "Biomedical Concept Package Effective 2025-07-01",
            "effectiveDate": "2025-07-01",
            "version": "2025-07-01"
        }"""
        
        j = json.loads(jsonstr)
        print(BiomedicalConceptPackage(j))