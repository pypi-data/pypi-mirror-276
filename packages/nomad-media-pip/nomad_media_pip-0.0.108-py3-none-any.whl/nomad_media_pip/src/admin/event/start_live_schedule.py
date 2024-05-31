from nomad_media_pip.src.exceptions.api_exception_handler import _api_exception_handler

import requests

def _start_live_schedule(AUTH_TOKEN, URL, EVENT_ID, DEBUG):
    
    API_URL = f"{URL}/api/admin/liveSchedule/content/{EVENT_ID}/start"
    
    HEADERS = {
        "Authorization": "Bearer " + AUTH_TOKEN,
        "Content-Type": "application/json"
    }
    
    if DEBUG:
        print(f"URL: {API_URL},\nMETHOD: POST")
    
    try:
        RESPONSE = requests.post(API_URL, headers= HEADERS)
        
        if not RESPONSE.ok:
            raise Exception()
    except:
        _api_exception_handler(RESPONSE, "Start Live Schedule Failed")