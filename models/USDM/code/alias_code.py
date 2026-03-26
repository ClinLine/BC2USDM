# @dataclass
from dataclasses import dataclass
from dataclasses import field
from uuid import uuid4 as guid
from utils.b_colors import BColors
from models.USDM.code import Code

# from models.USDM.code.code import Code



@dataclass
class AliasCode():
    # usdm_id (guid)
    # id_ should not be relevent for the model side, only for id based lookups
    id_:guid
    # ncit Code
    standard_code:Code
    # list of codes for all aliases
    decode:str
    standard_code_aliases: list[Code] = field(default_factory=list[Code])
    INSTANCE_TYPE = __qualname__

    '''
    List of terminologies:
    
    ncit - NCI Thesaurus
    ncim - NCI Metathesaurus
    canmed - CanMED
    chebi - Chemical Entities of Biological Interest
    ctcae5 - CTCAE 5
    duo - Data Use Ontology
    go - Gene Ontology
    hgnc - HUGO Gene Nomenclature Committee
    hl7v30 - Health Level 7 Vocabulary (V3)
    icd10 = International Classification of Diseases, Tenth Revision
    icd10cm - The International Classification of Diseases, Tenth Revision, Clinical Modification
    icd9cm - The International Classification of Diseases, Ninth Revision, Clinical Modification
    loinc - Logical Observation Identifier Names and Codes
    ma - Mouse Anatomy: Anatomical Dictionary for the Adult Mouse
    mdr = Medical Dictionary for Regulatory Activities
    medrt - MED-RT
    mged - Microarray Gene Expression Data Ontology
    ndfrt - National Drug File Reference Terminology
    npo - NanoParticle Ontology
    obi - Ontology for Biomedical Investigations
    obib - The ontology for Biobanking
    pdq - Physician Data Query
    radlex - Radiology Lexicon
    snomedct_us - SNOMED Clinical Terms
    umlssemnet - UMLS Semantic Network: UMLS Semantic Network
    zfa - Zebrafish Model Organism Database

    Sample Codes

Following are sample codes you can use with each terminology for testing.

    ncit - C3224 - Melanoma
    ncim - C0025202 - Melanoma
    canmed - HCPCS_HPV_VACCINE - HPV Vaccine
    chebi - CHEBI:119915 - Fentanyl
    ctcae5 - C143201 - Disease progression
    duo - DUO_0000004 - no restriction
    go - GO:0008152 - metabolic process
    hgnc - HGNC:3430 - ERBB2
    hl7v30 - F - Female
    icd10 - D03.9 - Melanoma in situ, unspecified
    icd10cm - D03.9 - Melanoma in situ, unspecified
    icd9cm - 172.9 - Melanoma of skin, site unspecified
    loinc - 21526-9 - Sodium:MCnc:24H:Urine:Qn
    ma - MA:0000353 - stomach
    mdr - 10053571 - Melanoma
    medrt - N0000177915 - Acetaminophen
    mged - MO_526 - microeinstein_per_minute_and_square_meter
    ndfrt - N0000175556 - beta-Adrenergic Blocker [EPC]
    npo - NPO_197 - gold nanocage
    obi - OBI_0001906 - cancer cell line
    obib - OBI_0002200 - cannot be assessed determination
    pdq - CDR0000492706 - cantuzumab ravtansine
    radlex - RID28531 - ground-glass opacity
    snomedct_us - 73211009 - Diabetes mellitus
    umlssemnet - T046 - Disorder
    zfa - ZFA:0001383 - fin bud

    '''

    # STATIC METHODS
    @staticmethod
    def assess_code_system(code_string:str):
        # all ncit (and ncim) codes follow C000... pattern:
        if code_string [0] == 'C' and code_string[1:-1].isdigit():
            return "ncit"
        else:
            # TODO determine code system based on code
            # Perhaps use NCI EVS Rest API https://evsexplore.semantics.cancer.gov/evsexplore/evsapi 
            print(f"[AliasCode.assess_code_system:] code recognition other than ncit is not yet supported")
            return "other"
    
    def __init__(self, standard_code, id_=None, aliases: list[Code] = None, check_code:bool=False):
        if(isinstance(id_, str)):
            print(f"[AliasCode.init]String id_ found: {id_}")
        if id_ is None or id_ == "":
            #TODO request guid from local storage, duplicates having (different) unique ids
            self.id_ = guid()
        else: self.id_ = id_
        
        if isinstance(standard_code, str) and check_code:
            print(f"{BColors.WARNING} AliasCode.init: Avoid creating AliasCode by string, provide a Code object instead. {BColors.ENDC}")
            code_system = AliasCode.assess_code_system(standard_code)
            self.standard_code = Code(code=standard_code, code_system=code_system)
        elif isinstance(standard_code, Code):
            self.standard_code = standard_code
        else:
            code_system = Code.CodeSystem.CUSTOM
            self.standard_code = Code(code=standard_code,code_system=code_system,code_system_version=Code.DEFAULT_CODE_SYSTEM_VERSION)
        self.standard_code_aliases = aliases

    def add_alias(self, alias:Code):
        '''Append provided alias to alias codes list'''
        if self.standard_code_aliases is None:
            self.standard_code_aliases = [alias]
        else:
            self.standard_code_aliases.append(alias)

    def __eq__(self, value):
        if self.id_ != value.id_:
            print(f"AliasCode.eq: id inequality is currently being disregarded, since it can't be changed by the user.")
        if self.decode != value.decode: return False
        if self.standard_code != value.standard_code: return False
    
    def __contains__(self, item):
        if not isinstance(item, Code):
            raise TypeError(f"{BColors.FAIL} AliasCode.contains can only be used to check for code aliases")
        
        if item in self.standard_code_aliases:
            return True
        return False
    # def __str__(self):
    #     result = "{"
    #     if self.id_ is not None:
    #         result += f"\n\r\t\"id:\":\"{self.id_}\","
    #     if self.standard_code is not None:
    #         result += f"\n\r\t\"standardCode:\":\"{self.standard_code}\","
    #     if self.standard_code_aliases is not None and len(self.standard_code_aliases) > 0:
    #         result += "\n\r\t\"standardCodeAliases:\":["
    #         for code in self.standard_code_aliases:
    #             result += f"{str(code)},"
    #         result = result[:-2] # Drop last ','
    #         result += "],"
    #     result = result[:-2] # drop last character, which should be a ','
    #     result +="\n\r}"
    #     return result
