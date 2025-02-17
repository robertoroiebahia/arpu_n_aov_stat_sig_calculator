import streamlit as st
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Define the OAuth scopes required.
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']

def get_credentials():
    # Load the client secrets configuration from Streamlit secrets.
    client_config = st.secrets["GOOGLE_CLIENT_SECRETS"]
    flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
    
    # Generate the authorization URL.
    auth_url, _ = flow.authorization_url(prompt='consent')
    
    # Display the URL so the user can visit it.
    st.write("Please visit the following URL to authorize the app:")
    st.write(auth_url)
    
    # Get the authorization code from the user.
    code = st.text_input("Enter the authorization code here:")
    
    if code:
        # Fetch the token using the provided code.
        flow.fetch_token(code=code)
        return flow.credentials
    else:
        return None

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
    else:
        st.warning("Please enter the authorization code to proceed.")
