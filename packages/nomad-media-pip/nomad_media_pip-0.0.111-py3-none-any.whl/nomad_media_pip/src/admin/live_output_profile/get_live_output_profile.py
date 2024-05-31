from nomad_media_pip.src.exceptions.api_exception_handler import _api_exception_handler

import requests

def _get_live_output_profile(self, AUTH_TOKEN, URL, ID, DEBUG):

    API_URL = f"{URL}/api/liveOutputProfile/{ID}"

    HEADERS = {
        "Authorization": "Bearer " + AUTH_TOKEN,
        "Content-Type": "application/json"
    }

    if DEBUG:
        print(f"URL: {API_URL},\nMETHOD: GET")

    while True:
        try:
            RESPONSE = requests.get(API_URL, headers=HEADERS)
            
            if RESPONSE.ok:
                break
            
            if RESPONSE.status_code == 403:
                self.refresh_token()
            else:
                raise Exception()
        
        except:
            _api_exception_handler(RESPONSE, "Get Live Output Profile Failed")


    return RESPONSE.json()