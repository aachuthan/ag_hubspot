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
                "notifyRecipients": "marketing@example.com", # Added dummy email
                "language": "en",
                "postSubmitAction": {
                    "type": "thank_you_message",
                    "value": "Thanks for submitting the form!"
                },
                # Detailed GDPR Consent Options
                "legalConsentOptions": {
                    "type": "explicit_consent_to_process",
                    "consentToProcessText": "I agree to allow Example Co. to store and process my personal data.",
                    "communicationsCheckboxes": [
                        {
                            "label": "I agree to receive marketing communications.",
                            "required": False,
                            "subscriptionTypeId": 999 # Dummy Subscription Type ID
                        }
                    ]
                }
            },
            # Context Object for Submission (Simulated)
            "context": {
                "hutk": self.fake.uuid4(), # Simulated HubSpot Cookie
                "ipAddress": self.fake.ipv4(),
                "pageUri": self.fake.url(),
                "pageName": self.fake.bs().title()
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
                        },
                        {
                            "name": "lastname",
                            "label": "Last Name",
                            "fieldType": "text",
                             "required": False,
                             "enabled": True,
                             "hidden": False,
                        },
                        {
                            "name": "mobilephone",
                            "label": "Mobile Phone",
                            "fieldType": "phonenumber",
                             "required": False,
                             "enabled": True,
                             "hidden": False,
                        },
                        {
                            "name": "company",
                            "label": "Company",
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
             }
        }
