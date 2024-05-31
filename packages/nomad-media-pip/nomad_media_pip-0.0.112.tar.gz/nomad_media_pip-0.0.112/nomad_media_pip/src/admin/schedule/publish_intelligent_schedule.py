from nomad_media_pip.src.exceptions.api_exception_handler import _api_exception_handler

import requests, json

def _publish_intelligent_schedule(self, AUTH_TOKEN, URL, SCHEDULE_ID, NUMBER_OR_LOCKED_DAYS, DEBUG):

    API_URL = f"{URL}/api/admin/schedule/{SCHEDULE_ID}/publish"

    HEADERS = {
        "Authorization": "Bearer " + AUTH_TOKEN,
        "Content-Type": "application/json"
    }

    BODY = {
        "number_of_days": NUMBER_OR_LOCKED_DAYS
    }

    if DEBUG:
        print(f"URL: {API_URL},\nMETHOD: POST")

    while True:
        try:
            RESPONSE = requests.post(API_URL, headers= HEADERS, data= json.dumps(BODY))

            if RESPONSE.ok:
                break
            
            if RESPONSE.status_code == 403:
                self.refresh_token()
            else:
                raise Exception()
        except:
            _api_exception_handler(RESPONSE, "Publish Intelligent Schedule Failed")
            
    return RESPONSE.json()