import random
from typing import Dict, Any
from datetime import datetime
from .base import BaseGenerator

class CallGenerator(BaseGenerator):
    def generate_one(self) -> Dict[str, Any]:
        # Properties for Calls (CRM Object)
        start_ts = str(int(datetime.now().timestamp() * 1000))
        duration = random.randint(60000, 3600000) # 1 min to 60 mins in ms
        
        return {
            "hs_timestamp": start_ts, # REQUIRED: When the engagement happened
            
            "hs_call_title": f"Call with {self.fake.name()}",
            "hs_call_body": self.fake.paragraph(),
            "hs_call_duration": str(duration),
            "hs_call_status": random.choice(["COMPLETED", "BUSY", "NO_ANSWER", "MISSED", "CANCELED"]),
            "hs_call_from_number": self.fake.phone_number(),
            "hs_call_to_number": self.fake.phone_number(),
            "hs_call_recording_url": self.fake.url(),
            
            # "hubspot_owner_id": "...",
            # "hubspot_owner_id": "...", 
        }
