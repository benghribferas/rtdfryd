"""Google Sheets connection and data handling."""
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from config import SPREADSHEET_URL, WORKSHEET_NAME, VENDOR_COLUMNS

def get_gsheets_connection() -> GSheetsConnection:
    """Create and return a Google Sheets connection."""
    return st.connection("gsheets", type=GSheetsConnection)

def fetch_vendor_data(conn: GSheetsConnection) -> pd.DataFrame:
    """Fetch and clean vendor data from Google Sheets."""
    try:
        data = conn.read(
            worksheet=WORKSHEET_NAME,
            usecols=VENDOR_COLUMNS,
            ttl=5
        )
        return data.dropna(how="all")
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return pd.DataFrame()