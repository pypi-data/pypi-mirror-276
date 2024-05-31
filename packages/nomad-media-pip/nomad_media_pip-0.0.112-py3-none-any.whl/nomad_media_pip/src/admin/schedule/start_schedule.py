from nomad_media_pip.src.exceptions.api_exception_handler import _api_exception_handler

import requests

def _start_schedule(self, AUTH_TOKEN, URL, ID, SKIP_CLEANUP_ON_FAILURE, DEBUG):

    if SKIP_CLEANUP_ON_FAILURE == None:
        SKIP_CLEANUP_ON_FAILURE = False

    API_URL = f"{URL}/api/admin/schedule/{ID}/start?skipCleanupOnFailure={SKIP_CLEANUP_ON_FAILURE}"

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
            _api_exception_handler(RESPONSE, "Start Schedule Failed")


    return RESPONSE.json()