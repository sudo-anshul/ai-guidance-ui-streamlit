import streamlit as st
import requests

# Load the API URL from Streamlit secrets
API_URL = st.secrets["API_URL"]

# Streamlit App
st.title("AI Financial Guidance")
st.write("Get insights and guidance from AI-powered financial advisors.")

# Input form for user query
st.header("Enter Your Financial Query")
user_query = st.text_area("Type your query here (e.g., 'What are the risks of investing in AAPL?'):")

# Submit button
if st.button("Get Guidance"):
    if not user_query.strip():
        st.error("Please enter a valid query.")
    else:
        # Send the query to the Flask API
        with st.spinner("Processing your query..."):
            try:
                response = requests.post(
                    f"{API_URL}/consult",
                    json={"query": user_query},
                    timeout=500,  # Timeout for the API request
                    verify=False  # Disable SSL verification for testing purposes
                )
                if response.status_code == 200:
                    # Parse and display the response
                    data = response.json()
                    st.success("AI Guidance Received:")
                    st.write(data.get("response", "No response received."))
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to the API: {e}")

# Health check
st.sidebar.header("API Health Check")
if st.sidebar.button("Check API Status"):
    try:
        health_response = requests.get(f"{API_URL}/health")
        if health_response.status_code == 200:
            st.sidebar.success("API is running!")
        else:
            st.sidebar.error(f"API Error: {health_response.status_code}")
    except requests.exceptions.RequestException as e:
        st.sidebar.error(f"Failed to connect to the API: {e}")
