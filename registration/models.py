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


	def __str__(self):
		return self.username


#PROJECT NAME
class ProjectName(models.Model):
	id = models.AutoField(primary_key=True)
	proj_name = models.CharField(max_length=20, blank=False, null=False)


# AFTER LOGGED IN
class UserLog(models.Model):
	id = models.AutoField(primary_key=True)
	task_name = models.CharField(max_length=50, blank=False, null=False)
	project_name = models.ForeignKey(ProjectName, on_delete=models.CASCADE)
	start_time = models.TimeField()
	end_time = models.TimeField()
	duration = models.DurationField()


# 	def save(self, *args, **kwargs ):


# 	def __str__(self):
# 		return self.task_name