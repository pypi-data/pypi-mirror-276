from nomad_media_pip.src.exceptions.api_exception_handler import _api_exception_handler

import requests, time

MAX_RETRIES = 2

def _upload_asset_part(FILE, URL, PART, DEBUG):
    if not FILE or not URL or not PART:
        raise Exception("Upload Part: Invalid API call")
    
    while True:
        try:
            OPEN_FILE = open(FILE, "rb")
            OPEN_FILE.seek(PART["startingPosition"])
            BODY = OPEN_FILE.read(PART["endingPosition"] + 1 - PART["startingPosition"])
            OPEN_FILE.close()

            HEADER = {
                "Accept": "application/json, text/plain, */*"
            }

            if DEBUG:
                print(f"URL: {URL},\nMETHOD: PUT,\n")

            RESPONSE = requests.put(URL, headers=HEADER, data=BODY)

            if RESPONSE.ok:
                break

            raise Exception()
        
        except requests.exceptions.Timeout:
            if retries < MAX_RETRIES:
                retries += 1
                time.sleep(20)
            else:
                _api_exception_handler(RESPONSE, "Upload part failed")
        
        except:
            _api_exception_handler(RESPONSE, "Upload part failed")

    return RESPONSE.headers.get("ETag")