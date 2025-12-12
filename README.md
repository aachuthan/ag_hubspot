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
  - **Standard Objects**: Contacts, Companies, Deals, Tickets with batch insertion support.
  - **Engagements**: Logs Meetings (with outcomes, locations) and Emails (in/out direction, HTML content) to the CRM.
- **Orchestration**:
  - Automatically links generated Assets (like Forms) to Campaigns.
  - Simulates sequential user journeys (e.g., Contact -> Form Submit -> Deal Created).

## 📂 Project Structure

```text
hubspot_data_gen/
├── generators/           # Logic for creating dummy data dictionaries
│   ├── base.py           # Base generator class using Faker
│   ├── campaigns.py      # Campaign & Budget generation
│   ├── forms.py          # Form v3 payload generation
│   ├── ...               # Other object generators
├── inserters/            # Logic for sending data to HubSpot API
│   ├── base.py           # Base API handler (auth, batching)
│   ├── marketing.py      # Marketing-specific insertion logic
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
| **CRM** | `crm.objects.contacts.write`, `crm.objects.contacts.read` | Create/Link Contacts |
| | `crm.objects.companies.write` | Create Companies |
| | `crm.objects.deals.write` | Create Deals |
| | `crm.objects.tickets.write` | Create Tickets |
| **Marketing** | `marketing.campaigns.write` | Create Campaigns, Assets |
| | `forms` | Create Forms |
| | `crm.objects.marketing_events.write` | Create Marketing Events |
| **Files** | `files` | (Optional) For asset management |

## 🚀 Usage

### Marketing Hub Orchestration (Recommended)
Generates a complete marketing dataset: Campaigns, Forms, and Marketing Events, properly linked and populated.

```bash
# Generate 10 sets of marketing data
python main.py --all-marketing --count 10

# Dry Run (Preview payload without sending to HubSpot)
python main.py --all-marketing --count 1 --dry-run
```

### Single Object Generation
Generate specific objects in isolation.

```bash
# CRM Objects
python main.py --object contacts --count 50
python main.py --object deals --count 20

# Engagements
python main.py --object meetings --count 10
python main.py --object emails --count 10

# Marketing Objects
python main.py --object campaigns --count 5
```

## 🐛 Debugging & Troubleshooting

- **401 Unauthorized**: verification failed. Check `HUBSPOT_ACCESS_TOKEN`.
- **403 Forbidden**: Missing scopes. Check the **Required Scopes** table above.
- **Properties Errors**: If you see errors about "read-only" properties, ensure you are not trying to write to system headers. This tool is tuned to use only writable `hs_` standard properties.

### VS Code Debugging
1. Open the **Run and Debug** tab (`Ctrl+Shift+D`).
2. Select "Python: Current File" or configure a `launch.json` for `main.py` with arguments.
