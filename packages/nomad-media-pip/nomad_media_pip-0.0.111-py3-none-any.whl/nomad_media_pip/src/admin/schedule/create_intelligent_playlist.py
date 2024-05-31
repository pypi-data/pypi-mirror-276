from nomad_media_pip.src.exceptions.api_exception_handler import _api_exception_handler
from nomad_media_pip.src.admin.schedule.delete_intelligent_playlist import _delete_intelligent_playlist

import requests, json

def _create_intelligent_playlist(self, AUTH_TOKEN, URL, COLLECTIONS, END_SEARCH_DATE, 
                                 END_SEARCH_DURATION_IN_MINUTES, NAME, RELATED_CONTENT, 
                                 SEARCH_DATE, SEARCH_DURATION_IN_MINUTES, SEARCH_FILTER_TYPE, 
                                 TAGS, THUMBNAIL_ASSET, DEBUG):
    
    SCHEDULE_API_URL = f"{URL}/api/admin/schedule"

    
    HEADERS = {
        "Authorization": "Bearer " + AUTH_TOKEN,
        "Content-Type": "application/json"
    }

    SCHEUDLE_BODY = {
        "name": NAME,
        "scheduleType": "4",
        "thumbnailAsset": THUMBNAIL_ASSET
    }

    if DEBUG:
        print(f"URL: {SCHEDULE_API_URL},\nMETHOD: POST,\nBODY: {json.dumps(SCHEUDLE_BODY)}")

    while True:
        try:
            SCHEDULE_RESPONSE = requests.post(SCHEDULE_API_URL, headers= HEADERS, data= json.dumps(SCHEUDLE_BODY))

            if SCHEDULE_RESPONSE.ok:
                break

            if SCHEDULE_RESPONSE.status_code == 403:
                self.refresh_token()
            else:
                raise Exception()
        except:
            _api_exception_handler(SCHEDULE_RESPONSE, "Create Intelligent Playlist Failed")

    SCHEDULE_INFO = SCHEDULE_RESPONSE.json()

    ITEM_API_URL = f"{SCHEDULE_API_URL}/{SCHEDULE_INFO['id']}/item"

    ITEM_BODY = {
        "collections": COLLECTIONS,
        "endSearchDate": END_SEARCH_DATE,
        "endSearchDurationInMinutes": END_SEARCH_DURATION_IN_MINUTES,
        "name": NAME,
        "relatedContent": RELATED_CONTENT,
        "searchDate": SEARCH_DATE,
        "searchDurationInMinutes": SEARCH_DURATION_IN_MINUTES,
        "searchFilterType": SEARCH_FILTER_TYPE,
        "tags": TAGS,
        "thumbnailAsset": THUMBNAIL_ASSET
    }

    if DEBUG:
        print(f"URL: {ITEM_API_URL},\nMETHOD: POST,\nBODY: {json.dumps(ITEM_BODY)}")

    while True:
        try:
            RESPONSE = requests.post(ITEM_API_URL, headers= HEADERS, data= json.dumps(ITEM_BODY))

            if RESPONSE.ok:
                ITEM_INFO = RESPONSE.json()

                for param in SCHEDULE_INFO:
                    ITEM_INFO[param] = SCHEDULE_INFO[param]

                break

            if RESPONSE.status_code == 403:
                self.refresh_token()
            else:
                raise Exception()
            
        except:
            _delete_intelligent_playlist(self, AUTH_TOKEN, URL, SCHEDULE_INFO["id"], DEBUG)
            _api_exception_handler(RESPONSE, "Create Intelligent Playlist Failed")
        
    return ITEM_INFO