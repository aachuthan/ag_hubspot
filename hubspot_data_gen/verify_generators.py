import sys
import os

# Add project root to path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from hubspot_data_gen.generators.campaigns import CampaignGenerator
from hubspot_data_gen.generators.marketing_events import MarketingEventGenerator
from hubspot_data_gen.generators.forms import FormGenerator
from hubspot_data_gen.generators.meetings import MeetingGenerator
from hubspot_data_gen.generators.email_engagements import EmailEngagementGenerator

def verify_dict_keys(data, required_keys, name):
    missing = [key for key in required_keys if key not in data]
    if missing:
        print(f"[FAIL] {name} missing keys: {missing}")
        return False
    print(f"[PASS] {name} has all required keys.")
    return True

def main():
    print("Verifying Generators...")
    
    # Campaigns
    camp_gen = CampaignGenerator()
    camp_data = camp_gen.generate_one()
    camp_keys = ["hs_name", "hs_start_date", "hs_end_date", "hs_campaign_status", "hs_utm_campaign"]
    verify_dict_keys(camp_data, camp_keys, "Campaigns")
    print(f"  > Campaign Dates: Start={camp_data['hs_start_date']}, End={camp_data['hs_end_date']}")
    budget_item = camp_gen.generate_budget_item()
    spend_item = camp_gen.generate_spend_item()
    print(f"  > Spend Date: {spend_item['date']}")

    # Marketing Events
    event_gen = MarketingEventGenerator()
    event_data = event_gen.generate_one()
    event_keys = ["externalAccountId", "externalEventId", "startDateTime", "eventType"]
    verify_dict_keys(event_data, event_keys, "Marketing Events")
    print(f"  > Event Dates: Start={event_data['startDateTime']}, End={event_data['endDateTime']}")

    # Forms
    form_gen = FormGenerator()
    form_data = form_gen.generate_one()
    # Check legalConsentOptions in configuration
    if "legalConsentOptions" in form_data.get("configuration", {}):
        print("[PASS] Forms has legalConsentOptions")
    else:
        print("[FAIL] Forms missing legalConsentOptions")
    
    if "context" in form_data:
        print("[PASS] Forms has context object")
    else:
        print("[FAIL] Forms missing context object")

    # Meetings
    meet_gen = MeetingGenerator()
    meet_data = meet_gen.generate_one()
    meet_keys = ["hs_timestamp", "hs_meeting_title", "hs_activity_type", "hs_meeting_start_time"]
    verify_dict_keys(meet_data, meet_keys, "Meetings")
    print(f"  > Meeting Timestamp: {meet_data['hs_timestamp']}")

    # Emails
    email_gen = EmailEngagementGenerator()
    email_data = email_gen.generate_one()
    email_keys = ["hs_timestamp", "hs_email_subject", "hs_email_html", "hs_email_headers"]
    verify_dict_keys(email_data, email_keys, "Emails")
    print(f"  > Email Timestamp: {email_data['hs_timestamp']}")

if __name__ == "__main__":
    main()
