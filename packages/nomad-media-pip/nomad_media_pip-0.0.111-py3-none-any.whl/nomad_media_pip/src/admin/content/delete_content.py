from nomad_media_pip.src.exceptions.api_exception_handler import _api_exception_handler

import requests

def _delete_content(self, AUTH_TOKEN, URL, ID, CONTENT_DEFINITION_ID, DEBUG):
  
    API_URL = f"{URL}/api/content/{ID}?contentDefinitionId={CONTENT_DEFINITION_ID}"
    
    HEADERS = {
      "Content-Type": "application/json",
      "Authorization": "Bearer " + AUTH_TOKEN
    }

    if DEBUG:
        print(f"URL: {API_URL},\nMETHOD: DELETE")

    while True:
        try:
            RESPONSE = requests.delete(API_URL, headers=HEADERS)

            if RESPONSE.ok:
                break

            if RESPONSE.status_code == 403:
                self.refresh_token()
            else:
                raise Exception()

        except:
            _api_exception_handler(RESPONSE, "Deleting content failed")