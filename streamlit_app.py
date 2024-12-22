import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import pandas as pd
from datetime import datetime

# Authenticate and connect to Google Sheets
def connect_to_gsheet(creds_json, spreadsheet_name, sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    
    credentials = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scope)
    client = gspread.authorize(credentials)
    spreadsheet = client.open(spreadsheet_name)
    return spreadsheet.worksheet(sheet_name)

# Google Sheet credentials file
SPREADSHEET_NAME = 'Streamlit'
SHEET_NAME = 'Vendors'
CREDENTIALS_FILE = './credentials.json'

# Constants
BUSINESS_TYPES = ["Manufacturer", "Distributor", "Wholesaler", "Retailer", "Service Provider"]
PRODUCTS = ["Electronics", "Apparel", "Groceries", "Software", "Other"]

# Form schema definition
form_schema = {
    "company_name": {
        "type": "text",
        "label": "Company Name",
        "required": True,
        "validation": {
            "min_length": 2,
            "max_length": 100,
            "message": "Company name must be between 2 and 100 characters."
        }
    },
    "business_type": {
        "type": "select",
        "label": "Business Type",
        "required": True,
        "options": BUSINESS_TYPES,
        "validation": {
            "message": "Please select a business type."
        }
    },
    "products": {
        "type": "multiselect",
        "label": "Products Offered",
        "required": True,
        "options": PRODUCTS,
        "validation": {
            "min_selections": 1,
            "message": "Please select at least one product."
        }
    },
    "years_in_business": {
        "type": "slider",
        "label": "Years in Business",
        "required": True,
        "min": 0,
        "max": 50,
        "default": 5,
        "validation": {
            "message": "Years in business must be between 0 and 50."
        }
    },
    "onboarding_date": {
        "type": "date",
        "label": "Onboarding Date",
        "required": True,
        "validation": {
            "message": "Please select a valid onboarding date."
        }
    },
    "additional_info": {
        "type": "textarea",
        "label": "Additional Notes",
        "required": False,
        "validation": {
            "max_length": 500,
            "message": "Additional notes cannot exceed 500 characters."
        }
    }
}

# Connect to the Google Sheet
sheet = connect_to_gsheet(CREDENTIALS_FILE, SPREADSHEET_NAME, SHEET_NAME)

def read_data():
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    # Convert all int64 columns to int
    for col in df.select_dtypes(['int64']).columns:
        df[col] = df[col].astype('int')
    return df

def add_data(row):
    sheet.append_row(row)

def update_data(index, row):
    sheet.delete_rows(index + 2)  # +2 because sheet is 1-indexed and has header
    sheet.insert_row(row, index + 2)

def delete_data(index):
    sheet.delete_rows(index + 2)

def render_form(schema, existing_data=None):
    form_data = {}
    
    for field, properties in schema.items():
        field_type = properties["type"]
        label = properties["label"]
        value = existing_data.get(field) if existing_data else None
        
        if field_type == "text":
            form_data[field] = st.text_input(label, value=value or "")
        elif field_type == "select":
            options = properties["options"]
            default_idx = options.index(value) if value in options else 0
            form_data[field] = st.selectbox(label, options, index=default_idx)
        elif field_type == "multiselect":
            options = properties["options"]
            default = value.split(", ") if value else []
            form_data[field] = st.multiselect(label, options, default=default)
        elif field_type == "slider":
            form_data[field] = st.slider(label, 
                                       properties["min"], 
                                       properties["max"], 
                                       value=value or properties["default"])
        elif field_type == "date":
            default_date = datetime.strptime(value, "%Y-%m-%d").date() if value else datetime.today()
            form_data[field] = st.date_input(label, value=default_date)
        elif field_type == "textarea":
            form_data[field] = st.text_area(label, value=value or "")
    
    return form_data

def validate_form(form_data, schema):
    errors = []
    for field, value in form_data.items():
        properties = schema[field]
        if properties.get("required"):
            if not value:
                errors.append(f"{properties['label']} is required.")
            elif properties["type"] == "multiselect" and len(value) < properties["validation"]["min_selections"]:
                errors.append(properties["validation"]["message"])
        
        if value:
            if properties["type"] in ["text", "textarea"]:
                if len(value) < properties["validation"].get("min_length", 0) or \
                   len(value) > properties["validation"].get("max_length", float('inf')):
                    errors.append(properties["validation"]["message"])
    
    return errors

st.title("Vendor Management Portal")

action = st.selectbox(
    "Choose an Action",
    ["Onboard New Vendor", "Update Existing Vendor", "View All Vendors", "Delete Vendor"]
)

if action == "Onboard New Vendor":
    st.markdown("Enter the details of the new vendor below.")
    
    with st.form(key="vendor_form"):
        form_data = render_form(form_schema)
        submitted = st.form_submit_button("Submit Vendor Details")
        
        if submitted:
            errors = validate_form(form_data, form_schema)
            if errors:
                for error in errors:
                    st.error(error)
            else:
                row = [
                    form_data["company_name"],
                    form_data["business_type"],
                    ", ".join(form_data["products"]),
                    form_data["years_in_business"],
                    form_data["onboarding_date"].strftime("%Y-%m-%d"),
                    form_data["additional_info"]
                ]
                add_data(row)
                st.success("Vendor details successfully submitted!")

elif action == "Update Existing Vendor":
    df = read_data()
    vendor_to_update = st.selectbox("Select a Vendor to Update", 
                                  options=df["Company Name"].tolist())
    
    if vendor_to_update:
        vendor_idx = df[df["Company Name"] == vendor_to_update].index[0]
        vendor_data = df.iloc[vendor_idx].to_dict()
        
        with st.form(key="update_form"):
            form_data = render_form(form_schema, vendor_data)
            submitted = st.form_submit_button("Update Vendor Details")
            
            if submitted:
                errors = validate_form(form_data, form_schema)
                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    row = [
                        form_data["company_name"],
                        form_data["business_type"],
                        ", ".join(form_data["products"]),
                        form_data["years_in_business"],
                        form_data["onboarding_date"].strftime("%Y-%m-%d"),
                        form_data["additional_info"]
                    ]
                    update_data(vendor_idx, row)
                    st.success("Vendor details successfully updated!")

elif action == "View All Vendors":
    df = read_data()
    st.dataframe(df)

elif action == "Delete Vendor":
    df = read_data()
    vendor_to_delete = st.selectbox("Select a Vendor to Delete", 
                                  options=df["Company Name"].tolist())
    
    if vendor_to_delete and st.button("Delete"):
        vendor_idx = df[df["Company Name"] == vendor_to_delete].index[0]
        delete_data(vendor_idx)
        st.success(f"Vendor '{vendor_to_delete}' successfully deleted!")
