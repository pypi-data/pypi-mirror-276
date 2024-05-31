from nomad_media_pip.src.exceptions.api_exception_handler import _api_exception_handler
from nomad_media_pip.src.admin.live_channel.live_channel_statuses import _LIVE_CHANNEL_STATUSES
from nomad_media_pip.src.admin.live_channel.wait_for_live_channel_status import _wait_for_live_channel_status

import json, requests

def _stop_live_channel(self, AUTH_TOKEN, URL, CHANNEL_ID, WAIT_FOR_STOP, DEBUG):
    API_URL = f"{URL}/api/liveChannel/{CHANNEL_ID}/stop"

    # Create header for the request
    HEADERS = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + AUTH_TOKEN
    }

    if (DEBUG):
        print(f"API_URL: {API_URL}\nMETHOD: POST")

    while True:
        try:
            RESPONSE = requests.post(API_URL, headers= HEADERS)

            if RESPONSE.ok:
                if WAIT_FOR_STOP == False: return
                # Wait for the live channel to be idle
                _wait_for_live_channel_status(self, AUTH_TOKEN, URL, CHANNEL_ID, _LIVE_CHANNEL_STATUSES["Idle"], 120, 2, DEBUG)

                break

            if RESPONSE.status_code == 403:
                self.refresh_token()
            else:
                raise Exception()

        except:
            _api_exception_handler(RESPONSE, "Stop Live Channel " + CHANNEL_ID + " failed")

