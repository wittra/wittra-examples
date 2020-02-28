from flask import Flask, request, abort
import base64
import json
import pprint
import datetime
app = Flask(__name__)

@app.route('/', defaults={'path': ''}, methods=['POST'])
@app.route('/<path:path>', methods=['POST'])
def log_payload(path):
    # Check valid request media type
    if request.content_type != 'application/json':
        return 'Content type is not JSON', 415

    # Ensure that payload is a dictionary
    payload = request.json
    if not isinstance(payload, dict):
        return 'Payload is not JSON', 500

    # Get message data
    timestamp = datetime.datetime.now()
    message = payload.get('message',{})
    if message:
        # Get device ID
        id = message.get('attributes',{}).get('deviceId','')
        # Get base64 encoded data payload
        data = base64.b64decode(message.get('data',''))
        print('----- Got message from {} ({}) -------'.format(id, timestamp))
        pprint.pprint(json.loads(data))
    else:
        print('----- Got message that could not be parsed ({}) -----'.format(timestamp))
        print(payload)
    return 'OK', 200

if __name__ == '__main__':
    app.run()
