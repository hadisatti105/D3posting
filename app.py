import os
from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# TrackDrive Config
TRACKDRIVE_PING_URL = "https://synegence-llc.trackdrive.com/api/v1/inbound_webhooks/ping/check_for_available_mva_cpl_buyers"
TRACKDRIVE_POST_URL = "https://synegence-llc.trackdrive.com/api/v1/inbound_webhooks/post/check_for_available_mva_cpl_buyers"
TRACKDRIVE_NUMBER = "+18882574485"
TRAFFIC_SOURCE_ID = "1049"

@app.route('/')
def lead_form():
    return render_template('lead_form.html')

@app.route('/submit-lead', methods=['POST'])
def submit_lead():
    data = request.form.to_dict()
    ping_params = {
        "trackdrive_number": TRACKDRIVE_NUMBER,
        "traffic_source_id": TRAFFIC_SOURCE_ID
    }

    ping_response = requests.get(TRACKDRIVE_PING_URL, params=ping_params).json()
    if not ping_response.get("success") or not ping_response.get("buyers"):
        return "No buyers currently available. Please try again later."

    ping_id = ping_response['buyers'][0]['ping_id']

    post_payload = {
        "trackdrive_number": TRACKDRIVE_NUMBER,
        "traffic_source_id": TRAFFIC_SOURCE_ID,
        "ping_id": ping_id,
        "first_name": data['first_name'],
        "last_name": data['last_name'],
        "email": data['email'],
        "caller_id": data['caller_id'],
        "state": data['state'],
        "zip": data['zip'],
        "tcpa_opt_in": True,
        "tcpa_optin_consent_language": "I agree to be contacted by the provider."
    }

    post_response = requests.post(TRACKDRIVE_POST_URL, json=post_payload).json()

    if post_response.get("success"):
        return f"Lead submitted successfully! Buyer will call you at: {post_response.get('forwarding_number')}"
    else:
        return f"Error: {post_response.get('errors')}"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
