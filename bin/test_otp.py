#!/usr/bin/python
import urllib2
import urllib
import random

YUBI_API_ERRORS = {
	'OK': 'The OTP is valid.',
	'BAD_OTP': 'The OTP is invalid format.',
	'REPLAYED_OTP': 'The OTP has already been seen by the service.',
	'BAD_SIGNATURE': 'The request lacks a parameter.',
	'MISSING_PARAMETER': 'The request lacks a parameter.',
	'NO_SUCH_CLIENT': 'The request id does not exist.',
	'OPERATION_NOT_ALLOWED': 'The request id is not allowed to verify OTPs.',
	'BACKEND_ERROR': 'Unexpected error in our server. Please contact us if you see this error.',
	'NOT_ENOUGH_ANSWERS': 'Server could not get requested number of syncs during before timeout',
	'REPLAYED_REQUEST': 'Server has seen the OTP/Nonce combination before',
}

YUBI_DEFAULT_ENDPOINTS = [
	'https://api.yubico.com/wsapi/2.0/verify',
	'https://api2.yubico.com/wsapi/2.0/verify',
	'https://api3.yubico.com/wsapi/2.0/verify',
	'https://api4.yubico.com/wsapi/2.0/verify',
	'https://api5.yubico.com/wsapi/2.0/verify',
]

YUBI_API_ID = ''

def check_key(endpoints, otp):
	# Build a random nonce
	nonce = ''.join(
				random.sample(
					'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
					random.randint(16, 40)
				)
			)

	# Data we send to the server
	data = {
		'id': YUBI_API_ID, # Yubi api ID
		'otp': otp, # OTP
		'nonce': nonce, # Nonce
	}

	# Try and get a response from each endpoint
	for endpoint in filter(None, endpoints.split(',')):
		try:
			# Send the request
			response = urllib2.urlopen("%s?%s" % (endpoint, urllib.urlencode(data)))
		except (urllib2.URLError, urllib2.HTTPError):
			print "%s failed" % endpoint
			pass

	# Nice message we might update later
	nice_message = "Unknown"

	# Check a server returned successfully
	if response:
		# Read the response
		raw = response.read()

		# Dict of data we are going to "fill in"
		data = {
			'h': None, # Signature
			'sl': None, # Percentage of servers that replied successfully
			't': None, # Timestamp (UTC)
			'otp': None, # OTP
			'nonce': None, # Nonce
			'status': None, # Validation status
		}

		# Loop though the response lines and fill the data dict
		for line in raw.split("\n"):
			if len(line.strip()) == 0: continue
			(key, val) = line.split("=", 1)
			if key.lower() in data:
				data[key.lower()] = val.strip()
			else:
				print "%s unknown" % key

		# Pretty response
		if data['status'] in YUBI_API_ERRORS:
			nice_message = YUBI_API_ERRORS[data['status']]

		# Check everything looks good
		if data['status'] == "OK" and data['otp'] == otp and data['nonce'] == nonce:
			return (True, nice_message)

	return (False, nice_message)

if __name__ == "__main__":
	otp = str(raw_input("OTP? "))
	response = check_key(
		','.join(YUBI_DEFAULT_ENDPOINTS),
		otp
	)

	if response[0] == True:
		print "OTP ok"
	else:
		print "OTP not ok"
		print "Server said:\n %s" % response[1]
