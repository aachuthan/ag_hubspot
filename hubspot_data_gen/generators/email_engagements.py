import random
from typing import Dict, Any
from datetime import datetime
from .base import BaseGenerator

class EmailEngagementGenerator(BaseGenerator):
    def generate_one(self) -> Dict[str, Any]:
        # Generating an 'Email' object for CRM (Logged Email)
        ts = str(int(datetime.now().timestamp() * 1000))
        
        email_text = self.fake.text()
        email_html = f"<html><body><p>{email_text}</p><p>Sent via HubSpot Data Gen</p></body></html>"
        
        return {
            # REQUIRED
            "hs_timestamp": ts,
            
            "hs_email_subject": self.fake.sentence(),
            "hs_email_text": email_text,
            "hs_email_html": email_html,
            "hs_email_direction": random.choice(["INCOMING_EMAIL", "EMAIL"]),
            "hs_email_status": random.choice(["SENT", "BOUNCED", "OPENED", "FAILED", "SCHEDULED"]),
            
            # Standard Headers (JSON String)
            "hs_email_headers": "{\"from\": \"sender@example.com\", \"to\": \"recipient@example.com\"}",
            
            "hs_attachment_ids": ""
        }
