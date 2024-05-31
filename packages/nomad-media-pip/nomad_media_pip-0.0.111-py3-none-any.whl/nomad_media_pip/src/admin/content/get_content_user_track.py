from nomad_media_pip.src.exceptions.api_exception_handler import _api_exception_handler

import requests
from urllib.parse import urlencode

def _get_content_user_track(self, AUTH_TOKEN, URL, CONTENT_ID, CONTENT_DEFINITION_ID, SORT_COLUMN,
                         IS_DESC, PAGE_INDEX, SIZE_INDEX, DEBUG):
        
    BASE_URL = f"{URL}/api/content/{CONTENT_DEFINITION_ID}/user-track/{CONTENT_ID}"

    PARAMS = { k: v for k, v in {
        "sortColumn": SORT_COLUMN,
        "isDesc": IS_DESC,
        "pageIndex": PAGE_INDEX,
        "sizeIndex": SIZE_INDEX
    }.items() if v is not None }

    API_URL = f"{BASE_URL}?{urlencode(PARAMS)}"

    # Create header for the request
    HEADERS = {
        "Authorization": "Bearer " + AUTH_TOKEN,
        "Content-Type": "application/json"
    }

    if DEBUG:
        print(f"URL: {API_URL},\nMETHOD: GET")

    while True:
        try:
            # Send the request
            RESPONSE = requests.get(API_URL, headers= HEADERS)

            if RESPONSE.ok:
                break

            if RESPONSE.status_code == 403:
                self.refresh_token()
            else:
                raise Exception()
        except:
            _api_exception_handler(RESPONSE, "Get content user track failed")
            
    return RESPONSE.json()