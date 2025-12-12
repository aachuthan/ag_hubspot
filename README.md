# HubSpot Dummy Data Generator

A modular Python application to generate and insert dummy data into HubSpot CRM and Marketing Hub. This tool supports creating Contacts, Companies, Deals, Tickets, as well as Marketing Campaigns, Forms, Events, and Engagements.

## Features

- **CRM Objects**: Contacts, Companies, Deals, Tickets (Batch Insert).
- **Marketing Objects**: Campaigns (with Budget & Spend), Forms, Marketing Events.
- **Engagements**: Meetings, Emails (logged to CRM).
- **Orchestration**: Automatically links generated Assets (Forms) to generated Campaigns.
- **Dry Run**: Preview data generation without hitting the API.

## Setup

1.  **Prerequisites**: Python 3.8+ installed.

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure API Token**:
    Set the `HUBSPOT_ACCESS_TOKEN` environment variable with your Private App Access Token.
    
    *Windows (PowerShell)*:
    ```powershell
    $env:HUBSPOT_ACCESS_TOKEN = "your-private-app-access-token"
    ```
    *Mac/Linux*:
    ```bash
    export HUBSPOT_ACCESS_TOKEN="your-private-app-access-token"
    ```

## Usage

Run `main.py` to generate data.

### 1. Marketing Hub Orchestration (Recommended)
Generates Forms and Campaigns, then links them together and adds budget items.

```bash
# Generate 10 items total (Forms, Campaigns, Assets) and insert to HubSpot
python main.py --all-marketing --count 10

# Dry run (preview only)
python main.py --all-marketing --count 10 --dry-run
```

### 2. Single Object Generation
Generate specific objects individually.

**CRM Objects:**
```bash
python main.py --object contacts --count 50
python main.py --object companies --count 20
python main.py --object deals --count 20
python main.py --object tickets --count 10
python main.py --object meetings --count 10
python main.py --object emails --count 10
```

**Marketing Objects:**
```bash
python main.py --object campaigns --count 5
python main.py --object forms --count 5
python main.py --object marketing_events --count 5
```

### Options
- `--count, -c`: Number of records to generate (default: 10).
- `--dry-run`: Print generated data to console instead of sending to HubSpot.
- `--all-marketing`: Enable full marketing orchestration flow.

## Debugging

**VS Code**:
1.  Open the **Run and Debug** view (`Ctrl+Shift+D`).
2.  Select **"Python: Insert Contacts (Live)"** or **"Python: Dry Run Contacts"**.
3.  Press **F5**.
    *Note: You can pass custom arguments by editing `.vscode/launch.json`.*

**CLI**:
```bash
python -m pdb main.py --object contacts --count 1 --dry-run
```
