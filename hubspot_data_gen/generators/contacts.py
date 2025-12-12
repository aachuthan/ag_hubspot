import random
from typing import Dict, Any
from .base import BaseGenerator

class ContactGenerator(BaseGenerator):
    def generate_one(self) -> Dict[str, Any]:
        return {
            "email": self.fake.email(),
            "firstname": self.fake.first_name(),
            "lastname": self.fake.last_name(),
            "phone": self.fake.phone_number(),
            "mobilephone": self.fake.phone_number(),
            "company": self.fake.company(),
            "website": self.fake.url(),
            "jobtitle": self.fake.job(),
            "address": self.fake.street_address(),
            "city": self.fake.city(),
            "state": self.fake.state(),
            "zip": self.fake.zipcode(),
            "country": self.fake.country(),
            "lifecyclestage": random.choice([
                "subscriber", "lead", "marketingqualifiedlead", 
                "salesqualifiedlead", "opportunity", "customer", 
                "evangelist", "other"
            ]),
            # "lead_status": random.choice(["NEW", "OPEN", "IN_PROGRESS", "OPEN_DEAL", "UNQUALIFIED", "ATTEMPTED_TO_CONTACT", "CONNECTED", "BAD_TIMING"]), # Standard but often customized
            "salutation": self.fake.prefix(),
            "gender": random.choice(["Male", "Female", "Other", "Prefer not to say"]), # Usually custom
        }
