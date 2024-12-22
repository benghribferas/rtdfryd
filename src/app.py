"""Main Streamlit application."""
import streamlit as st
import pandas as pd
from src.services.sheets_service import GoogleSheetsService
from src.config import VENDOR_FIELDS

def main():
    st.title("Vendor Management System")
    
    # Initialize Google Sheets service
    sheets_service = GoogleSheetsService('credentials.json')
    
    # Fetch vendor data
    vendors_df = sheets_service.fetch_vendors()
    
    if vendors_df is not None:
        st.dataframe(vendors_df)
    else:
        st.error("Unable to fetch vendor data. Please check your configuration.")

if __name__ == "__main__":
    main()