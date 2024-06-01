from nomad_media_pip.src.exceptions.api_exception_handler import _api_exception_handler

import requests, json

def _get_content_definition(self, AUTH_TOKEN, URL, ID, DEBUG):

    API_URL = f"{URL}/contentDefinition/{ID}"

    HEADERS = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AUTH_TOKEN}"
    }

    if DEBUG:
        print(f"API_URL: {API_URL}\nMETHOD: GET")

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
            _api_exception_handler(RESPONSE, "Get Content Definition failed")

    return RESPONSE.json()