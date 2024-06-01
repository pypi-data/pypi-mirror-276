from nomad_media_pip.src.exceptions.api_exception_handler import _api_exception_handler

import requests, json

def _create_schedule_item_asset(self, AUTH_TOKEN, URL, SCHEUDLE_ID, ASSET, DAYS, DURATION_TIME_CODE,
                                END_TIME_CODE, PREVIOUS_ITEM, TIME_CODE, DEBUG):
        
    API_URL = f"{URL}/api/admin/schedule/{SCHEUDLE_ID}/item"
    
    HEADERS = {
        "Authorization": "Bearer " + AUTH_TOKEN,
        "Content-Type": "application/json"
    }
    
    BODY = {
        "asset": ASSET,
        "days": DAYS,
        "durationTimeCode": DURATION_TIME_CODE,
        "endTimeCode": END_TIME_CODE,
        "previousItem": PREVIOUS_ITEM,
        "scheduleItemType": "1",
        "sourceType": "3",
        "timeCode": TIME_CODE
    }
    
    if DEBUG:
        print(f"URL: {API_URL},\nMETHOD: POST,\nBODY: {json.dumps(BODY, indent=4)}")
    
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
            _api_exception_handler(RESPONSE, "Create Schedule Item Asset Failed")


    return RESPONSE.json()