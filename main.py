import argparse
import sys
import os
from typing import List, Dict, Any
from hubspot_data_gen.generators import (
    ContactGenerator, CompanyGenerator, DealGenerator, TicketGenerator,
    CampaignGenerator, FormGenerator, MeetingGenerator, 
    EmailEngagementGenerator, MarketingEventGenerator
)
from hubspot_data_gen.inserter import HubSpotInserter

def main():
    parser = argparse.ArgumentParser(description="Generate and insert dummy data into HubSpot.")
    parser.add_argument("--object", "-o", type=str, 
                        choices=["contacts", "companies", "deals", "tickets", 
                                 "campaigns", "forms", "meetings", "emails", "marketing_events"],
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
            print("\n[ERROR] HUBSPOT_ACCESS_TOKEN environment variable not set.")
            print("Please set it before running in live mode.")
            print("Example (PowerShell): $env:HUBSPOT_ACCESS_TOKEN = 'your-token'")
            sys.exit(1)

    inserter = HubSpotInserter()

    try:
        if args.all_marketing:
            run_marketing_orchestration(inserter, args.count, args.dry_run)
        else:
            run_single_object(inserter, args.object, args.count, args.dry_run)
    except Exception as e:
        print(f"\n[CRITICAL ERROR] An unexpected error occurred: {e}")
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
    return None

def run_single_object(inserter, obj_type, count, dry_run):
    generator = get_generator(obj_type)
    if not generator:
        print(f"Unknown Object: {obj_type}")
        return

    print(f"Generating {count} {obj_type}...")
    try:
        data = generator.generate(count)
    except Exception as e:
         print(f"[ERROR] Failed to generate data for {obj_type}: {e}")
         return

    if dry_run:
        print(f"Dry run for {obj_type}. Example:")
        print(data[0] if data else "No data")
    else:
        inserter.batch_insert(obj_type, data)

def run_marketing_orchestration(inserter, count, dry_run):
    print("=== Starting Marketing Hub Orchestration ===")
    
    # 1. Generate Assets
    # Forms
    form_gen = FormGenerator()
    print(f"Generating forms...")
    forms_data = form_gen.generate(max(1, count // 2))
    form_ids = []
    
    if not dry_run:
        form_ids = inserter.batch_insert("forms", forms_data)
    else:
        print(f"[Dry Run] Generated {len(forms_data)} forms.")

    # 2. Generate Campaigns
    camp_gen = CampaignGenerator()
    print(f"Generating campaigns...")
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
        
    else:
        print(f"[Dry Run] Generated {len(camp_data)} campaigns + Budget/Spend simulation.")
        print(f"[Dry Run] Would link {len(forms_data)} forms to these campaigns.")

if __name__ == "__main__":
    main()
