from django.urls import path
from registration.api.views import (
		registration_view
	)	
app_name = "registration"

urlpatterns = [
	path('register', registration_view, name="register"),
]