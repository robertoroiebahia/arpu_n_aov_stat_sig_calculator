import streamlit as st
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define the OAuth scopes required.
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']

def get_credentials():
    # Load the client secrets configuration from Streamlit secrets (TOML format).
    client_config = st.secrets["GOOGLE_CLIENT_SECRETS"]
    
    # The client_config contains an "installed" key as per our TOML file.
    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    creds = flow.run_console()
    return creds

def list_ga4_accounts(creds):
    # Build the GA4 Admin API service object.
    service = build('analyticsadmin', 'v1alpha', credentials=creds)
    response = service.accounts().list().execute()
    return response.get('accounts', [])

st.title("GA4 Accounts Viewer")

if st.button("Connect to Google Analytics"):
    with st.spinner("Authenticating with Google..."):
        creds = get_credentials()
    if creds:
        with st.spinner("Fetching GA4 accounts..."):
            accounts = list_ga4_accounts(creds)
        if not accounts:
            st.error("No GA4 accounts found.")
        else:
            st.success("Connected successfully!")
            st.subheader("Accounts:")
            for account in accounts:
                st.write(f"**Name:** {account.get('displayName')}, **ID:** {account.get('name')}")
