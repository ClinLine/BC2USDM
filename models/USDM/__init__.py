__name__="BC2USDM.models.USDM"

class AttributeNames:
    repository = "bcRepository"

    class Repository:
        business_therapeutic_areas = "businessTherapeuticAreas"
        categories = "bcCategories"
        biomedical_concepts = "biomedicalConcepts"

    class BusinessTherapeuticAreas:
        id = "id"
        code = "code"
        code_system = "codeSystem"
        code_system_version = "codeSystemVersion"
        decode = "decode"
        instance_type = "instanceType"

    class BiomedicalConceptCategories:
        id = "id"
        label = name = "name"
        description = "description"
        code = "code"
        child_ids = "childIds"
        member_ids = "memberIds"
        instance_type = "instanceType"
        notes = "notes"

    class BiomedicalConcept:
        id = "id"
        name = "name"
        label = "label"
        synonyms = "synonyms"
        reference = "reference"
        properties = "properties"
        code = "code"
        notes = "notes"
        instance_type = "instanceType"

        class AliasCode:
            id = "id"
            standard_code = "standardCode"

            aliases = standardCodeAliases = "standardCodeAliases"
            instanceType = "instanceType"

            class StandardCode:
                id = "id"
                code = "code"
                code_system = "codeSystem"
                code_system_version = "codeSsytemVersion"
                decode = "decode"
                instance_type = "instanceType"

        class Propety:
            id = "id"
            name = "name"
            label = "label"
            is_required = "isRequired"
            is_enabled = "isEnabled"
            data_type = "datatype"
            response_codes = "responseCodes"
            code = "code"
            notes = "notes"
            instance_type = "instanceType"

            class AliasCode:
                id = "id"
                standard_code = "standardCode"

                aliases = standardCodeAliases = "standardCodeAliases"
                instanceType = "instanceType"

                class StandardCode:
                    id = "id"
                    code = "code"
                    code_system = "codeSystem"
                    code_system_version = "codeSsytemVersion"
                    decode = "decode"
                    instance_type = "instanceType"

