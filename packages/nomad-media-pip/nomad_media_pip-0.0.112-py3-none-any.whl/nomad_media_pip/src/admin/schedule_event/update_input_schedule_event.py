from nomad_media_pip.src.exceptions.api_exception_handler import _api_exception_handler
from nomad_media_pip.src.admin.schedule_event.event_types import _EVENT_TYPES
from nomad_media_pip.src.admin.schedule_event.get_input_schedule_event import _get_input_schedule_event

import requests, json

def _update_input_schedule_event(self, AUTH_TOKEN, URL, ID, CHANNEL_ID, INPUT, BACKUP_INPUT,
                                 FIXED_ON_AIR_TIME_UTC, DEBUG):
    
    API_URL = f"{URL}/api/liveChannel/{CHANNEL_ID}/liveScheduleEvent"

    SCHEDULE_EVENT_INFO = _get_input_schedule_event(self, AUTH_TOKEN, URL, CHANNEL_ID,
                                                    ID, DEBUG)
    
    HEADERS = {
        "Authorization": "Bearer " + AUTH_TOKEN,
        "Content-Type": "application/json"
    }

    BODY = {
        "id": ID,
        "channelId": CHANNEL_ID,
        "liveInput": INPUT or SCHEDULE_EVENT_INFO.get('input'),
        "liveInput2": BACKUP_INPUT or SCHEDULE_EVENT_INFO.get('backupInput'),
        "fixedOnAirTimeUTC": FIXED_ON_AIR_TIME_UTC or SCHEDULE_EVENT_INFO.get('fixedOnAirTimeUTC'),
        "type": {
            "id": _EVENT_TYPES["liveInput"],
            "description": "Live Input"
        }
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
            _api_exception_handler(RESPONSE, "Update Input Schedule Event Failed")
            
    return RESPONSE.json()