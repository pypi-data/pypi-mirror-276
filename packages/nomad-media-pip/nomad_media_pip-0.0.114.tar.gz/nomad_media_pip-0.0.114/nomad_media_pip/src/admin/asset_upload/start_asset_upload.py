from nomad_media_pip.src.exceptions.api_exception_handler import _api_exception_handler

import json, os, requests, time

MAX_RETRIES = 2

def _start_upload(self, AUTH_TOKEN, URL, NAME, EXISTING_ASSET_ID, RELATED_CONTENT_ID, 
                  UPLOAD_OVERWRITE_OPTION, FILE, PARENT_ID, LANGUAGE_ID, DEBUG):

    API_URL = f"{URL}/api/asset/upload/start"
    FILE_STATS = os.stat(FILE)


    FILE_NAME = os.path.basename(FILE)

    CHUNK_SIZE = 8388608
        
    # Create header for the request
    HEADERS = {
  	    "Authorization": "Bearer " + AUTH_TOKEN,
        "Content-Type": "application/json"
    }

    # Build the payload BODY
    BODY = {
        "displayName": NAME or FILE_NAME,
      	"contentLength":FILE_STATS.st_size,
      	"uploadOverwriteOption": UPLOAD_OVERWRITE_OPTION,
      	"chunkSize": CHUNK_SIZE,
      	"relativePath": FILE_NAME,
        "parentId":	PARENT_ID,
        "existingAssetId": EXISTING_ASSET_ID,
        "relatedContentId": RELATED_CONTENT_ID,
        "languageId": LANGUAGE_ID,
        "uploadOverwriteOption": UPLOAD_OVERWRITE_OPTION
    }

    if DEBUG:
        print(f"URL: {API_URL},\nMETHOD: POST,\nBODY: {json.dumps(BODY, indent=4)}")

    retries = 0
    while True:
        try:
            # Send the request
            RESPONSE = requests.post(API_URL, headers= HEADERS, data= json.dumps(BODY))

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
                _api_exception_handler(RESPONSE, "Start asset upload failed")

        except:
            _api_exception_handler(RESPONSE, "Start asset upload failed")


    return RESPONSE.json()