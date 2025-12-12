import os

# HubSpot API Configuration
ACCESS_TOKEN = os.getenv("HUBSPOT_ACCESS_TOKEN", "")

# Generation Configuration
DEFAULT_BATCH_SIZE = 10
MAX_BATCH_SIZE = 100
