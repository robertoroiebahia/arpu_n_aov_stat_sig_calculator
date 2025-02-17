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
    
    if auth_code:
        # Decode the auth code if it's URL-encoded.
        decoded_code = urllib.parse.unquote(auth_code)
        try:
            flow.fetch_token(code=decoded_code)
            credentials = flow.credentials
            st.write("Login Done")
            user_info_service = build("oauth2", "v2", credentials=credentials)
            user_info = user_info_service.userinfo().get().execute()
            assert user_info.get("email"), "Email not found in infos"
            st.session_state["google_auth_code"] = decoded_code
            st.session_state["user_info"] = user_info
        except Exception as e:
            st.error("Error fetching token: " + str(e))
    else:
        if st.button("Sign in with Google"):
            authorization_url, state = flow.authorization_url(
                access_type="offline",
                include_granted_scopes="true",
            )
            st.markdown(
                f"**[Click here to sign in with Google]({authorization_url})**",
                unsafe_allow_html=True,
            )
            st.write("After signing in, copy the 'code' parameter from the URL and paste it below:")
            code_input = st.text_input("Enter the authorization code:")
            if code_input:
                decoded_code = urllib.parse.unquote(code_input)
                try:
                    flow.fetch_token(code=decoded_code)
                    credentials = flow.credentials
                    st.write("Login Done")
                    user_info_service = build("oauth2", "v2", credentials=credentials)
                    user_info = user_info_service.userinfo().get().execute()
                    assert user_info.get("email"), "Email not found in infos"
                    st.session_state["google_auth_code"] = decoded_code
                    st.session_state["user_info"] = user_info
                except Exception as e:
                    st.error("Error fetching token: " + str(e))

def main():
    if "google_auth_code" not in st.session_state:
        auth_flow()
    
    if "google_auth_code" in st.session_state:
        email = st.session_state["user_info"].get("email")
        st.write(f"Hello {email}")

if __name__ == "__main__":
    main()
