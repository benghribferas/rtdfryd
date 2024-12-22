"""Google Sheets API service."""
from typing import List, Optional
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build, Resource
from src.config import SPREADSHEET_ID, RANGE_NAME

class GoogleSheetsService:
    def __init__(self, credentials_path: str):
        """Initialize the Google Sheets service.
        
        Args:
            credentials_path: Path to the service account credentials file
        """
        self.credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
        self.service: Resource = build('sheets', 'v4', credentials=self.credentials)

    def fetch_vendors(self) -> Optional[pd.DataFrame]:
        """Fetch vendor data from Google Sheets.
        
        Returns:
            DataFrame containing vendor data or None if there's an error
        """
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=SPREADSHEET_ID,
                range=RANGE_NAME
            ).execute()
            
            values: List[List[str]] = result.get('values', [])
            if not values:
                return None
                
            df = pd.DataFrame(values[1:], columns=values[0])
            return df.dropna(how='all')
            
        except Exception as e:
            print(f"Error fetching vendor data: {str(e)}")
            return None