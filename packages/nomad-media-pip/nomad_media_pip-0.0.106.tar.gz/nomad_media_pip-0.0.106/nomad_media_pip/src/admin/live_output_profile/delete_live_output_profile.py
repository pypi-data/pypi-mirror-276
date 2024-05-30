from nomad_media_pip.src.exceptions.api_exception_handler import _api_exception_handler

import requests

def _delete_live_output_profile(AUTH_TOKEN, URL, ID, DEBUG):

    API_URL = f"{URL}/api/liveOutputProfile/{ID}"

    HEADERS = {
        "Authorization": "Bearer " + AUTH_TOKEN,
        "Content-Type": "application/json"
    }

    if DEBUG:
        print(f"URL: {API_URL},\nMETHOD: DELETE")

    try:
        RESPONSE = requests.delete(API_URL, headers=HEADERS)

        if not RESPONSE.ok:
            raise Exception()

    except:
        _api_exception_handler(RESPONSE, "Delete Live Output Profile Failed")