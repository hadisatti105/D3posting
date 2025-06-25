
from flask import Flask, request, jsonify, render_template
import requests
import datetime

app = Flask(__name__)

@app.route('/')
def lead_form():
    return render_template('lead_form.html')

@app.route('/submit-lead', methods=['POST'])
def submit_lead():
    data = request.form.to_dict()

    # Add static and required fields
    data['original_lead_submit_date'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data['ip_address'] = request.remote_addr
    data['source_url'] = request.referrer or "https://yourlandingpage.com"
    data['tcpa_opt_in'] = 'true'
    data['tcpa_optin_consent_language'] = "I consent to be contacted."
    data['payment_method_available'] = 'true'
    data['monthly_affordable_payment_amount'] = '100'
    data['media_type'] = 'Google Ads'
    data['traffic_source_platform'] = 'Invoca'
    data['lead_type'] = 'Exclusive'

    # Assume ping_id was stored before
    data['ping_id'] = 'REPLACE_WITH_ACTUAL_PING_ID'  # This must be captured from an earlier ping

    post_url = "https://synegence-llc.trackdrive.com/api/v1/inbound_webhooks/post/check_for_available_mva_cpl_buyers"

    try:
        response = requests.post(post_url, json=data)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
