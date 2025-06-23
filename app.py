from flask import Flask, request, render_template, jsonify
import requests
import os

app = Flask(__name__)

# Production endpoints
PING_URL = "https://synegence-llc.trackdrive.com/api/v1/inbound_webhooks/ping/check_for_available_mva_cpl_buyers"
POST_URL = "https://synegence-llc.trackdrive.com/api/v1/inbound_webhooks/post/check_for_available_mva_cpl_buyers"

@app.route('/')
def lead_form():
    return render_template('lead_form.html')

@app.route('/submit-lead', methods=['POST'])
def submit_lead():
    # Step 1: Prepare Ping data
    ping_data = {
        "trackdrive_number": request.form.get("trackdrive_number"),
        "traffic_source_id": request.form.get("traffic_source_id"),
        "caller_id": request.form.get("caller_id")
    }

    ping_response = requests.post(PING_URL, json=ping_data).json()

    if not ping_response.get("success") or not ping_response.get("buyers"):
        return jsonify({
            "success": False,
            "message": "No buyers currently available",
            "ping_response": ping_response
        })

    # Step 2: Post data with ping_id and full lead info
    post_data = {
        **ping_data,
        "ping_id": ping_response["buyers"][0]["ping_id"],

        # Lead Details
        "first_name": request.form.get("first_name"),
        "last_name": request.form.get("last_name"),
        "email": request.form.get("email"),
        "state": request.form.get("state"),
        "zip": request.form.get("zip"),

        # Compliance & Matching Fields
        "tcpa_opt_in": True,
        "tcpa_optin_consent_language": request.form.get("tcpa_optin_consent_language"),
        "accident_state": request.form.get("accident_state"),
        "accident_date": request.form.get("accident_date"),
        "has_insurance": request.form.get("has_insurance"),
        "injury_occured": request.form.get("injury_occured"),
        "hospitalized_or_treated": request.form.get("hospitalized_or_treated"),
        "person_at_fault": request.form.get("person_at_fault"),
        "currently_represented": request.form.get("currently_represented"),
        "trusted_form_cert_url": request.form.get("trusted_form_cert_url")
    }

    post_response = requests.post(POST_URL, json=post_data).json()

    return jsonify({
        "success": post_response.get("success", False),
        "post_response": post_response
    })

if __name__ == '__main__':
    # Flask production config (debug=False)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
