from django import forms

from .models import UserRegistration

class UserRegisterForm(forms.ModelForm):
	class Meta:
		model = UserRegistration
		fields = [
			'username', 'first_name', 'last_name'
		]