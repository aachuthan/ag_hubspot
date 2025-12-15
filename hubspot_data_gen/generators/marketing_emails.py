import random
from typing import Dict, Any
from .base import BaseGenerator

class MarketingEmailGenerator(BaseGenerator):
    def generate_one(self) -> Dict[str, Any]:
        # Unique name to avoid collisions
        email_name = f"Campaign Email {random.randint(1000, 9999)}: {self.fake.catch_phrase()}"
        
        return {
            "name": email_name,
            "subject": f"Special Offer: {self.fake.bs().title()}",
            "templatePath": "@hubspot/email/dnd/welcome.html", # Safe system default
            "state": "DRAFT",
            "content": {
                "plainTextBody": self.fake.paragraph(),
                "htmlTitle": email_name,
            },
            # "activeDomain": "..." # Optional, omitting to avoid 400s if domain doesn't exist
        }
