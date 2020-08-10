from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest

from .models import UserRegistration, ProjectName, Task, TaskLog

# from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required
# from django.contrib.auth.decorators.csrf import csrf_exempt
import json

from .utils import JsonWebToken
from . import utils 
from .middleware import authenticate


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
				response['message'] = "User not verified"
				response['status'] = "Failed"
			else:
				body = {
					"id": user_data.id,
					"username": user_data.username,
					"email_id" : user_data.email
				}
				token = JsonWebToken()
				body['token'] = token.encryption(body)
				response['data'] = body
				response['message'] = "Login Successful"
				response['status'] = "Success"
	return HttpResponse(json.dumps(response), content_type='text/json')

@authenticate
def task(request):
	response = None
	if request.method == "POST":
		student_task = json.loads(request.body)
		task_name = student_task['task_name']
		project_id = student_task['project_id']
		created_at = student_task['created_at']
		updated_at = student_task['updated_at']
		is_delete = student_task['is_delete']
		task_list = Task(task_name = task_name, project_id = project_id, created_at = created_at)

		try:
			task_list.save()
			print(task_list)
			response = json.dumps([{'Success': 'Task Entered'}])
		except:
			response = json.dumps([{'Error': 'Not Entered, Something went wrong'}])
	return HttpResponse(response, content_type='text/json')

@authenticate
def test(request):
	response = {
		"message": "testing"
	}
	if request.method == "GET":
		print('GET method')
	return HttpResponse(json.dumps(response), content_type='text/json')





@authenticate
def projects(request):
	response = {}
	response['data'] = None
	response['message'] = "Something went wrong"
	response['status'] = "Failed"
	
	if request.method == "GET":
		data = ProjectName.objects.filter().all()
		print(data)
		formatted_data = []
		for b in data:
			formatted_data.append({
				"id": b.id,
				"project_name" : b.proj_name
				})

		response['data'] = formatted_data
		response['message'] = "List of projects"
		response['status'] = "Success"

	return HttpResponse(json.dumps(response), content_type='text/json')




# def home(request):
# 	return render(request, 'registration/home.html')

# @login_required
# def dashboardView(request):
# 	return render(request, 'registration/dashboard.html')






