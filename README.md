# HubSpot Dummy Data Generator

A modular Python application to generate and insert dummy data into HubSpot CRM. This tool allows you to create bulk Contacts, Companies, Deals, and Tickets with realistic data using the Faker library and inserts them via the HubSpot Batch API.

## Project Structure
- `hubspot_data_gen/`: Main package containing generators and insertion logic.
    - `generators/`: Contains `base.py` and specific object generators (`contacts.py`, `companies.py`, `deals.py`, `tickets.py`).
    - `inserter.py`: Handles batch API requests to HubSpot.
    - `config.py`: Configuration (API token).
- `main.py`: CLI entry point.
- `requirements.txt`: Project dependencies.

## Setup

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure API Token:**
    - Set the `HUBSPOT_ACCESS_TOKEN` environment variable with your Private App Access Token.
    - Alternatively, you can edit `hubspot_data_gen/config.py` directly (not recommended for git).

    **PowerShell:**
    ```powershell
    $env:HUBSPOT_ACCESS_TOKEN = "your-private-app-access-token"
    ```
    **Bash/Mac/Linux:**
    ```bash
    export HUBSPOT_ACCESS_TOKEN="your-private-app-access-token"
    ```

## Usage

Run the `main.py` script to generate data. The script supports generating Contacts, Companies, Deals, and Tickets.

### 1. Dry Run (Generate only)
Use the `--dry-run` flag to generate data and verify the output structure without making any API calls to HubSpot.

```bash
python main.py --object contacts --count 5 --dry-run
python main.py --object companies --count 5 --dry-run
python main.py --object deals --count 5 --dry-run
python main.py --object tickets --count 5 --dry-run
```

### 2. Insert Data
Remove the `--dry-run` flag to insert data into your HubSpot portal.

```bash
# Generate and insert 100 contacts
python main.py --object contacts --count 100

# Generate and insert 50 companies
python main.py --object companies --count 50
```

## Features
- **Modular**: Easy to add new object generators in `generators/`.
- **Comprehensive Fields**: Populates maximum standard fields based on HubSpot's latest API documentation.
- **Batch Processing**: Inserts data in batches of 100 to respect API limits and ensure performance.
