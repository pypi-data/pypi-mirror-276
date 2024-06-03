import requests
import json

class SocketBee:
    def __init__(self, app_id, secret, key, config=None):
        if config is None:
            config = {}
        self.config = {
            'protocol': 'https',
            'host': 'east-1.socket.socketbee.com',
            'port': 443,
        }
        self.config.update(config)
        self.app_id = app_id
        self.headers = {
            'Content-Type': 'application/json',
            'secret': secret,
            'key': key,
        }

    def get_url(self):
        return f"{self.config['protocol']}://{self.config['host']}:{self.config['port']}/send-event/{self.app_id}"

    def send_event(self, channel, event, data):
        body = json.dumps({
            'channel': channel,
            'event': {
                'event': event,
                'data': data,
            },
        })

        try:
            response = requests.post(self.get_url(), headers=self.headers, data=body)
            return {
                'status': response.status_code,
                'body': response.text,
            }
        except requests.exceptions.RequestException as e:
            if e.response is not None:
                return {
                    'status': e.response.status_code,
                    'errors': e.response.text,
                }
            else:
                return {
                    'status': 0,
                    'error_message': str(e),
                }
