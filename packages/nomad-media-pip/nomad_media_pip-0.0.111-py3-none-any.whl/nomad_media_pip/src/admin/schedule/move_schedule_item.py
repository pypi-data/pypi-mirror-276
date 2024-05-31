from nomad_media_pip.src.exceptions.api_exception_handler import _api_exception_handler

import requests, json

def _move_schedule_item(self, AUTH_TOKEN, URL, ID, ITEM_ID, PREVIOUS_ITEM, DEBUG):
    
    API_URL = f"{URL}/api/admin/schedule/{ID}/item/{ITEM_ID}/move"

    HEADERS = {
        "Authorization": "Bearer " + AUTH_TOKEN,
        "Content-Type": "application/json"
    }

    BODY = {
        "previous_item": PREVIOUS_ITEM
    }

    if DEBUG:
        print(f"URL: {API_URL},\nMETHOD: POST")

    while True:
        try:
            RESPONSE = requests.post(API_URL, headers= HEADERS, data=json.dumps(BODY))

            if RESPONSE.ok:
                break
            
            if RESPONSE.status_code == 403:
                self.refresh_token()
            else:
                raise Exception()
        except:
            _api_exception_handler(RESPONSE, "Move Schedule Item Failed")
            
    return RESPONSE.json()