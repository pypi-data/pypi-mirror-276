from nomad_media_pip.src.exceptions.api_exception_handler import _api_exception_handler

import json, requests, time

MAX_RETRIES = 2

def _add_custom_properties(self, AUTH_TOKEN, URL, ID, NAME, DATE, CUSTOM_PROPERTIES, DEBUG):

    API_URL = f"{URL}/api/admin/asset/{ID}"
        
    # Create header for the request
    HEADERS = {
  	    "Authorization": "Bearer " + AUTH_TOKEN,
        "Content-Type": "application/json"
    }

    BODY = {}

    if NAME: BODY["displayName"] = NAME
    if DATE: BODY["displayDate"] = DATE
    if CUSTOM_PROPERTIES: BODY["customProperties"] = CUSTOM_PROPERTIES

    if DEBUG: 
        print(f"URL: {API_URL},\nMETHOD: PATCH,\nBODY: {json.dumps(BODY, indent=4)}")

    while True:
        try:
            # Send the request
            RESPONSE = requests.patch(API_URL, headers= HEADERS, data= json.dumps(BODY))

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
                _api_exception_handler(RESPONSE, "add custom properties failed")
				 
        except:
            _api_exception_handler(RESPONSE, "add custom properties failed")

    return RESPONSE.json()