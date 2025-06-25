from flask import Flask, render_template, request, jsonify
import requests
import datetime
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('lead_form.html')

@app.route('/submit-lead', methods=['POST'])
def submit_lead():
    form_data = request.form.to_dict()

    # Static required values
    form_data["trackdrive_number"] = "+18882574485"
    form_data["traffic_source_id"] = "1049"
    form_data["ip_address"] = request.remote_addr or "127.0.0.1"
    form_data["original_lead_submit_date"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # TrackDrive POST API endpoint
    post_url = "https://synegence-llc.trackdrive.com/api/v1/inbound_webhooks/post/check_for_available_mva_cpl_buyers"

    try:
        response = requests.post(post_url, json=form_data)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
