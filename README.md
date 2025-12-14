# HubSpot Data Generator

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![HubSpot API](https://img.shields.io/badge/HubSpot-API%20v3-orange)
![License](https://img.shields.io/badge/license-MIT-green)

A modular, extensible Python application designed to generate rich dummy data for HubSpot's CRM and Marketing Hub. It ensures all data adheres to HubSpot's standard properties and API requirements, making it ideal for testing integrations, dashboards, and workflows.

## ✨ Features

- **Rich Marketing Objects**:
  - **Campaigns**: Generates campaigns with correct `hs_` properties, UTM parameters, budget, and spend data.
  - **Forms**: Creates GDPR-compliant forms with proper context (cookies, page URI) and contact field mappings.
  - **Marketing Events**: Simulates webinars/conferences with valid ISO timestamps and external IDs.
- **Robust CRM Data**:
  - **Standard Objects**: Contacts, Companies, Deals, Tickets, Products.
  - **Engagements**: Logs Meetings, Emails, Calls, Tasks, and Notes with rich metadata.
- **Orchestration**:
  - Automatically links generated Assets (like Forms) to Campaigns.
  - Simulates sequential user journeys (e.g., Contact -> Form Submit -> Deal Created).
- **Bulk Ingestion**:
  - Efficiently creates records in batches (up to 100 at a time) to respect API rate limits.
- **Developer Guide**:
  - See [General CRM Ingestion Guidelines](GENERAL_CRM_INGESTION_GUIDELINES.md) for architectural patterns and best practices.

## 📂 Project Structure

```text
hubspot_data_gen/
├── generators/           # Logic for creating dummy data dictionaries
│   ├── base.py           # Base generator class using Faker
│   ├── campaigns.py      # Campaign generation
│   ├── calls.py          # Call engagement generation
│   ├── ...               # Other object generators
├── inserter.py           # Logic for batching and sending data to HubSpot API
├── main.py               # CLI Entry point
```

## 🛠️ Setup

### 1. Prerequisites
- Python 3.8 or higher
- A HubSpot Portal (Test account recommended)

### 2. Installation
```bash
pip install -r requirements.txt
```

### 3. Configuration
You need a **Private App Access Token** from your HubSpot portal.

**Set Environment Variable:**
- **Windows (PowerShell)**: `$env:HUBSPOT_ACCESS_TOKEN = "your-token"`
- **Mac/Linux**: `export HUBSPOT_ACCESS_TOKEN="your-token"`

### 4. Required Scopes
Ensure your Private App has the following scopes enabled:

| Category | Scopes | Purpose |
|----------|--------|---------|
| **CRM** | `crm.objects.contacts.write` | Create Contacts |
| | `crm.objects.companies.write` | Create Companies |
| | `crm.objects.deals.write` | Create Deals |
| | `crm.objects.tickets.write` | Create Tickets |
| **Engagements** | `crm.objects.contacts.write` | (Often covers standard engagements) |
| | *Note: Some portals split engagement scopes.* | |
| **Marketing** | `marketing.campaigns.write` | Create Campaigns, Assets |
| | `forms` | Create Forms |
| | `crm.objects.marketing_events.write` | Create Marketing Events |

## 🚀 Usage

You can generate and bulk insert any of the following supported objects. The tool automatically handles batching.

### 1. CRM Objects
```bash
python main.py --object contacts --count 100
python main.py --object companies --count 50
python main.py --object deals --count 50
python main.py --object tickets --count 20
python main.py --object products --count 20
```

### 2. Engagements (HubSpot V3 Objects)
These create engagement records directly in the CRM.
```bash
python main.py --object meetings --count 10
python main.py --object emails --count 10
python main.py --object calls --count 10
python main.py --object tasks --count 10
python main.py --object notes --count 10
```

### 3. Marketing Objects
```bash
python main.py --object campaigns --count 5
python main.py --object marketing_events --count 5
# Forms (Note: Forms API is sequential)
python main.py --object forms --count 5
```

### 4. Full Dry Run (Safe Test)
Preview the data that *would* be sent without actually touching your HubSpot portal.
```bash
python main.py --object calls --count 1 --dry-run
```

## 🐛 Debugging & Troubleshooting

- **401 Unauthorized**: verification failed. Check `HUBSPOT_ACCESS_TOKEN`.
- **403 Forbidden**: Missing scopes. Check the **Required Scopes** table above.
- **Properties Errors**: If you see errors about "read-only" properties, ensure you are not trying to write to system headers. This tool is tuned to use only writable `hs_` standard properties.

### VS Code Debugging
1. Open the **Run and Debug** tab (`Ctrl+Shift+D`).
2. Select "Python: Current File" or configure a `launch.json` for `main.py` with arguments.
