from nomad_media_pip.src.exceptions.api_exception_handler import _api_exception_handler

import requests

def _delete_user_session_data(self, AUTH_TOKEN, URL, USER_ID, DEBUG):

    API_URL = f"{URL}/api/admin/user/userSession/{USER_ID}"

    HEADERS = {
        "Authorization": "Bearer " + AUTH_TOKEN,
        "Content-Type": "application/json"
    }

    if DEBUG:
        print(f"URL: {API_URL},\nMETHOD: DELETE")

    while True:
        try:
            RESPONSE = requests.delete(API_URL, headers= HEADERS)
            
            if RESPONSE.ok:
                break

            if RESPONSE.status_code == 403:
                self.refresh_token()
            else:
                raise Exception()
        except:
            _api_exception_handler(RESPONSE, "Delete User Session Data Failed")