from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from registration.api.serializers import RegistrationSerializers

@api_view(['POST'])
def registration_view(request):
	if request.method == 'POST':
		serializer = RegistrationSerializers(data=request.data)
		data = {}
		if serializer.is_valid():
			registration = serializer.save()
			data['response'] = "Successfully registered a new user"
			data['email'] = registration.email
			data['username'] = registration.username
			data['first_name'] = registration.first_name
			data['last_name'] = registration.last_name

		else:
			data = serializer.errors

		return Response(data)