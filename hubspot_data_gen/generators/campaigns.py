import random
from typing import Dict, Any
from datetime import datetime, timedelta
from .base import BaseGenerator

class CampaignGenerator(BaseGenerator):
    def generate_one(self) -> Dict[str, Any]:
        start_date = datetime.now() + timedelta(days=random.randint(1, 30))
        end_date = start_date + timedelta(days=random.randint(30, 90))
        
        name_val = f"{self.fake.bs().title()} Campaign {random.randint(1000, 9999)}"
        # Standard HubSpot Campaign Properties
        # API usually expects these in the key-value map or under a 'properties' key depending on endpoint version.
        # We will provide a flat dictionary which the inserter can then format as needed (e.g. into 'properties': {...})
        return {
            "hs_name": name_val, # REQUIRED: The campaign name
            
            # Writable Standard Properties
            "hs_start_date": start_date.strftime("%Y-%m-%d"),
            "hs_end_date": end_date.strftime("%Y-%m-%d"),
            "hs_notes": self.fake.sentence(),
            "hs_audience": random.choice(["Existing Customers", "New Leads", "Churned Users", "High Value"]),
            "hs_currency_code": "USD",
            "hs_campaign_status": "active", # planned, in_progress, active, paused, completed
            "hs_color_hex": self.fake.hex_color(),
            
            # UTM Parameters (standardized keys)
            "hs_utm_campaign": self.fake.slug(),
            "hs_utm_source": random.choice(["facebook", "google", "linkedin", "email"]),
            "hs_utm_medium": random.choice(["cpc", "organic", "social", "email"]),
            "hs_utm_content": "variation_" + random.choice(["a", "b", "c"]),
            "hs_utm_term": self.fake.word(),
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
            "date": datetime.now().strftime("%Y-%m-%d"),
            "description": self.fake.sentence()
        }
