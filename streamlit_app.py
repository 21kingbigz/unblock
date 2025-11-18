import streamlit as st
import requests
from bs4 import BeautifulSoup
import time

# --- Streamlit App Configuration ---
st.set_page_config(
    page_title="Streamlit Content Relay",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🌐 Simple Content Relay for Unblocking Sites")
st.markdown("Enter a URL below. The Streamlit server will fetch the page content and display it here, bypassing local content filters.")

# --- User Input ---
target_url = st.text_input(
    "Enter Target URL (e.g., https://example.com)",
    value=""
)

# --- Button to Trigger Fetch ---
if st.button("Fetch Content"):
    if not target_url:
        st.warning("Please enter a URL to fetch.")
    else:
        # Simple validation to ensure it looks like a proper URL
        if not target_url.startswith(('http://', 'https://')):
            target_url = 'https://' + target_url

        try:
            with st.spinner(f'Fetching content from **{target_url}**...'):
                # The crucial step: Streamlit's server makes the request
                response = requests.get(target_url, timeout=15, allow_redirects=True)
                
            # Check for successful response
            if response.status_code == 200:
                st.success(f"Successfully fetched content (Status: {response.status_code})")
                
                # Use BeautifulSoup to parse and format the HTML content for display
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Display the page title
                page_title = soup.title.string if soup.title else "No Title Found"
                st.header(f"Page Title: {page_title}")

                # Display the content as code (to show the raw result)
                with st.expander("View Raw HTML Content", expanded=False):
                    st.code(response.text, language='html')

                # Display the text of the page (cleaned up)
                st.subheader("Extracted Page Text (Partial)")
                # Get only the visible text content of the page
                st.write(soup.get_text(separator=' ', strip=True)[:4000] + "...") # Show first 4000 characters

            else:
                st.error(f"Failed to fetch URL. Status Code: {response.status_code}")
                st.info("The target server may have blocked the request, or the URL is invalid.")

        except requests.exceptions.Timeout:
            st.error("Request timed out after 15 seconds.")
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred: {e}")

# --- Deployment Note ---
st.sidebar.info(
    "**Note:** For this to unblock content, the app must be **deployed** "
    "to an external service like **Google App Engine** or **Streamlit Cloud**, "
    "so the web request originates from the cloud server, not your local network."
)
