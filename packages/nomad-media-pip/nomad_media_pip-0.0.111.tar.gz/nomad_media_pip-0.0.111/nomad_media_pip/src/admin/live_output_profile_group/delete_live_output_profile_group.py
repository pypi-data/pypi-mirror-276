from nomad_media_pip.src.exceptions.api_exception_handler import _api_exception_handler

import requests, json

def _delete_live_output_profile_group(self, AUTH_TOKEN, URL, LIVE_OUTPUT_PROFILE_GROUP_ID, DEBUG):

	API_URL = f"{URL}/api/liveOutputProfileGroup/{LIVE_OUTPUT_PROFILE_GROUP_ID}"

	HEADERS = {
		"Content-Type": "application/json",
		"Authorization": f"Bearer {AUTH_TOKEN}"
	}

	if DEBUG:
		print(f"API_URL: {API_URL}\nMETHOD: DELETE")

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
			_api_exception_handler(RESPONSE, "Delete Live Output Profile Group Failed")
			
	return RESPONSE.json()