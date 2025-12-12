import random
from typing import Dict, Any
from datetime import datetime
from .base import BaseGenerator

class EmailEngagementGenerator(BaseGenerator):
    def generate_one(self) -> Dict[str, Any]:
        # Generating an 'Email' object for CRM (Logged Email)
        return {
            "hs_email_subject": self.fake.sentence(),
            "hs_email_text": self.fake.text(),
            "hs_email_direction": random.choice(["INCOMING_EMAIL", "EMAIL"]),
            "hs_timestamp": str(int(datetime.now().timestamp() * 1000)),
            "hs_email_status": random.choice(["SENT", "BOUNCED", "OPENED"]),
        }
