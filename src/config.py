"""Configuration settings for the application."""
from typing import List

# Google Sheets Configuration
SPREADSHEET_ID: str = "1wyO6gZAF3W4V8L9VhxlBijhlkXpvHwe9v5Z9_4UQtic"
RANGE_NAME: str = "Vendors!A:F"

# Vendor Fields
VENDOR_FIELDS: List[str] = [
    "Company Name",
    "Contact Person",
    "Email",
    "Phone",
    "Address",
    "Status"
]