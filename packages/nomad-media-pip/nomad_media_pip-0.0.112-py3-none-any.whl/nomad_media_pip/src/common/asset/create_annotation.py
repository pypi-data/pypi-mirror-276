from nomad_media_pip.src.exceptions.api_exception_handler import _api_exception_handler

import requests, json

def _create_annotation(self, AUTH_TOKEN, URL, ASSET_ID, START_TIME_CODE, END_TIME_CODE, TITLE,
                       SUMMARY, DESCRIPTION, DEBUG):
    
    API_URL = f"{URL}/api/asset/{ASSET_ID}/annotation"

    HEADERS = {
        "Content-Type": "application/json",
      	"Authorization": "Bearer " + AUTH_TOKEN
    }

    BODY = {
        "startTimecode": START_TIME_CODE,
        "endTimecode": END_TIME_CODE,
        "properties": {
            "title": TITLE,
            "description": DESCRIPTION,
            "summary": SUMMARY
        }
    }

    if DEBUG:
        print(f"URL: {API_URL}\nMETHOD: POST\nBODY: {json.dumps(BODY, indent=4)}")

    try:
        RESPONSE = requests.post(API_URL, headers=HEADERS, data=json.dumps(BODY))

        if not RESPONSE.ok:
            raise Exception()
        
        return RESPONSE.json()
    
    except:
        _api_exception_handler(RESPONSE, "Create annotation failed")