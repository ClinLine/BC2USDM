class AttributeNames:
    class Link:
        reference = href = "href"
        label = title = "Title"
        type = "Type"

    class BiomedicalConceptPackage:
        links = "_links"
        reference = href = "href"
        title = "title"
        type = "type"
        packages = "packages"
        self = "self"

    class BiomedicalConceptCategories:
        links = "_links"
        self = "self"
        reference = href = "href"
        title = "title"
        type = "type"
        categories = "categories"
        shortname = name = "name"


    class BiomedicalConceptList:
        links = "_links"
        name = "name"
        category = "category"
        label = "label"

        class BiomedicalConceptListLinks:
            biomedical_concepts = "biomedicalConcepts"
            self = "self"

    class BiomedicalConcept:
        links = "_links"
        concept_id = "conceptId"
        reference = href = "href"

        categories = "categories"
        label = short_name = "shortName"
        synonyms = "synonyms"

        result_scales = "resultScales"
        definition = "definition"
        coding = "coding"
        data_element_concepts = "dataElementConcepts"
        ncit_code = "ncitCode"

        class BiomedicalConceptLinks:
            parent_biomedical_concept = "parentBiomedicalConcept"
            parent_package = "parentPackage"
            self = "self"
        
        class Coding:
            code = "code"
            system = "system"
            system_name = "systemName"

        class DataElementConcepts:
            concept_id = "conceptId"
            reference = href = "href"
            label = short_name  = "shortName"
            data_type = "dataType"
            example_set = "exampleSet"
            ncit_code = "ncitCode"

class ResultScales:
    Quantitative = "Quantitative"
    Ordinal = "Ordinal"
    Nominal = "Nominal"
    Narrative = "Narrative"
    Temporal = "Temporal"
