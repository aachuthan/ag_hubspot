import random
from typing import Dict, Any
from datetime import datetime, timedelta
from .base import BaseGenerator

class MarketingEventGenerator(BaseGenerator):
    def generate_one(self) -> Dict[str, Any]:
        start_date = datetime.now() + timedelta(days=random.randint(10, 60))
        end_date = start_date + timedelta(hours=2)
        
        # REQUIRED Properties
        external_account_id = f"acc-{random.randint(10000, 99999)}"
        external_event_id = f"evt-{random.randint(100000, 999999)}"
        
        return {
            "eventName": f"Webinar: {self.fake.catch_phrase()}",
            "eventOrganizer": self.fake.company(),
            "eventDescription": self.fake.paragraph(),
            "eventUrl": self.fake.url(),
            "eventType": random.choice(["webinar", "conference", "tradeshow", "workshop"]),
            
            # REQUIRED / Standard Properties
            "externalAccountId": external_account_id,
            "externalEventId": external_event_id,
            "startDateTime": start_date.isoformat() + "Z", # Marketing events use ISO8601
            "endDateTime": end_date.isoformat() + "Z",
            
            "eventCancelled": False,
            "customProperties": [] # Keeping empty as requested to stick to standard
        }
