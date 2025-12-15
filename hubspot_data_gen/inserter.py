import requests
import json
import math
import time
import logging
from typing import List, Dict, Any, Optional
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from .config import ACCESS_TOKEN, MAX_BATCH_SIZE

# Logger initialized in main.py or via basicConfig if run independently (though not recommended)
logger = logging.getLogger(__name__)

class HubSpotInserter:
    def __init__(self, token: str = ACCESS_TOKEN):
        self.token = token
        self.base_crm_url = "https://api.hubapi.com/crm/v3/objects"
        self.base_marketing_url = "https://api.hubapi.com/marketing/v3"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        self.timeout = 60 # Seconds, recommended 60-90s by HubSpot

    @retry(
        retry=retry_if_exception_type(requests.exceptions.RequestException),
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        reraise=True
    )
    def _post_with_retry(self, url: str, json_data: Any) -> requests.Response:
        """Helper to perform POST requests with retry logic."""
        response = requests.post(url, headers=self.headers, json=json_data, timeout=self.timeout)
        response.raise_for_status()
        return response

    @retry(
        retry=retry_if_exception_type(requests.exceptions.RequestException),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        reraise=True
    )
    def _put_with_retry(self, url: str) -> requests.Response:
         """Helper to perform PUT requests with retry logic."""
         response = requests.put(url, headers=self.headers, timeout=self.timeout)
         response.raise_for_status()
         return response

    def batch_insert(self, object_type: str, records: List[Dict[str, Any]]) -> List[str]:
        """
        Batch insert records. Returns list of IDs of created objects.
        """
        if not self.token and object_type != "dry_run": 
             raise ValueError("HubSpot Access Token is missing. Please set HUBSPOT_ACCESS_TOKEN.")

        created_ids = []

        if object_type == "forms":
            return self._insert_sequential(object_type, records, f"{self.base_marketing_url}/forms")
        elif object_type == "marketing_emails":
            return self._insert_sequential(object_type, records, f"{self.base_marketing_url}/emails")
        elif object_type == "marketing_events":
            return self._insert_sequential(object_type, records, f"{self.base_marketing_url}/marketing-events/events")
        elif object_type == "campaigns":
            created_ids = self._insert_batch_generic(object_type, records, f"{self.base_marketing_url}/campaigns/batch/create")
            return created_ids
        else:
            return self._insert_batch_generic(object_type, records, f"{self.base_crm_url}/{object_type}/batch/create")

    def _insert_batch_generic(self, object_type: str, records: List[Dict[str, Any]], url: str) -> List[str]:
        total_records = len(records)
        logger.info(f"Starting batch insert for {total_records} {object_type}...")
        all_created_ids = []

        for i in range(0, total_records, MAX_BATCH_SIZE):
            chunk = records[i:i + MAX_BATCH_SIZE]
            inputs = [{"properties": record} for record in chunk]
            payload = {"inputs": inputs}
            
            try:
                response = self._post_with_retry(url, payload)
                data = response.json()
                
                # Collect IDs
                if "results" in data:
                    ids = [item["id"] for item in data["results"]]
                    all_created_ids.extend(ids)
                    
                logger.info(f"Successfully inserted batch {i // MAX_BATCH_SIZE + 1} ({len(chunk)} records).")
            except requests.exceptions.RequestException as e:
                self._log_hubspot_error(e, f"inserting batch {i // MAX_BATCH_SIZE + 1}")
                # Don't create 'response' variable as it's not needed with helper
            
            # Rate Limit Sleep (Basic throttle on top of retry)
            time.sleep(1.0) 
        
        return all_created_ids

    def _insert_sequential(self, object_type: str, records: List[Dict[str, Any]], url: str) -> List[str]:
        logger.info(f"Starting sequential insert for {len(records)} {object_type}...")
        created_ids = []
        for index, record in enumerate(records):
            try:
                response = self._post_with_retry(url, record)
                data = response.json()
                if "id" in data:
                    created_ids.append(data["id"])
                elif "externalEventId" in record:
                     created_ids.append(record["externalEventId"])
                
                logger.info(f"Created {object_type} {index + 1}/{len(records)}")
            except requests.exceptions.RequestException as e:
                self._log_hubspot_error(e, f"creating {object_type} {index + 1}")
            
            # Rate Limit Sleep for sequential
            time.sleep(0.3)
            
        return created_ids

    def insert_campaign_sub_items(self, campaign_ids: List[str], generator):
        """Add Budget and Spend items to created campaigns."""
        logger.info(f"Adding Budget and Spend items to {len(campaign_ids)} campaigns...")
        
        for campaign_id in campaign_ids:
            # Add Budget
            try:
                budget = generator.generate_budget_item()
                url = f"{self.base_marketing_url}/campaigns/{campaign_id}/budget"
                self._post_with_retry(url, budget)
            except Exception as e:
                logger.error(f"Failed to add budget to campaign {campaign_id}: {e}")

            # Add Spend
            try:
                spend = generator.generate_spend_item()
                url = f"{self.base_marketing_url}/campaigns/{campaign_id}/spend"
                self._post_with_retry(url, spend)
            except Exception as e:
                logger.error(f"Failed to add spend to campaign {campaign_id}: {e}")
            
            time.sleep(0.2) 

    def associate_assets_to_campaigns(self, campaign_ids: List[str], asset_map: Dict[str, List[str]]):
        """Associate assets to campaigns."""
        logger.info("Associating assets to campaigns...")
        
        for asset_type, asset_ids in asset_map.items():
            if not asset_ids:
                continue
                
            for i, asset_id in enumerate(asset_ids):
                if not campaign_ids: break
                campaign_id = campaign_ids[i % len(campaign_ids)]
                
                url = f"{self.base_marketing_url}/campaigns/{campaign_id}/assets/{asset_type}/{asset_id}"
                
                try:
                    self._put_with_retry(url)
                    logger.info(f"Linked {asset_type} {asset_id} to campaign {campaign_id}")
                except Exception as e:
                    self._log_hubspot_error(e, f"linking {asset_type} {asset_id} to {campaign_id}")
                
                time.sleep(0.2)

    def _log_hubspot_error(self, e: Exception, context: str):
        """Helper to log detailed HubSpot errors."""
        logger.error(f"Failed {context}: {e}")
        
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_data = e.response.json()
                logger.error(f"Full Error Response: {json.dumps(error_data, indent=2)}")
                
                message = error_data.get('message', 'No message')
                
                logger.error(f"HubSpot Message: {message}")
                
                if 'failures' in error_data: # Batch failures
                    for failure in error_data['failures']:
                        logger.error(f"Failure Detail: {failure}")

                if 'errors' in error_data: # Standard validation errors
                    for err in error_data['errors']:
                        prop_name = err.get('context', {}).get('propertyName', ['Unknown Property'])[0]
                        err_msg = err.get('message', '')
                        logger.error(f"-> Field '{prop_name}': {err_msg}")
                        
            except ValueError:
                # Not JSON
                logger.error(f"Raw Response: {e.response.text}")
