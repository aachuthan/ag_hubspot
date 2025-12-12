import random
from typing import Dict, Any
from .base import BaseGenerator

class FormGenerator(BaseGenerator):
    def generate_one(self) -> Dict[str, Any]:
        # Minimal Form v3 payload
        name = f"{self.fake.bs().title()} Form {random.randint(1000, 9999)}"
        return {
            "name": name,
            "formType": "hubspot",
            "configuration": {
                "createNewContactForNewEmail": "true",
                "notifyRecipients": "",
                "language": "en",
                "postSubmitAction": {
                    "type": "thank_you_message",
                    "value": "Thanks for submitting the form!"
                }
            },
            "fieldGroups": [
                {
                    "groupType": "default_group",
                    "richTextType": "text",
                    "fields": [
                        {
                            "name": "email",
                            "label": "Email",
                            "fieldType": "text",
                             "required": True,
                             "enabled": True,
                             "hidden": False,
                        },
                         {
                            "name": "firstname",
                            "label": "First Name",
                            "fieldType": "text",
                             "required": False,
                             "enabled": True,
                             "hidden": False,
                        }
                    ]
                }
            ],
             "displayOptions": {
                "theme": "canvas",
                "style": "legal-consent"
             },
             "legalConsentOptions": {
                 "type": "none"
             }
        }
