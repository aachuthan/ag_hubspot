import random
from typing import Dict, Any
from datetime import datetime, timedelta
from .base import BaseGenerator

class MeetingGenerator(BaseGenerator):
    def generate_one(self) -> Dict[str, Any]:
        start_time = datetime.now() + timedelta(days=random.randint(1, 14))
        end_time = start_time + timedelta(minutes=random.choice([15, 30, 60]))
        
        start_ts = str(int(start_time.timestamp() * 1000))
        end_ts = str(int(end_time.timestamp() * 1000))
        
        return {
            # REQUIRED: Timestamp of the meeting
            "hs_timestamp": start_ts, 
            
            "hs_meeting_title": f"Meeting with {self.fake.company()}",
            "hs_meeting_body": self.fake.paragraph(),
            "hs_internal_meeting_notes": f"Internal Note: {self.fake.sentence()}",
            "hs_meeting_location": random.choice(["Zoom", "Google Meet", "Office", "Phone"]),
            "hs_meeting_start_time": start_ts,
            "hs_meeting_end_time": end_ts,
            "hs_meeting_outcome": random.choice(["SCHEDULED", "COMPLETED", "RESCHEDULED", "NO_SHOW"]),
            "hs_meeting_external_url": self.fake.url(),
            
            
            # Attachments (Empty for now, but field is standard)
            "hs_attachment_ids": "" 
        }
