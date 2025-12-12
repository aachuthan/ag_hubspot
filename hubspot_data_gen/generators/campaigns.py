import random
from typing import Dict, Any
from datetime import datetime, timedelta
from .base import BaseGenerator

class CampaignGenerator(BaseGenerator):
    def generate_one(self) -> Dict[str, Any]:
        start_date = datetime.now() + timedelta(days=random.randint(1, 30))
        end_date = start_date + timedelta(days=random.randint(30, 90))
        
        return {
            "name": f"{self.fake.bs().title()} Campaign {random.randint(1000, 9999)}",
            "appName": "HubSpot Data Gen",
            "utmCampaign": self.fake.slug(),
            "utmSource": random.choice(["facebook", "google", "linkedin", "email"]),
            "utmMedium": random.choice(["cpc", "organic", "social", "email"]),
            "utmContent": "variation_" + random.choice(["a", "b", "c"]),
            "utmTerm": self.fake.word(),
            # "startTime": int(start_date.timestamp() * 1000), # Not always writable on create, depends on endpoints
            # "endTime": int(end_date.timestamp() * 1000)
        }

    def generate_budget_item(self) -> Dict[str, Any]:
        return {
            "name": f"Budget: {self.fake.bs()}",
            "amount": str(random.randint(1000, 50000)),
            "description": self.fake.sentence()
        }

    def generate_spend_item(self) -> Dict[str, Any]:
        return {
            "name": f"Spend: {self.fake.bs()}",
            "amount": str(random.randint(100, 5000)),
            "date": int(datetime.now().timestamp() * 1000),
            "description": self.fake.sentence()
        }
