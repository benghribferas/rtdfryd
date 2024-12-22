"""Google Sheets service and data handling."""
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from config import WORKSHEET_NAME, VENDOR_COLUMNS

class GSheetsService:
    def __init__(self):
        """Initialize the Google Sheets service."""
        self.conn = st.connection("gsheets", type=GSheetsConnection)

    def fetch_vendors(self) -> pd.DataFrame:
        """Fetch vendor data from Google Sheets."""
        try:
            data = self.conn.read(
                worksheet=WORKSHEET_NAME,
                usecols=VENDOR_COLUMNS,
                ttl=5
            )
            cleaned_data = data.dropna(how="all")
            return cleaned_data if not cleaned_data.empty else pd.DataFrame()
            
        except Exception as e:
            st.error(f"Error fetching vendor data: {str(e)}")
            return pd.DataFrame()