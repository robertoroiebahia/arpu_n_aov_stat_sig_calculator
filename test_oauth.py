import streamlit as st
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define the OAuth scopes required
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']

def get_credentials():
    # Create the OAuth flow using your client_secrets.json file
    flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', SCOPES)
    # Run the local server flow. This will open a browser window for authentication.
    creds = flow.run_local_server(port=0)
    return creds

def list_ga4_accounts(creds):
    # Build the GA4 Admin API service object.
    service = build('analyticsadmin', 'v1alpha', credentials=creds)
    # Call the API to list accounts.
    response = service.accounts().list().execute()
    accounts = response.get('accounts', [])
    return accounts

st.title("GA4 Accounts Viewer")

if st.button("Connect to Google Analytics"):
    with st.spinner("Authenticating with Google..."):
        creds = get_credentials()
    with st.spinner("Fetching GA4 accounts..."):
        accounts = list_ga4_accounts(creds)
    
    if not accounts:
        st.error("No GA4 accounts found.")
    else:
        st.success("Connected successfully!")
        st.subheader("Accounts:")
        for account in accounts:
            st.write(f"**Name:** {account.get('displayName')}, **ID:** {account.get('name')}")
