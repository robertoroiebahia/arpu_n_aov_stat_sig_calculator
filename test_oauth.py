import os
import streamlit as st
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
import urllib.parse
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import RunReportRequest

# Use the redirect URI from an environment variable or default to localhost:8501
redirect_uri = os.environ.get("REDIRECT_URI", "http://localhost:8501/")

def auth_flow():
    st.write("Welcome to My App!")
    # Check if the URL query parameters include an authorization code.
    auth_code = st.query_params.get("code")
    
    # Load the OAuth client configuration from Streamlit Secrets.
    client_config = st.secrets["GOOGLE_CLIENT_SECRETS"]
    
    # Create the OAuth flow using the loaded client configuration.
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
        # Decode the auth code in case it is URL-encoded.
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
                st.session_state["credentials"] = credentials
                st.session_state["user_info"] = user_info
                # Clear query parameters so the code doesn't re-trigger.
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
                    st.session_state["credentials"] = credentials
                    st.session_state["user_info"] = user_info
                    st.experimental_set_query_params()
                    st.experimental_rerun()
            except Exception as e:
                st.error("Error fetching token: " + str(e))

def run_ga4_report(credentials, property_id):
    # Initialize the GA4 Data API client with the given credentials.
    client = BetaAnalyticsDataClient(credentials=credentials)
    # Create a report request: this example retrieves sessions by country for the last 7 days.
    request = RunReportRequest(
        property=f"properties/{property_id}",
        date_ranges=[{"start_date": "7daysAgo", "end_date": "today"}],
        dimensions=[{"name": "country"}],
        metrics=[{"name": "sessions"}],
    )
    response = client.run_report(request=request)
    return response

def main():
    if "authenticated" not in st.session_state:
        auth_flow()
    else:
        user_info = st.session_state["user_info"]
        email = user_info.get("email", "Unknown")
        st.write(f"Hello, {email}")
        
        # Ask for the GA4 Property ID.
        property_id = st.text_input("Enter your GA4 Property ID (numeric only, e.g., 123456789):")
        if property_id:
            st.write("Fetching GA4 report...")
            try:
                response = run_ga4_report(st.session_state["credentials"], property_id)
                st.subheader("Report Results (Sessions by Country):")
                # Display header row.
                headers = [header.name for header in response.dimension_headers] + \
                          [header.name for header in response.metric_headers]
                st.write(headers)
                # Display each row.
                for row in response.rows:
                    dims = [d.value for d in row.dimension_values]
                    mets = [m.value for m in row.metric_values]
                    st.write(dims + mets)
            except Exception as e:
                st.error("Error fetching GA4 report: " + str(e))

if __name__ == "__main__":
    main()
