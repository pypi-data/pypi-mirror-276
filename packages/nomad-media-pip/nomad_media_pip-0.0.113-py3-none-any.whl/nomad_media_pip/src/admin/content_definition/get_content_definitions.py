from nomad_media_pip.src.exceptions.api_exception_handler import _api_exception_handler

import requests, json

def _get_content_definitions(self, AUTH_TOKEN, URL, CONTENT_MANAGEMENT_TYPE, SORT_COLUMN, IS_DESC, PAGE_INDEX, PAGE_SIZE, DEBUG):

    API_URL = f"{URL}/contentDefinition"

    HEADERS = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AUTH_TOKEN}"
    }

    PARAMS = {
        "contentManagementType": CONTENT_MANAGEMENT_TYPE,
        "sortColumn": SORT_COLUMN,
        "isDesc": IS_DESC,
        "pageIndex": PAGE_INDEX,
        "pageSize": PAGE_SIZE
    }

    if DEBUG:
        print(f"API_URL: {API_URL}\nMETHOD: GET, PARAMS: {PARAMS}")

    while True:
        try:
            RESPONSE = requests.get(API_URL, headers=HEADERS, params=PARAMS)

            if RESPONSE.ok:
                break

            if RESPONSE.status_code == 403:
                self.refresh_token()
            else:
                raise Exception()
        except:
            _api_exception_handler(RESPONSE, "Get Content Definitions failed")
            
    return RESPONSE.json()