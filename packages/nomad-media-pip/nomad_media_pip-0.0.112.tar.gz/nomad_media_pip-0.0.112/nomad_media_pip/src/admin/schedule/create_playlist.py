from nomad_media_pip.src.exceptions.api_exception_handler import _api_exception_handler

import requests, json

def _create_playlist(self, AUTH_TOKEN, URL, NAME, THUMBNAIL_ASSET, LOOP_PLAYLIST, DEFAULT_VIDEO_ASSET, DEBUG):

    API_URL = f"{URL}/api/admin/schedule"
    
    HEADERS = {
        "Authorization": "Bearer " + AUTH_TOKEN,
        "Content-Type": "application/json"
    }
    
    BODY = {
        "name": NAME,
        "scheduleType": "1",
        "thumbnailAsset": THUMBNAIL_ASSET,
        "loopPlaylist": LOOP_PLAYLIST,
        "defaultVideoAsset": DEFAULT_VIDEO_ASSET
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
            _api_exception_handler(RESPONSE, "Create Playlist Failed")
            
    return RESPONSE.json()