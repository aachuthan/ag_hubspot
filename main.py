import argparse
import sys
import os
import logging
from typing import List, Dict, Any

# Configure logging
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Clear existing handlers to avoid duplication if re-run
if root_logger.hasHandlers():
    root_logger.handlers.clear()

# Console Handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
root_logger.addHandler(console_handler)

# File Handler (Errors only)
file_handler = logging.FileHandler("error.log", mode='a', encoding='utf-8')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)
root_logger.addHandler(file_handler)

logger = logging.getLogger(__name__)

from hubspot_data_gen.generators import (
    ContactGenerator, CompanyGenerator, DealGenerator, TicketGenerator,
    CampaignGenerator, FormGenerator, MeetingGenerator, 
    EmailEngagementGenerator, MarketingEventGenerator,
    CallGenerator, TaskGenerator, NoteGenerator, ProductGenerator
)
from hubspot_data_gen.inserter import HubSpotInserter

def main():
    parser = argparse.ArgumentParser(description="Generate and insert dummy data into HubSpot.")
    parser.add_argument("--object", "-o", type=str, 
                        choices=["contacts", "companies", "deals", "tickets", 
                                 "campaigns", "forms", "meetings", "emails", "marketing_events",
                                 "calls", "tasks", "notes", "products"],
                        help="The object type to generate data for.")
    parser.add_argument("--count", "-c", type=int, default=10, 
                        help="Number of records to generate.")
    parser.add_argument("--dry-run", action="store_true", 
                        help="Generate data but do not insert into HubSpot.")
    parser.add_argument("--all-marketing", action="store_true",
                        help="Run full marketing flow: Assets -> Campaigns -> Linking.")

    args = parser.parse_args()
    
    # Validation
    if not args.object and not args.all_marketing:
        parser.print_help()
        sys.exit(1)

    # Pre-flight Check: Token
    if not args.dry_run:
        token = os.getenv("HUBSPOT_ACCESS_TOKEN")
        if not token:
            logger.error("HUBSPOT_ACCESS_TOKEN environment variable not set.")
            logger.error("Please set it before running in live mode.")
            logger.error("Example (PowerShell): $env:HUBSPOT_ACCESS_TOKEN = 'your-token'")
            sys.exit(1)

    inserter = HubSpotInserter()

    try:
        if args.all_marketing:
            run_marketing_orchestration(inserter, args.count, args.dry_run)
        else:
            run_single_object(inserter, args.object, args.count, args.dry_run)
    except Exception as e:
        logger.critical(f"An unexpected error occurred: {e}")
        # In debug mode (or if user wants) we could re-raise.
        # raise e 

def get_generator(obj_type: str):
    if obj_type == "contacts": return ContactGenerator()
    elif obj_type == "companies": return CompanyGenerator()
    elif obj_type == "deals": return DealGenerator()
    elif obj_type == "tickets": return TicketGenerator()
    elif obj_type == "campaigns": return CampaignGenerator()
    elif obj_type == "forms": return FormGenerator()
    elif obj_type == "meetings": return MeetingGenerator()
    elif obj_type == "emails": return EmailEngagementGenerator()
    elif obj_type == "marketing_events": return MarketingEventGenerator()
    elif obj_type == "calls": return CallGenerator()
    elif obj_type == "tasks": return TaskGenerator()
    elif obj_type == "notes": return NoteGenerator()
    elif obj_type == "products": return ProductGenerator()
    return None

def run_single_object(inserter, obj_type, count, dry_run):
    generator = get_generator(obj_type)
    if not generator:
        logger.error(f"Unknown Object: {obj_type}")
        return

    logger.info(f"Generating {count} {obj_type}...")
    try:
        data = generator.generate(count)
    except Exception as e:
         logger.error(f"Failed to generate data for {obj_type}: {e}")
         return

    if dry_run:
        logger.info(f"Dry run for {obj_type}. Example:")
        print(data[0] if data else "No data") # Keep print for data output to be clean
    else:
        inserter.batch_insert(obj_type, data)

def run_marketing_orchestration(inserter, count, dry_run):
    logger.info("=== Starting Marketing Hub Orchestration ===")
    
    # 1. Generate Assets
    # Forms
    form_gen = FormGenerator()
    logger.info(f"Generating forms...")
    forms_data = form_gen.generate(max(1, count // 2))
    form_ids = []
    
    if not dry_run:
        form_ids = inserter.batch_insert("forms", forms_data)
    else:
        logger.info(f"[Dry Run] Generated {len(forms_data)} forms.")

    # 2. Generate Campaigns
    camp_gen = CampaignGenerator()
    logger.info(f"Generating campaigns...")
    camp_data = camp_gen.generate(max(1, count // 5)) 
    camp_ids = []
    
    if not dry_run:
        camp_ids = inserter.batch_insert("campaigns", camp_data)
        
        # 3. Add Budget/Spend
        if camp_ids:
            inserter.insert_campaign_sub_items(camp_ids, camp_gen)
        
        # 4. Link Assets
        if camp_ids and form_ids:
            asset_map = {
                "form": form_ids 
            }
            inserter.associate_assets_to_campaigns(camp_ids, asset_map)
        elif not camp_ids:
            logger.warning("No campaigns created, skipping linking.")
        
    else:
        logger.info(f"[Dry Run] Generated {len(camp_data)} campaigns + Budget/Spend simulation.")
        logger.info(f"[Dry Run] Would link {len(forms_data)} forms to these campaigns.")

if __name__ == "__main__":
    main()
