import random
from typing import Dict, Any
from .base import BaseGenerator

class CompanyGenerator(BaseGenerator):
    def generate_one(self) -> Dict[str, Any]:
        return {
            "name": self.fake.company(),
            "domain": self.fake.domain_name(),
            "industry": self.fake.job(), # Using job as a proxy for industry string
            "about_us": self.fake.text(max_nb_chars=200),
            "phone": self.fake.phone_number(),
            "address": self.fake.street_address(),
            "address2": self.fake.secondary_address(),
            "city": self.fake.city(),
            "state": self.fake.state(),
            "zip": self.fake.zipcode(),
            "country": self.fake.country(),
            "website": self.fake.url(),
            "numberofemployees": random.randint(1, 10000),
            "annualrevenue": random.randint(10000, 100000000),
            "description": self.fake.bs(),
            "founded_year": str(random.randint(1900, 2024)),
            "timezone": self.fake.timezone(),
            # "lifecyclestage": random.choice(["subscriber", "lead", "marketingqualifiedlead", "salesqualifiedlead", "opportunity", "customer", "evangelist", "other"]),
        }
