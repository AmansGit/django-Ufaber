from django.db import models
from django import forms

# new user::
class UserRegistration(models.Model):
	id = models.AutoField(primary_key=True, default=True)
	username = models.CharField(max_length=11, unique=True, null=False)
	first_name = models.CharField(max_length=10,blank=False)
	last_name = models.CharField(max_length=20, blank=True)
	email = models.EmailField(max_length=100,null=False,blank=True)
	password = models.CharField(max_length=50,blank=False)
	class Meta:
		db_table = "user"

	def __str__(self):
		return self.username


#PROJECT NAME
class ProjectName(models.Model):
	id = models.AutoField(primary_key=True)
	proj_name = models.CharField(max_length=20, blank=False, null=False, unique=True)
	class Meta:
		db_table = "project"


# AFTER LOGGED IN
class Task(models.Model):
	id = models.AutoField(primary_key=True)
	task_name = models.CharField(max_length=50, blank=False, null=False)
	user_id = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
	project_id = models.ForeignKey(ProjectName, on_delete=models.CASCADE)
	start_time = models.DateTimeField(null = True)
	end_time = models.DateTimeField(null = True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	is_delete = models.BooleanField(default=False)
	class Meta:
		db_table = "task"


class TaskLog(models.Model):
	id = models.AutoField(primary_key=True)
	task_id = models.ForeignKey(Task, blank=False, null=False, on_delete=models.CASCADE)
	start_time = models.DateTimeField(null=False)
	end_time = models.DateTimeField(null=True)
	duration = models.DurationField(null=True)
	class Meta:
		db_table = "task_log"

