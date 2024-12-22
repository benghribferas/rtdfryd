"""Configuration settings for the application."""
from typing import List

# Google Sheets Configuration
SPREADSHEET_URL: str = "https://docs.google.com/spreadsheets/d/1wyO6gZAF3W4V8L9VhxlBijhlkXpvHwe9v5Z9_4UQtic/edit?gid=0#gid=0"
WORKSHEET_NAME: str = "Vendors"
VENDOR_COLUMNS: List[int] = list(range(6))

# Vendor Fields
VENDOR_FIELDS = [
    "Company Name",
    "Contact Person",
    "Email",
    "Phone",
    "Address",
    "Status"
]