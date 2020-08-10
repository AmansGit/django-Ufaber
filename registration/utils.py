import bcrypt, json, hashlib, base64

import jwt
import datetime




def encrypt_password(password):
	# return bcrypt.hashpw(base64.b64encode(hashlib.sha256('{}'.format(password).encode()).digest()),bcrypt.gensalt())
	return bcrypt.hashpw("password".encode('utf8'), bcrypt.gensalt()).decode("utf8")

def password_varify(password, hashpw):
	print(password, hashpw)
	password = '{}'.format(password).encode('utf8')
	hashpw = '{}'.format(hashpw).encode('utf8')
	print(password)
	if bcrypt.checkpw(password, hashpw):
		return True
	else:
		return False


class JsonWebToken:

	def __init__(self):
		self.secret_key = "asiufbwefv,nd askhfsafjiauyfawensydfgaiba sdfsbfhwe"

	def encryption(self, body={}):
		current_time = datetime.datetime.now()
		body['iat'] = current_time.timestamp()
		body['exp'] = (current_time + datetime.timedelta(seconds = 500)).timestamp()
		return jwt.encode(body, self.secret_key, algorithm='HS256').decode('utf-8')

	def decryption(self, token):
		options = {'verify_exp': True}
		
		try:
			return jwt.decode(token, self.secret_key, algorithms=['HS256'], options=options)
		except Exception as e:
			return None
