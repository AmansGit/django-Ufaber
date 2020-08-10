from .utils import JsonWebToken
from django.http import HttpResponse
import json

def authenticate(func_name):
	def middleware(request):
		# print('request: ', request)
		# print(dir(request))
		# print(request.headers)
		if 'Token' not in request.headers or not request.headers['Token']:
			# print("token not found")
			response = {}
			response['data'] = None
			response['message'] = "Toekn Not found"
			response['status'] = "Failed"
			return HttpResponse(json.dumps(response), content_type='text/json', status=401)

		else:
			token = request.headers['Token']
			# print("Tokenn: ",token)
		
			jwtt = JsonWebToken()
			auth_object = jwtt.decryption(token)
			print(auth_object)
			if auth_object == None:
				response = {}
				response['data'] = None
				response['message'] = "Token Expired"
				response['status'] = "Failed"
				return HttpResponse(json.dumps(response), content_type='text/json', status=400)

			request.user = auth_object
			return func_name(request)

	# print('func_name:', func_name)
	return middleware