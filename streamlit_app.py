import streamlit as st
import requests

# Function to fetch user IP address from an external service
def get_user_ip():
    try:
        # This will get the public IP of the user
        response = requests.get("https://api.ipify.org?format=json")
        return response.json()["ip"]
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching user IP: {e}")
        return None

# Streamlit app title
st.title("IMEI Checker")

# Input field for IMEI number
imei_number = st.text_input("Enter IMEI Number:")

# Button to trigger the API call
if st.button("Check IMEI"):
    user_ip = get_user_ip()

    if user_ip:
        # Base URL
        base_url = "https://api-citizens-prod-imei.gs-ef.com/"
        endpoint = "ceirimeicheck/api/v1/imei/check"
        url = base_url + endpoint

        # Request payload with IMEI and user IP
        payload = {
            "imeiNumber": [imei_number],  # IMEI number from the input field
            "userIp": user_ip  # Add user IP to the payload
        }

        try:
            # Make the API request with the user IP
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                result = response.json()
                
                # Extract data from the response
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
    else:
        st.error("Unable to fetch user IP address.")
