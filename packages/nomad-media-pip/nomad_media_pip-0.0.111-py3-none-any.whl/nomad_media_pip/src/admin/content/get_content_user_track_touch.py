from nomad_media_pip.src.exceptions.api_exception_handler import _api_exception_handler

import requests

def _get_content_user_track_touch(self, AUTH_TOKEN, URL, CONTNET_ID, CONTENT_DEFINITION_ID, 
                                  DEBUG):
    API_URL = f"{URL}/api/content/{CONTENT_DEFINITION_ID}/user-track/{CONTNET_ID}/touch"

    # Create header for the request
    HEADERS = {
        "Authorization": "Bearer " + AUTH_TOKEN,
        "Content-Type": "application/json"
    }

    if DEBUG:
        print(f"URL: {API_URL},\nMETHOD: GET")

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
            _api_exception_handler(RESPONSE, "Get content user track touch failed")
            
    return RESPONSE.json()