from nomad_media_pip.src.exceptions.api_exception_handler import _api_exception_handler

import json, requests, time

MAX_RETRIES = 2

def _post_search(self, AUTH_TOKEN, URL, QUERY, OFFSET, SIZE, FILTERS, SORT_FIELDS, RESULT_FIELDS, 
                 SIMILAR_ASSET_ID, MIN_SCORE, EXCLUDE_TOTAL_RECORD_COUNT, FILTER_BINDER, 
				 IS_ADMIN, DEBUG):
	API_URL = f"{URL}/api/admin/search" if IS_ADMIN else f"{URL}/api/portal/search"

	# Create header for the request
	HEADERS = {
		"Authorization": "Bearer " + AUTH_TOKEN,
		"Content-Type": "application/json"
	}

	# Build the payload BODY
	BODY = {}


	if QUERY: BODY["searchQuery"] = QUERY 
	BODY["pageOffset"] = OFFSET if OFFSET else 0
	BODY["pageSize"] = SIZE if SIZE else 100
	if FILTERS: BODY["filters"] = FILTERS
	if SORT_FIELDS: BODY["sortFields"] = SORT_FIELDS
	if RESULT_FIELDS: BODY["resultFields"] = RESULT_FIELDS
	if SIMILAR_ASSET_ID: BODY["similarAssetId"] = SIMILAR_ASSET_ID
	if MIN_SCORE: BODY["minScore"] = MIN_SCORE
	if EXCLUDE_TOTAL_RECORD_COUNT: BODY["excludeTotalRecordCount"] = EXCLUDE_TOTAL_RECORD_COUNT
	if FILTER_BINDER: BODY["filterBinder"] = FILTER_BINDER

	if DEBUG:
		print(f"URL: {API_URL},\nMETHOD: POST\nBODY: {json.dumps(BODY, indent= 4)}")

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
				_api_exception_handler(RESPONSE, "Searching failed")
				 
		except:
			_api_exception_handler(RESPONSE, "Searching failed")


	return RESPONSE.json()