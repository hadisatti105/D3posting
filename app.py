from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

PING_URL = "https://synegence-llc.trackdrive.com/api/v1/inbound_webhooks/ping/check_for_available_mva_cpl_buyers"
POST_URL = "https://synegence-llc.trackdrive.com/api/v1/inbound_webhooks/post/check_for_available_mva_cpl_buyers"

@app.route("/", methods=["GET"])
def lead_form():
    return render_template("lead_form.html")

@app.route("/submit-lead", methods=["POST"])
def submit_lead():
    form = request.form.to_dict()

    # Step 1: Perform PING
    ping_payload = {
        "trackdrive_number": "+18882574485",
        "traffic_source_id": "1049",
        "caller_id": form.get("phone_number"),
        "trusted_form_cert_url": form.get("trusted_form_url")
    }

    ping_response = requests.post(PING_URL, json=ping_payload)
    ping_json = ping_response.json()

    if not ping_json.get("success"):
        return jsonify({
            "success": False,
            "error": "Ping failed",
            "ping_response": ping_json
        })

    # Extract ping_id from successful response
    ping_id = ping_json.get("try_all_buyers", {}).get("ping_id")

    # Step 2: POST with all required fields
    post_payload = {
        "trackdrive_number": "+18882574485",
        "traffic_source_id": "1049",
        "ping_id": ping_id,
        "first_name": form.get("first_name"),
        "last_name": form.get("last_name"),
        "caller_id": form.get("phone_number"),
        "email": form.get("email_address"),
        "city": form.get("city"),
        "state": form.get("state"),
        "zip": form.get("zip_code"),
        "ip_address": request.remote_addr,
        "trusted_form_cert_url": form.get("trusted_form_url"),
        "accident_type": form.get("accident_type"),
        "auto_accident_in_past_2_years": form.get("auto_accident_in_past_2_years")
    }

    post_response = requests.post(POST_URL, json=post_payload)
    return jsonify(post_response.json())

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=10000)
