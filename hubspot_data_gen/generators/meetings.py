import random
from typing import Dict, Any
from datetime import datetime, timedelta
from .base import BaseGenerator

class MeetingGenerator(BaseGenerator):
    def generate_one(self) -> Dict[str, Any]:
        start_time = datetime.now() + timedelta(days=random.randint(1, 14))
        end_time = start_time + timedelta(minutes=random.choice([15, 30, 60]))
        
        return {
            "hs_meeting_title": f"Meeting with {self.fake.company()}",
            "hs_meeting_body": self.fake.paragraph(),
            "hs_meeting_location": "Zoom",
            "hs_meeting_start_time": str(int(start_time.timestamp() * 1000)),
            "hs_meeting_end_time": str(int(end_time.timestamp() * 1000)),
            "hs_meeting_outcome": random.choice(["SCHEDULED", "COMPLETED", "RESCHEDULED", "NO_SHOW"]),
            "hs_activity_type": "Meeting",
        }
