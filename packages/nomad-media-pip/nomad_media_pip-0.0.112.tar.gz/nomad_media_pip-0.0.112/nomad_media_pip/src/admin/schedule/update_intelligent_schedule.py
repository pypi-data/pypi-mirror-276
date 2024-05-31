from nomad_media_pip.src.exceptions.api_exception_handler import _api_exception_handler
from nomad_media_pip.src.admin.schedule.get_intelligent_schedule import _get_intelligent_schedule

import requests, json

def _update_intelligent_schedule(self, AUTH_TOKEN, URL, ID, DEFAULT_VIDEO_ASSET, NAME, THUMBNAIL_ASSET, 
                               TIME_ZONE_ID, DEBUG):
    
    API_URL = f"{URL}/api/admin/schedule/{ID}"
    
    SCHEDULE = _get_intelligent_schedule(self, AUTH_TOKEN, URL, ID, DEBUG)
    
    HEADERS = {
        "Authorization": "Bearer " + AUTH_TOKEN,
        "Content-Type": "application/json"
    }

    BODY = {
        "defaultVideoAsset": DEFAULT_VIDEO_ASSET or SCHEDULE.get("defaultVideoAsset"),
        "name": NAME or SCHEDULE.get("name"),
        "scheduleType": "3",
        "thumbnailAsset": THUMBNAIL_ASSET or SCHEDULE.get("thumbnailAsset"),
        "timeZoneId": TIME_ZONE_ID or SCHEDULE.get("timeZoneId"),
        "id": ID,
    }

    if DEBUG:
        print(f"URL: {API_URL},\nMETHOD: PUT,\nBODY: {json.dumps(BODY, indent=4)}")

    while True:
        try:
            RESPONSE = requests.put(API_URL, headers= HEADERS, data= json.dumps(BODY))
            
            if RESPONSE.ok:
                break
            
            if RESPONSE.status_code == 403:
                self.refresh_token()
            else:
                raise Exception()
        except:
            _api_exception_handler(RESPONSE, "Update Intelligent Schedule Failed")
            
    return RESPONSE.json()