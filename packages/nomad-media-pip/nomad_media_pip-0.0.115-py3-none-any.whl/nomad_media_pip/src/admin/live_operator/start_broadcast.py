from nomad_media_pip.src.exceptions.api_exception_handler import _api_exception_handler
from nomad_media_pip.src.admin.live_operator.wait_for_live_operator_status import _wait_for_live_operator_status

import requests, json

def _start_broadcast(self, AUTH_TOKEN, URL, ID, PREROLL_ASSET_ID, POSTROLL_ASSET_ID, LIVE_INPUT_ID, 
                    RELATED_CONTENT_IDS, TAG_IDS, DEBUG):
    API_URL = f"{URL}/api/admin/liveOperator/start"

    HEADERS = {
        "Authorization": "Bearer " +  AUTH_TOKEN,
        "Content-Type": "application/json"
    }
    
    BODY = {
        "id": ID
    }

    if LIVE_INPUT_ID: BODY["liveInput"] = { "id": LIVE_INPUT_ID }
    if PREROLL_ASSET_ID: BODY["prerollAsset"] = { "id": PREROLL_ASSET_ID }
    if POSTROLL_ASSET_ID: BODY["postrollAsset"] = { "id": POSTROLL_ASSET_ID }

    if RELATED_CONTENT_IDS and isinstance(RELATED_CONTENT_IDS, list) and len(RELATED_CONTENT_IDS) > 0:
        BODY["relatedContent"] = [{"id": id} for id in RELATED_CONTENT_IDS]

    if TAG_IDS and isinstance(TAG_IDS, list) and len(TAG_IDS) > 0:
        BODY["tags"] = [{"id": id} for id in TAG_IDS]

    if (DEBUG):
        print(f"API_URL: {API_URL}\nMETHOD: POST\nBODY: {json.dumps(BODY, indent= 4)}")

    while True:
        try:
            RESPONSE = requests.post(API_URL, headers= HEADERS, data= json.dumps(BODY))

            if RESPONSE.ok:
                _wait_for_live_operator_status(self, AUTH_TOKEN, URL, ID, "Running", 1200, 20, DEBUG)
                break

            if RESPONSE.status_code == 403:
                self.refresh_token()
            else:
                raise Exception()
        
        except:
            _api_exception_handler(RESPONSE, f"Starting broadcast for Live Channel {ID} failed")


    return RESPONSE.json()