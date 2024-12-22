"""UI components for the Streamlit application."""
import streamlit as st
import pandas as pd

def display_header():
    """Display the application header and description."""
    st.title("Vendor Management Portal")
    st.markdown("Enter the details of the new vendor below.")

def display_vendor_data(vendor_data: pd.DataFrame):
    """Display vendor data in a dataframe."""
    st.dataframe(vendor_data)