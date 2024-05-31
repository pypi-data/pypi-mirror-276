from nomad_media_pip.src.exceptions.api_exception_handler import _api_exception_handler

import requests, json

def _get_live_channel(self, AUTH_TOKEN, URL, CHANNEL_ID, DEBUG):
    API_URL = f"{URL}/api/liveChannel/{CHANNEL_ID}"

    # Create header for the request
    HEADERS = {
        'Content-Type': 'application/json',
        "Authorization": "Bearer " + AUTH_TOKEN
    }

    if (DEBUG):
        print(f"API_URL: {API_URL}\nMETHOD: GET")

    while True:
        try:
            # Send the request
            RESPONSE = requests.get(API_URL, headers= HEADERS)
            
            if RESPONSE.ok:
                break

            if RESPONSE.status_code == 403:
                self.refresh_token()
            else:
                raise Exception()

        except:
            _api_exception_handler(RESPONSE, f"Get Live Channel with ID {CHANNEL_ID} failed")

    return RESPONSE.json()