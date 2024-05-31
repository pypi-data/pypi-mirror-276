from nomad_media_pip.src.exceptions.api_exception_handler import _api_exception_handler

import requests, json

def _update_playlist_video(self, AUTH_TOKEN, URL, SCHEDULE_ID, ITEM_ID, ASSET, DEBUG):

    API_URL = f"{URL}/api/admin/schedule/{SCHEDULE_ID}/item/{ITEM_ID}"

    HEADERS = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AUTH_TOKEN}"
    }

    BODY = {
        "asset": ASSET
    }

    if DEBUG:
        print(f"API_URL: {API_URL}\nMETHOD: PUT\nBODY: {json.dumps(BODY, indent=4)}")

    while True:
        try:
            RESPONSE = requests.put(API_URL, headers=HEADERS, data=json.dumps(BODY))

            if RESPONSE.ok:
                break

            if RESPONSE.status_code == 403:
                self.refresh_token()
            else:
                raise Exception()
        except:
            _api_exception_handler(RESPONSE, "Update Playlist Video failed")
            
    return RESPONSE.json()