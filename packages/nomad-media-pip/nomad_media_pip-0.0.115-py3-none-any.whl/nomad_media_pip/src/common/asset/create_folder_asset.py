from nomad_media_pip.src.exceptions.api_exception_handler import _api_exception_handler

import requests, json, time

MAX_RETRIES = 2

def _create_folder_asset(self, AUTH_TOKEN, URL, PARENT_ID, DISPLAY_NAME, DEBUG):

    API_URL = f"{URL}/api/admin/asset/{PARENT_ID}/create-folder"

    HEADERS = {
        "Content-Type": "application/json",
      	"Authorization": "Bearer " + AUTH_TOKEN
    }

    BODY = {
        "displayName": DISPLAY_NAME
    }

    if DEBUG:
        print(f"URL: {API_URL}\nMETHOD: POST\nBODY: {json.dumps(BODY, indent=4)}")

    while True:
        try:
            RESPONSE = requests.post(API_URL, headers=HEADERS, data=json.dumps(BODY))

            if RESPONSE.ok:
                break
            
            if RESPONSE.status_code == 403:
                self.refresh_token()
            else:
              raise Exception()

        except requests.exceptions.Timeout:
          if retries < MAX_RETRIES:
              retries += 1
              time.sleep(20)
          else:
              _api_exception_handler(RESPONSE, "Create folder asset failed")

        except:
            _api_exception_handler(RESPONSE, "Create folder asset failed")

    return RESPONSE.json()