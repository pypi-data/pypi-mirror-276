from nomad_media_pip.src.exceptions.api_exception_handler import _api_exception_handler

import requests

def _stop_schedule(self, AUTH_TOKEN, URL, ID, FORCE_STOP, DEBUG):
    if FORCE_STOP == None:
        FORCE_STOP = False

    API_URL = f"{URL}/api/admin/schedule/{ID}/stop?force={FORCE_STOP}"

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
            _api_exception_handler(RESPONSE, "Stop Schedule Failed")


    return RESPONSE.json()