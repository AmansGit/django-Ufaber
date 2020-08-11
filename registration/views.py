from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required

import json, pytz
from datetime import datetime, timezone

from .models import UserRegistration, ProjectName, Task, TaskLog
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
			# print(usrregistr)
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
		# print(user_data)
		if user_data == None:
			response['data'] = None
			response['message'] = "User Not found"
			response['status'] = "Failed"
		else:
			# print(user_data.password)
			varified = utils.password_varify(password, user_data.password)
			# print(varified)
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
		# is_delete = student_task['is_delete']
		# task_obj = Task.objects.filter(task_name = task_name, project_id=ProjectName)
		
		try:
			project = ProjectName.objects.filter(id = project_id).first()
			if not project:
				raise Exception("Project Not Found") 
			# print("request.user.id: ", request.user.id)
			# print("project.id: ", project.id)
			task_obj = Task(task_name = task_name, project_id = project, user_id = request.user)
			# print("task_obj:", task_obj)
			task_obj.save()
			# print("task_obj.project_id: ", task_obj)
			response = json.dumps({
					"data": {"task_id": task_obj.id},
					'message': 'Task Created',
					"status": "Success"
				})
		except Exception as e:
			# print(e)
			
			response = json.dumps({
					"data": None,
					"message": str(e),
					"status": "Failed"

				})
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
		# print(data)
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




@authenticate
def task_works_on(request):
	response = {}
	body = json.loads(request.body)
	task_id = body['task_id']
	task_obj = Task.objects.filter(id=task_id).first()
	if not task_obj:
		response['data'] = None
		response['message'] = "Task not found"
		response['status'] = "Failed"
	else:
		task_status = body['task_status']
		print(task_status)
		task_log_list = TaskLog.objects.filter(end_time = None, task_id=task_obj.id).all()

		if task_status:
			print(len(task_log_list))
			if len(task_log_list) == 0:
				new_task_log = TaskLog(task_id=task_obj, start_time = datetime.now(timezone.utc))
				new_task_log.save()
				print(new_task_log)

				response['data'] = None
				response['message'] = "Task Created"
				response['status'] = "Success"	

			else:
				response['data'] = None
				response['message'] = "Task is already going on, Please Off the task"
				response['status'] = "Failed"




		else:
			print(len(task_log_list))
			if len(task_log_list) == 0:
				response['data'] = None
				response['message'] = "Task log not yet started"
				response['status'] = "Failed"
			else:
				for task_log in task_log_list:
					task_log.end_time = datetime.now(timezone.utc)
					print("task_log.end_time::", task_log.end_time)
					print("task_log.start_time::", task_log.start_time)
					task_log.duration = task_log.end_time - task_log.start_time
					task_log.save()

				response['data'] = None
				response['message'] = "Task ended"
				response['status'] = "Success"	

	return HttpResponse(json.dumps(response), content_type='text/json')

def task_status():
	pass