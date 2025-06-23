import os
from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

# --- TrackDrive Configuration ---
TRACKDRIVE_PING_URL = "https://synegence-llc.trackdrive.com/api/v1/inbound_webhooks/ping/check_for_available_mva_cpl_buyers"
TRACKDRIVE_POST_URL = "https://synegence-llc.trackdrive.com/api/v1/inbound_webhooks/post/check_for_available_mva_cpl_buyers"
TRACKDRIVE_NUMBER = "+18882574485"
TRAFFIC_SOURCE_ID = "1049"

# --- HTML Form Page ---
@app.route('/')
def lead_form():
    return render_template('lead_form.html')


# --- Submit Lead (Ping + Post + JSON Response) ---
@app.route('/submit-lead', methods=['POST'])
def submit_lead():
    data = request.form.to_dict()

    # Step 1: Ping TrackDrive
    ping_params = {
        "trackdrive_number": TRACKDRIVE_NUMBER,
        "traffic_source_id": TRAFFIC_SOURCE_ID
    }
    ping_response = requests.get(TRACKDRIVE_PING_URL, params=ping_params).json()

    if not ping_response.get("success") or not ping_response.get("buyers"):
        return jsonify({
            "success": False,
            "message": "No buyers currently available",
            "ping_response": ping_response
        }), 200

    ping_id = ping_response['buyers'][0]['ping_id']

    # Step 2: Post to TrackDrive
    post_payload = {
        "trackdrive_number": TRACKDRIVE_NUMBER,
        "traffic_source_id": TRAFFIC_SOURCE_ID,
        "ping_id": ping_id,
        "first_name": data.get('first_name'),
        "last_name": data.get('last_name'),
        "email": data.get('email'),
        "caller_id": data.get('caller_id'),
        "state": data.get('state'),
        "zip": data.get('zip'),
        "tcpa_opt_in": True,
        "tcpa_optin_consent_language": "I agree to be contacted by the provider."
    }

    post_response = requests.post(TRACKDRIVE_POST_URL, json=post_payload).json()

    return jsonify({
        "success": post_response.get("success"),
        "message": "Lead submitted successfully" if post_response.get("success") else "Failed to submit lead",
        "post_response": post_response
    }), 200


# --- Start Flask ---
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
