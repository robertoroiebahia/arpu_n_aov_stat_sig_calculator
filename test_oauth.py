import os
import streamlit as st
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import webbrowser

# Use an environment variable or default redirect URI for Streamlit
redirect_uri = os.environ.get("REDIRECT_URI", "http://localhost:8501/")

def auth_flow():
    st.write("Welcome to My App!")
    # Check if an authorization code exists in the query parameters.
    auth_code = st.query_params.get("code")
    
    # Load the client configuration from Streamlit Secrets.
    # Ensure your secrets.toml contains a [GOOGLE_CLIENT_SECRETS.installed] table.
    client_config = st.secrets["GOOGLE_CLIENT_SECRETS"]
    
    # Create the OAuth flow using the client config.
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        client_config,
        scopes=["https://www.googleapis.com/auth/userinfo.email", "openid"],
        redirect_uri=redirect_uri,
    )
    
    if auth_code:
        # If an authorization code is present, fetch the token.
        flow.fetch_token(code=auth_code)
        credentials = flow.credentials
        st.write("Login Done")
        user_info_service = build(
            serviceName="oauth2",
            version="v2",
            credentials=credentials,
        )
        user_info = user_info_service.userinfo().get().execute()
        assert user_info.get("email"), "Email not found in infos"
        st.session_state["google_auth_code"] = auth_code
        st.session_state["user_info"] = user_info
    else:
        # No auth code yet; prompt the user to sign in.
        if st.button("Sign in with Google"):
            authorization_url, state = flow.authorization_url(
                access_type="offline",
                include_granted_scopes="true",
            )
            # Open the URL in a new browser tab.
            webbrowser.open_new_tab(authorization_url)

def main():
    if "google_auth_code" not in st.session_state:
        auth_flow()

    if "google_auth_code" in st.session_state:
        email = st.session_state["user_info"].get("email")
        st.write(f"Hello {email}")

if __name__ == "__main__":
    main()
