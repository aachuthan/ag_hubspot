import random
from typing import Dict, Any
from .base import BaseGenerator

class TicketGenerator(BaseGenerator):
    def generate_one(self) -> Dict[str, Any]:
        # Standard '0' pipeline stages (Support Pipeline)
        stages = ["1", "2", "3", "4"] # New, Waiting on contact, Waiting on us, Closed
        priorities = ["LOW", "MEDIUM", "HIGH"]
        
        return {
            "subject": f"Support: {self.fake.sentence(nb_words=5)}",
            "content": self.fake.paragraph(),
            "hs_pipeline": "0",
            "hs_pipeline_stage": random.choice(stages),
            "hs_ticket_priority": random.choice(priorities),
            "hs_ticket_source": random.choice(["EMAIL", "CHAT", "PHONE", "FORM"]),
        }
