from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# TrackDrive API URLs
PING_URL = "https://synegence-llc.trackdrive.com/api/v1/inbound_webhooks/ping/check_for_available_mva_cpl_buyers"
POST_URL = "https://synegence-llc.trackdrive.com/api/v1/inbound_webhooks/post/check_for_available_mva_cpl_buyers"

# Hardcoded static values for all posts
TRACKDRIVE_NUMBER = "+18882574485"
TRAFFIC_SOURCE_ID = "1049"

@app.route('/')
def index():
    return render_template("lead_form.html")

@app.route('/submit-lead', methods=['POST'])
def submit_lead():
    form_data = request.form.to_dict()

    # Add hardcoded static values
    form_data["trackdrive_number"] = TRACKDRIVE_NUMBER
    form_data["traffic_source_id"] = TRAFFIC_SOURCE_ID

    # Validate trusted form cert
    trusted_form_url = form_data.get("trusted_form_cert_url", "").strip()
    if not trusted_form_url:
        return jsonify({
            "success": False,
            "error": "Trusted Form Cert URL is missing. Lead not submitted."
        }), 400

    # Ping request
    ping_params = {
        "trackdrive_number": TRACKDRIVE_NUMBER,
        "traffic_source_id": TRAFFIC_SOURCE_ID,
        "caller_id": form_data.get("caller_id")
    }

    try:
        ping_res = requests.get(PING_URL, params=ping_params, timeout=10)
        ping_json = ping_res.json()
    except Exception as e:
        return jsonify({"success": False, "error": f"Ping request failed: {str(e)}"}), 500

    if not ping_json.get("success") or "ping_id" not in ping_json.get("try_all_buyers", {}):
        return jsonify({
            "success": False,
            "error": "Ping failed or no matching buyer available.",
            "details": ping_json
        }), 400

    # Extract ping_id from response
    ping_id = ping_json["try_all_buyers"]["ping_id"]
    form_data["ping_id"] = ping_id

    # Post lead data
    try:
        post_res = requests.post(POST_URL, data=form_data, timeout=10)
        return jsonify(post_res.json()), post_res.status_code
    except Exception as e:
        return jsonify({"success": False, "error": f"Post request failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
