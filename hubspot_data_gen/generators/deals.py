import random
from typing import Dict, Any
from datetime import datetime, timedelta
from .base import BaseGenerator

class DealGenerator(BaseGenerator):
    def generate_one(self) -> Dict[str, Any]:
        # Standard 'default' pipeline stages
        stages = [
            "appointmentscheduled", "qualifiedtobuy", "presentationscheduled", 
            "decisionmakerboughtin", "contractsent", "closedwon", "closedlost"
        ]
        
        future_date = datetime.now() + timedelta(days=random.randint(1, 90))
        
        return {
            "dealname": f"{self.fake.company()} Deal",
            "amount": str(random.randint(1000, 50000)),
            "dealstage": random.choice(stages),
            "pipeline": "default",
            "closedate": str(int(future_date.timestamp() * 1000)), # HubSpot expects milliseconds
            "dealtype": random.choice(["newbusiness", "existingbusiness"]),
            "description": self.fake.text(max_nb_chars=200)
        }
