# HubSpot Dummy Data Generator

A modular Python application to generate and insert dummy data into HubSpot CRM and Marketing Hub. 

## 🚀 Quick Start

1.  **Install**: `pip install -r requirements.txt`
2.  **Token**: `export HUBSPOT_ACCESS_TOKEN="your-token"`
3.  **Run**: `python main.py --all-marketing --count 5`

---

## Features

- **CRM Objects**: Contacts, Companies, Deals, Tickets (Batch Insert).
- **Marketing Objects**: Campaigns (with Budget & Spend), Forms, Marketing Events.
- **Engagements**: Meetings, Emails (logged to CRM).
- **Orchestration**: Automatically links generated Assets (Forms) to generated Campaigns.

## Setup

1.  **Prerequisites**: Python 3.8+ installed.

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure API Token**:
    Create a Private App in HubSpot and ensure it has the **Required Scopes** (see below).
    Set the `HUBSPOT_ACCESS_TOKEN` environment variable.
    
    *Windows (PowerShell)*:
    ```powershell
    $env:HUBSPOT_ACCESS_TOKEN = "your-private-app-access-token"
    ```
    *Mac/Linux*:
    ```bash
    export HUBSPOT_ACCESS_TOKEN="your-private-app-access-token"
    ```

### Required Scopes
Ensure your Private App has these scopes enabled:
- `crm.objects.contacts.write`
- `crm.objects.companies.write`
- `crm.objects.deals.write`
- `crm.objects.tickets.write`
- `files` (often needed for assets)
- `forms` (for Forms API)
- `marketing.campaigns.write` (for Campaigns, Budget, Assets)
- `crm.objects.marketing_events.write`
- `crm.objects.contacts.read` (for linking)

## Usage

### 1. Marketing Hub Orchestration (Recommended)
Generates Forms and Campaigns, then links them together and adds budget items.

```bash
# Generate 10 items total and insert to HubSpot
python main.py --all-marketing --count 10

# Dry run (preview only)
python main.py --all-marketing --count 10 --dry-run
```

### 2. Single Object Generation
```bash
# CRM
python main.py --object contacts --count 50
python main.py --object companies --count 20
python main.py --object deals --count 20
python main.py --object tickets --count 10

# Engagements
python main.py --object meetings --count 10
python main.py --object emails --count 10

# Marketing
python main.py --object campaigns --count 5
python main.py --object forms --count 5
python main.py --object marketing_events --count 5
```

## Debugging

**VS Code**:
1.  Open **Run and Debug** (`Ctrl+Shift+D`).
2.  Select **"Python: Insert Contacts (Live)"** and press **F5**.

**CLI**:
```bash
python -m pdb main.py --object contacts --count 1 --dry-run
```

## Troubleshooting
- **401 Unauthorized**: Check your `HUBSPOT_ACCESS_TOKEN`. Ensure no extra spaces.
- **403 Forbidden**: Check your **Scopes**. You likely missed one (e.g., `marketing.campaigns.write`).
- **429 Too Many Requests**: The tool handles this automatically, but if you see it often, wait a few minutes.
