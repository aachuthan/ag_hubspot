import random
from typing import Dict, Any
from datetime import datetime
from .base import BaseGenerator

class NoteGenerator(BaseGenerator):
    def generate_one(self) -> Dict[str, Any]:
        # Properties for Notes (CRM Object)
        ts = str(int(datetime.now().timestamp() * 1000))
        
        return {
            "hs_timestamp": ts, # REQUIRED
            "hs_note_body": self.fake.paragraph(nb_sentences=5),
        }
