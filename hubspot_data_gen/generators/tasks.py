import random
from typing import Dict, Any
from datetime import datetime, timedelta
from .base import BaseGenerator

class TaskGenerator(BaseGenerator):
    def generate_one(self) -> Dict[str, Any]:
        # Properties for Tasks (CRM Object)
        due_date = datetime.now() + timedelta(days=random.randint(1, 7))
        due_ts = str(int(due_date.timestamp() * 1000))
        
        return {
            "hs_timestamp": due_ts, # REQUIRED: Due Date
            
            "hs_task_subject": f"Task: {self.fake.bs().title()}",
            "hs_task_body": self.fake.sentence(),
            "hs_task_priority": random.choice(["LOW", "MEDIUM", "HIGH"]),
            "hs_task_status": random.choice(["WAITING", "COMPLETED", "DEFERRED", "NOT_STARTED", "IN_PROGRESS"]),
            "hs_task_type": random.choice(["TODO", "EMAIL", "CALL"]),
            "hs_task_reminders": str(int((due_date - timedelta(hours=1)).timestamp() * 1000)), # Reminder 1 hour before
        }
