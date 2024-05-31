from nomad_media_pip.src.exceptions.api_exception_handler import _api_exception_handler

import requests

def _get_live_operators(self, AUTH_TOKEN, URL, DEBUG):
    API_URL = f"{URL}/api/admin/liveOperator"

    HEADERS = {
        "Authorization": "Bearer " +  AUTH_TOKEN,
        "Content-Type": "application/json"
    }

    if (DEBUG):
        print(f"API_URL: {API_URL}\nMETHOD: GET")

    while True:
        try:
            RESPONSE = requests.get(API_URL, headers= HEADERS)

            if RESPONSE.ok:
                break
            
            if RESPONSE.status_code == 403:
                self.refresh_token()
            else:
                raise Exception()
        
        except:
            _api_exception_handler(RESPONSE, "Getting Live Operators failed")
            
    return RESPONSE.json()