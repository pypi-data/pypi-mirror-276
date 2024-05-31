from nomad_media_pip.src.exceptions.api_exception_handler import _api_exception_handler

import json, requests

def _delete_live_input(self, AUTH_TOKEN, URL, INPUT_ID, DEBUG):
    API_URL = f"{URL}/api/liveInput/{INPUT_ID}"

    # Create header for the request
    HEADERS = {
        "Authorization": "Bearer " + AUTH_TOKEN
    }
    
    if (DEBUG):
        print(f"API_URL: {API_URL}\nMETHOD: DELETE")

    while True:
        try:
            # Send the request
            RESPONSE = requests.delete(API_URL, headers= HEADERS)

            if (RESPONSE.ok):
                break

            if RESPONSE.status_code == 403:
                self.refresh_token()
            else:
                raise Exception()

        except:
            _api_exception_handler(RESPONSE, f"Delete Live Input {INPUT_ID} failed")
