from nomad_media_pip.src.exceptions.api_exception_handler import _api_exception_handler

import requests, json

def _logout(self, AUTH_TOKEN, URL, USER_SESSION_ID, DEBUG):
    API_URL = f"{URL}/api/account/logout"

    HEADERS = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + AUTH_TOKEN
    }

    BODY = {
        "userSessionId": USER_SESSION_ID,   
    }

    if DEBUG:
        print(f"API URL: {API_URL}\nMETHOD: POST\nBODY: {json.dumps(BODY, indent=4)}")

    while True:
        try:
            # Send the request
            RESPONSE = requests.post(API_URL, headers= HEADERS, data = json.dumps(BODY))

            if RESPONSE.ok:
                break
            
            if RESPONSE.status_code == 403:
                self.refresh_token()
            else:
                raise Exception()

        except:
            _api_exception_handler(RESPONSE, "Logout failed")



    return True