import os
import streamlit as st
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import urllib.parse

# Use the redirect URI from an environment variable or default to localhost:8501
redirect_uri = os.environ.get("REDIRECT_URI", "http://localhost:8501/")

def auth_flow():
    st.write("Welcome to My App!")
    auth_code = st.query_params.get("code")
    
    # Load client configuration from Streamlit Secrets (TOML format)
    client_config = st.secrets["GOOGLE_CLIENT_SECRETS"]
    
    # Create the OAuth flow using the client configuration.
    # Updated scopes to include Google Analytics read access.
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        client_config,
        scopes=[
            "https://www.googleapis.com/auth/userinfo.email",
            "openid",
            "https://www.googleapis.com/auth/analytics.readonly"
        ],
        redirect_uri=redirect_uri,
    )
    
    if auth_code:
        decoded_code = urllib.parse.unquote(auth_code)
        try:
            flow.fetch_token(code=decoded_code)
            credentials = flow.credentials
            user_info_service = build("oauth2", "v2", credentials=credentials)
            user_info = user_info_service.userinfo().get().execute()
            if not user_info.get("email"):
                st.error("Email not found in user info.")
            else:
                st.session_state["google_auth_code"] = decoded_code
                st.session_state["user_info"] = user_info
                st.session_state["credentials"] = credentials  # Store credentials for API calls
                st.experimental_set_query_params()  # Clear query parameters so we don't re-process the code.
                st.experimental_rerun()  # Refresh the app to show authenticated state.
        except Exception as e:
            st.error("Error fetching token: " + str(e))
    else:
        st.write("Please sign in with Google:")
        if st.button("Sign in with Google"):
            authorization_url, state = flow.authorization_url(
                access_type="offline",
                include_granted_scopes="true",
            )
            st.markdown(
                f"**[Click here to sign in with Google]({authorization_url})**",
                unsafe_allow_html=True,
            )
        st.write("Or paste your authorization code below:")
        code_input = st.text_input("Enter the authorization code:")
        if code_input:
            decoded_code = urllib.parse.unquote(code_input)
            try:
                flow.fetch_token(code=decoded_code)
                credentials = flow.credentials
                user_info_service = build("oauth2", "v2", credentials=credentials)
                user_info = user_info_service.userinfo().get().execute()
                if not user_info.get("email"):
                    st.error("Email not found in user info.")
                else:
                    st.session_state["google_auth_code"] = decoded_code
                    st.session_state["user_info"] = user_info
                    st.session_state["credentials"] = credentials
                    st.experimental_set_query_params()
                    st.experimental_rerun()
            except Exception as e:
                st.error("Error fetching token: " + str(e))

def list_ga4_accounts(credentials):
    # Build the GA4 Admin API service object.
    service = build("analyticsadmin", "v1alpha", credentials=credentials)
    response = service.accounts().list().execute()
    accounts = response.get("accounts", [])
    return accounts

def main():
    if "google_auth_code" not in st.session_state:
        auth_flow()
    
    if "google_auth_code" in st.session_state:
        user_info = st.session_state["user_info"]
        email = user_info.get("email", "Unknown")
        st.write(f"Hello, {email}!")
        
        if "credentials" in st.session_state:
            credentials = st.session_state["credentials"]
            accounts = list_ga4_accounts(credentials)
            if accounts:
                st.subheader("GA4 Accounts:")
                for account in accounts:
                    st.write(f"**Name:** {account.get('displayName')}, **ID:** {account.get('name')}")
            else:
                st.write("No GA4 accounts found.")
        else:
            st.error("Credentials not available.")

if __name__ == "__main__":
    main()
