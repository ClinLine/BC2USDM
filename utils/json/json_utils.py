class json_utils:
    @staticmethod
    def export_study_as_json(os: object):
        '''
        Docstring for export_study_as_json
        
        :param os: Description
        :type os: object
        '''

        '''
        { 
            "study": {
                "id": guid,
                "name": label_guid,
                "description": null,
                "label", null,
                versions": [{
                        "id": "StudyVersion_$(versionIdentifier)",
                        "extensionAttributes": [],
                        "versionIdentifier": "1",
                        "rationale": "A simple test",
                        "documentVersionIds":[
                            "StudyDefinitionDocumentVersion_$(versionIdentifier)
                        ],
                        "dateValues": [{
                                "id": "$(guid)",
                                "extensionAttributes": [],
                                "name": "$(label)_$(id)",
                                "label": "Design Approval",
                                "description": "Design approval data",
                                "type": {
                                    "id": "Code_20",
                                    "extenstionAttributes":[],
                                    "code": "$(Code.APPROVAL_DATE.code)")"}}]
                }]
            }
        }
        '''