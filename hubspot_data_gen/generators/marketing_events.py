import random
from typing import Dict, Any
from datetime import datetime, timedelta
from .base import BaseGenerator

class MarketingEventGenerator(BaseGenerator):
    def generate_one(self) -> Dict[str, Any]:
        start_date = datetime.now() + timedelta(days=random.randint(10, 60))
        end_date = start_date + timedelta(hours=2)
        
        return {
            "eventName": f"Webinar: {self.fake.catch_phrase()}",
            "eventOrganizer": self.fake.company(),
            "eventDescription": self.fake.paragraph(),
            "eventUrl": self.fake.url(),
            "startDateTime": start_date.isoformat() + "Z", # Marketing events use ISO8601
            "endDateTime": end_date.isoformat() + "Z",
            "eventCancelled": False,
            "customProperties": []
        }
