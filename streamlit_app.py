import streamlit as st
import requests

# Streamlit app title
st.title("IMEI Checker")

# Input field for IMEI number
imei_number = st.text_input("Enter IMEI Number:")

# Button to trigger the API call
if st.button("Check IMEI"):
    # Base URL
    base_url = "https://api-citizens-prod-imei.gs-ef.com/"

    # Endpoint for checking IMEI
    endpoint = "ceirimeicheck/api/v1/imei/check"

    # Full URL
    url = base_url + endpoint

    # Request payload
    payload = {
        "imeiNumber": [imei_number]  # Use the IMEI number from the input field
    }

    try:
        # Send a POST request with SSL verification disabled
        response = requests.post(url, json=payload, verify=False)

        # Check if the request was successful
        if response.status_code == 200:
            result = response.json()

            # Extract details from the response
            model = result["result"]["model"]
            status = result["result"]["status"]
            active = result["result"]["active"]
            manufacturer = result["result"]["manufacturerName"]
            trials_left = result["result"]["numberOfTrialsLeft"]
            imei_number = result["result"]["deviceImeiNumber"]
            amount = result["result"]["amount"]

            # Display the response in a user-friendly way
            st.subheader("IMEI Check Result")
            st.write(f"**Model:** {model}")
            st.write(f"**Status:** {status}")
            st.write(f"**Active Status:** {active}")
            st.write(f"**Manufacturer:** {manufacturer}")
            st.write(f"**Trials Left:** {trials_left}")
            st.write(f"**IMEI Number:** {imei_number}")
            st.write(f"**Amount:** {amount} USD")

        else:
            st.error(f"Error: Unable to check IMEI. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
