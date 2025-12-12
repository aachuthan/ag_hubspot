import requests
import json
import math
from typing import List, Dict, Any, Optional
from .config import ACCESS_TOKEN, MAX_BATCH_SIZE

class HubSpotInserter:
    def __init__(self, token: str = ACCESS_TOKEN):
        self.token = token
        self.base_crm_url = "https://api.hubapi.com/crm/v3/objects"
        self.base_marketing_url = "https://api.hubapi.com/marketing/v3"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def batch_insert(self, object_type: str, records: List[Dict[str, Any]]) -> List[str]:
        """
        Batch insert records. Returns list of IDs of created objects.
        """
        if not self.token and object_type != "dry_run": # Allow dry run check outside
             raise ValueError("HubSpot Access Token is missing.")

        created_ids = []

        if object_type == "forms":
            return self._insert_sequential(object_type, records, f"{self.base_marketing_url}/forms")
        elif object_type == "marketing_events":
            # Marketing Events uses externalEventId usually, but we can POST to root.
            # No batch endpoint documented for creation, so sequential.
            return self._insert_sequential(object_type, records, f"{self.base_marketing_url}/marketing-events/events")
        elif object_type == "campaigns":
            created_ids = self._insert_batch_generic(object_type, records, f"{self.base_marketing_url}/campaigns/batch/create")
            # Handle Budget/Spend for Campaigns
            # (Requires iterating created IDs, which we get from response)
            return created_ids
        else:
            # CRM Objects (contacts, companies, deals, tickets, meetings, emails)
            return self._insert_batch_generic(object_type, records, f"{self.base_crm_url}/{object_type}/batch/create")

    def _insert_batch_generic(self, object_type: str, records: List[Dict[str, Any]], url: str) -> List[str]:
        total_records = len(records)
        print(f"Starting batch insert for {total_records} {object_type}...")
        all_created_ids = []

        for i in range(0, total_records, MAX_BATCH_SIZE):
            chunk = records[i:i + MAX_BATCH_SIZE]
            inputs = [{"properties": record} for record in chunk]
            payload = {"inputs": inputs}
            
            try:
                response = requests.post(url, headers=self.headers, json=payload)
                response.raise_for_status()
                data = response.json()
                
                # Collect IDs
                if "results" in data:
                    ids = [item["id"] for item in data["results"]]
                    all_created_ids.extend(ids)
                    
                print(f"Successfully inserted batch {i // MAX_BATCH_SIZE + 1} ({len(chunk)} records).")
            except requests.exceptions.RequestException as e:
                print(f"Error inserting batch {i // MAX_BATCH_SIZE + 1}: {e}")
                if response is not None:
                     print("Response:", response.text)
        
        return all_created_ids

    def _insert_sequential(self, object_type: str, records: List[Dict[str, Any]], url: str) -> List[str]:
        print(f"Starting sequential insert for {len(records)} {object_type}...")
        created_ids = []
        for index, record in enumerate(records):
            try:
                response = requests.post(url, headers=self.headers, json=record)
                response.raise_for_status()
                data = response.json()
                if "id" in data:
                    created_ids.append(data["id"])
                elif "externalEventId" in record: # Marketing Events might use this
                     created_ids.append(record["externalEventId"])
                
                print(f"Created {object_type} {index + 1}/{len(records)}")
            except requests.exceptions.RequestException as e:
                print(f"Error creating {object_type} {index + 1}: {e}")
                if response is not None:
                     print("Response:", response.text)
        return created_ids

    def insert_campaign_sub_items(self, campaign_ids: List[str], generator):
        """Add Budget and Spend items to created campaigns."""
        print(f"Adding Budget and Spend items to {len(campaign_ids)} campaigns...")
        
        for campaign_id in campaign_ids:
            # Add Budget
            try:
                budget = generator.generate_budget_item()
                url = f"{self.base_marketing_url}/campaigns/{campaign_id}/budget"
                requests.post(url, headers=self.headers, json=budget)
            except Exception as e:
                print(f"Failed to add budget to campaign {campaign_id}: {e}")

            # Add Spend
            try:
                spend = generator.generate_spend_item()
                url = f"{self.base_marketing_url}/campaigns/{campaign_id}/spend"
                requests.post(url, headers=self.headers, json=spend)
            except Exception as e:
                print(f"Failed to add spend to campaign {campaign_id}: {e}")

    def associate_assets_to_campaigns(self, campaign_ids: List[str], asset_map: Dict[str, List[str]]):
        """
        Associate assets to campaigns.
        asset_map: {"form": [id1, id2], "email": [id3, id4]}
        Distributes assets round-robin to campaigns.
        """
        print("Associating assets to campaigns...")
        
        for asset_type, asset_ids in asset_map.items():
            if not asset_ids:
                continue
                
            for i, asset_id in enumerate(asset_ids):
                # Assign to a campaign (round robin)
                if not campaign_ids: break
                campaign_id = campaign_ids[i % len(campaign_ids)]
                
                url = f"{self.base_marketing_url}/campaigns/{campaign_id}/assets/{asset_type}/{asset_id}"
                
                try:
                    requests.put(url, headers=self.headers)
                    print(f"Linked {asset_type} {asset_id} to campaign {campaign_id}")
                except Exception as e:
                    # Often 409 if already associated, or 404 if not found
                    print(f"Failed to link {asset_type} {asset_id} to {campaign_id}: {e}")
