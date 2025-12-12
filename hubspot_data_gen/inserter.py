import requests
import json
import math
from typing import List, Dict, Any
from .config import ACCESS_TOKEN, MAX_BATCH_SIZE

class HubSpotInserter:
    def __init__(self, token: str = ACCESS_TOKEN):
        self.token = token
        self.base_url = "https://api.hubapi.com/crm/v3/objects"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def batch_insert(self, object_type: str, records: List[Dict[str, Any]]):
        """
        Batch insert records into HubSpot.
        :param object_type: 'contacts', 'companies', 'deals', 'tickets'
        :param records: List of dictionaries containing properties
        """
        if not self.token:
            raise ValueError("HubSpot Access Token is missing. Please set HUBSPOT_ACCESS_TOKEN in env or config.")

        total_records = len(records)
        print(f"Starting batch insert for {total_records} {object_type}...")

        # Chunk records
        for i in range(0, total_records, MAX_BATCH_SIZE):
            chunk = records[i:i + MAX_BATCH_SIZE]
            inputs = [{"properties": record} for record in chunk]
            payload = {"inputs": inputs}
            
            url = f"{self.base_url}/{object_type}/batch/create"
            response = None
            
            try:
                response = requests.post(url, headers=self.headers, json=payload)
                response.raise_for_status()
                print(f"Successfully inserted batch {i // MAX_BATCH_SIZE + 1} ({len(chunk)} records).")
            except requests.exceptions.RequestException as e:
                print(f"Error inserting batch {i // MAX_BATCH_SIZE + 1}: {e}")
                if response is not None:
                     print("Response:", response.text)
