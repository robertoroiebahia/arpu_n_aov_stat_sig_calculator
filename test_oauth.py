import os
import streamlit as st
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import urllib.parse

# Use the redirect URI from an environment variable or default to localhost:8501
redirect_uri = os.environ.get("REDIRECT_URI", "http://localhost:8501/")

def auth_flow():
    st.write("Welcome to My App!")
    # Get the authorization code from query parameters (if present)
    auth_code = st.query_params.get("code")
    
    # Load client configuration from Streamlit Secrets (TOML format)
    client_config = st.secrets["GOOGLE_CLIENT_SECRETS"]
    
    # Create the OAuth flow using the client configuration.
    flow = google_auth_oauthlib.flow.Flow.from_client_config(
        client_config,
        scopes=["https://www.googleapis.com/auth/userinfo.email", "openid"],
        redirect_uri=redirect_uri,
    )
    
    # If the authorization code is present in the URL
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
                st.session_state["authenticated"] = True
                st.session_state["user_info"] = user_info
                # Clear the query parameters so the code doesn't re-trigger authentication.
                st.experimental_set_query_params()
                st.experimental_rerun()
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
        # Provide a text input to allow manual entry of the auth code
        code_input = st.text_input("Or paste your authorization code here:")
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
                    st.session_state["authenticated"] = True
                    st.session_state["user_info"] = user_info
                    # Clear query params and refresh the app.
                    st.experimental_set_query_params()
                    st.experimental_rerun()
            except Exception as e:
                st.error("Error fetching token: " + str(e))

def main():
    if "authenticated" not in st.session_state:
        auth_flow()
    else:
        user_info = st.session_state["user_info"]
        email = user_info.get("email", "Unknown")
        st.write(f"Hello, {email}")

if __name__ == "__main__":
    main()
