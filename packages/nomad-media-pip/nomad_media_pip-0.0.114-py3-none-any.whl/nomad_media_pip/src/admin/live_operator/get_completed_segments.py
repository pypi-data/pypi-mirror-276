from nomad_media_pip.src.exceptions.api_exception_handler import _api_exception_handler

import requests

def _get_completed_segments(self, AUTH_TOKEN, URL, ID, DEBUG):
    API_URL = f"{URL}/api/admin/liveOperator/{ID}/segments"

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
            _api_exception_handler(RESPONSE, f"Getting completed segments for Live Channel {ID} failed")
            
    return RESPONSE.json()