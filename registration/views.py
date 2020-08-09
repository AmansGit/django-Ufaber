from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest

from .models import UserRegistration, ProjectName, UserLog

# from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required
# from django.contrib.auth.decorators.csrf import csrf_exempt

import json
from . import utils 

# @csrf_exempt
def new_user_registration(request):
	response = None
	if request.method == 'POST':
		student = json.loads(request.body)
		username = student['username']
		first_name = student['first_name']
		last_name = student['last_name']
		email_id = student['email']
		password = utils.encrypt_password(student['password'])
		usrregistr = UserRegistration(username=username, first_name=first_name, 
					last_name=last_name, email=email_id, password=password)
		try:

			usrregistr.save()
			print(usrregistr)
			response = json.dumps([{'Success': 'Registered carefully!!'}])
		except:
			response = json.dumps([{'Error': 'Something went wrong!! Try Agian'}])

	return HttpResponse(response, content_type='text/json')


def login(request):
	response = {}
	if request.method == 'POST':
		body = json.loads(request.body)
		username = body['username']
		password = body['password']
		user_data = UserRegistration.objects.filter(username=username).first()
		print(user_data)
		if user_data == None:
			response['data'] = None
			response['message'] = "User Not found"
			response['status'] = "Failed"
		else:
			print(user_data.password)
			varified = utils.password_varify(password, user_data.password)
			print(varified)
			if varified == False:
				response['data'] = None
				response['password'] = "User not verified"
				response['status'] = "Failed"
	return HttpResponse(json.dumps(response), content_type='text/json')




def home(request):
	return render(request, 'registration/home.html')

@login_required
def dashboardView(request):
	return render(request, 'registration/dashboard.html')
