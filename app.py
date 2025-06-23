from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

# Constants
TRACKDRIVE_PING_URL = 'https://synegence-llc.trackdrive.com/api/v1/inbound_webhooks/ping/check_for_available_mva_cpl_buyers'
TRACKDRIVE_POST_URL = 'https://synegence-llc.trackdrive.com/api/v1/inbound_webhooks/post/check_for_available_mva_cpl_buyers'

@app.route('/')
def lead_form():
    return render_template('lead_form.html')

@app.route('/submit-lead', methods=['POST'])
def submit_lead():
    data = request.form.to_dict()

    # Hardcoded fields
    data['trackdrive_number'] = '+18882574485'
    data['traffic_source_id'] = '1049'

    # PING request
    ping_params = {
        'trackdrive_number': data['trackdrive_number'],
        'traffic_source_id': data['traffic_source_id'],
        'caller_id': data['caller_id']
    }

    ping_response = requests.get(TRACKDRIVE_PING_URL, params=ping_params)
    ping_result = ping_response.json()

    if not ping_result.get('success'):
        return jsonify({'message': 'Ping failed', 'ping_response': ping_result})

    # POST payload
    post_data = {
        'trackdrive_number': data['trackdrive_number'],
        'traffic_source_id': data['traffic_source_id'],
        'caller_id': data['caller_id'],
        'ping_id': ping_result['try_all_buyers'].get('ping_id'),

        'first_name': data['first_name'],
        'last_name': data['last_name'],
        'email': data['email'],
        'state': data['state'],
        'zip': data['zip'],
        'accident_state': data.get('accident_state'),
        'accident_date': data.get('accident_date'),
        'has_insurance': data.get('has_insurance'),
        'injury_occured': data.get('injury_occured'),
        'currently_represented': data.get('currently_represented'),
        'person_at_fault': data.get('person_at_fault'),
        'hospitalized_or_treated': data.get('hospitalized_or_treated'),
        'auto_accident_in_past_2_years': data.get('auto_accident_in_past_2_years'),
        'trusted_form_cert_url': data.get('trusted_form_cert_url'),
    }

    post_response = requests.post(TRACKDRIVE_POST_URL, json=post_data)
    post_result = post_response.json()

    return jsonify({'message': 'Lead submitted', 'post_response': post_result})


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=10000)
