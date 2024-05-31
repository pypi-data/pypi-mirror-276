from nomad_media_pip.src.exceptions.api_exception_handler import _api_exception_handler

import requests

def _next_event(self, AUTH_TOKEN, URL, CHANNEL_ID, DEBUG):
    
    API_URL = f"{URL}/api/liveChannel/{CHANNEL_ID}/nextEvent"
    
    HEADERS = {
        "Authorization": "Bearer " + AUTH_TOKEN,
        "Content-Type": "application/json"
    }
    
    if DEBUG:
        print(f"URL: {API_URL},\nMETHOD: POST")
    
    while True:
        try:
            RESPONSE = requests.post(API_URL, headers= HEADERS)
            
            if RESPONSE.ok:
                break

            if RESPONSE.status_code == 403:
                self.refresh_token()
            else:
                raise Exception()
        except:
            _api_exception_handler(RESPONSE, "Get Next Event Failed")