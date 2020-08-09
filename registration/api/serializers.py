from rest_framework import serializers

from registration.models import UserRegistration



class RegistrationSerializers(serializers.ModelSerializer):
	password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

	class Meta:
		model = UserRegistration
		fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']

		extra_kwargs = {
				'password': {'write_only': True}
		}

	def save(self):
		registration = UserRegistration(
						email=self.validated_data['email'],
						username=self.validated_data['username']
			)
		password = self.validated_data['password']
		password2 = self.validated_data['password2']

		if password != password2:
			raise serializers.ValidationError({'password': 'Password must match.'})

		registration.set_password(password)
		registration.save()
		return registration