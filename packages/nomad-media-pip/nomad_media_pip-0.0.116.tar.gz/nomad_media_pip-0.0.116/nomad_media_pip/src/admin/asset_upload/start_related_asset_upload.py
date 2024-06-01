from nomad_media_pip.src.exceptions.api_exception_handler import _api_exception_handler

import json, os, requests, time

MAX_RETRIES = 2

def _start_related_asset_upload(self, AUTH_TOKEN, URL, EXISTING_ASSET_ID, RELATED_ASSET_ID, 
                  NEW_RELATED_ASSET_METADATA_TYPE, UPLOAD_OVERWRITE_OPTION, FILE,
                  LANGUAGE_ID, DEBUG):

    API_URL = f"{URL}/api/asset/upload/start-related-asset"
    FILE_STATS = os.stat(FILE)


    FILE_NAME = os.path.basename(FILE)

    AWS_MIN_LIMIT = 5242880
    chunkSize = FILE_STATS.st_size / 10000

    if (chunkSize < (AWS_MIN_LIMIT * 4)):
        chunkSize = 20971520
        
    # Create header for the request
    HEADERS = {
  	    "Authorization": "Bearer " + AUTH_TOKEN,
        "Content-Type": "application/json"
    }

    # Build the payload BODY
    BODY = {
      	"contentLength":FILE_STATS.st_size,
      	"chunkSize": chunkSize,
        "existingAssetId": EXISTING_ASSET_ID,
        "languageId": LANGUAGE_ID,
        "newRelatedAssetMetadataType": NEW_RELATED_ASSET_METADATA_TYPE,
        "relatedAssetId": RELATED_ASSET_ID,
      	"relativePath": FILE_NAME,
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

        
            if retries < MAX_RETRIES:
                retries += 1
                time.sleep(20)
            else:
                _api_exception_handler(RESPONSE, "Start asset upload failed")

        except:
            _api_exception_handler(RESPONSE, "Start asset upload failed")



    return RESPONSE.json()