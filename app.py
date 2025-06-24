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
    # Extract form data
    data = request.form.to_dict()
    
    # Required ping fields
    ping_payload = {
        "trackdrive_number": data.get("trackdrive_number"),
        "traffic_source_id": data.get("traffic_source_id"),
        "caller_id": data.get("caller_id"),
        "trusted_form_cert_url": data.get("trusted_form_cert_url"),
    }

    # Ping to check buyer availability
    ping_response = requests.post(PING_URL, json=ping_payload)
    ping_data = ping_response.json()

    if not ping_data.get("success"):
        return jsonify({
            "message": "No buyers currently available",
            "ping_response": ping_data,
            "success": False
        })

    # Extract ping_id from response
    ping_id = ping_data["try_all_buyers"]["ping_id"]

    # Post fields – extend with more if needed
    post_payload = {
        **data,  # includes all fields from the form
        "ping_id": ping_id
    }

    # Send the post
    post_response = requests.post(POST_URL, json=post_payload)
    return jsonify(post_response.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
