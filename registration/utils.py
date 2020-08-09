import bcrypt, json, hashlib, base64
from jwt.utils import get_int_from_datetime

from jwt import (
	JWT,
	jwk_from_dict
)
from jwt.utils import get_int_from_datetime
import datetime



# class JsonWebToken():

# 	def __init__(self):
# 		self.instance = JWT()
# 		self.signing_key = jwk_from_dict({})   

# 	def encryption(self, body={}):
# 		body['iat'] = get_int_from_datetime(datetime.now(timezone.utc)) #initiated time
# 		body['exp'] = get_int_from_datetime(datetime.now(timezone.utc) + timedelta(hours=1)) #Expire time
# 		return self.instance.encode(body, self.signing_key, alg='RS256')

# 	def decryption(self, token):
# 		return self.instance.decode(token, self.signing_key, alg='RS256', do_time_check=True)


def encrypt_password(password):
	# return bcrypt.hashpw(base64.b64encode(hashlib.sha256('{}'.format(password).encode()).digest()),bcrypt.gensalt())
	return bcrypt.hashpw("password".encode('utf8'), bcrypt.gensalt()).decode("utf8")

class JsonWebToken:
	
	def _init_(self):
		self.secret_key = "asiufbwefv,nd askhfsafjiauyfawensydfgaiba sdfsbfhwe"

	def encryption(self, body={"name": "akash", "age": 25}):
		current_time = datetime.datetime.now()
		body['iat'] = current_time.timestamp()
		body['exp'] = (current_time + datetime.timedelta(seconds = 30)).timestamp()
		return jwt.encode(body, secret_key, algorithm='HS256').decode('utf-8')

	def decryption(self, token):
		options = {'verify_exp': True}
		return jwt.decode(token, secret_key, algorithms=['HS256'], options=options)

def password_varify(password, hashpw):
	print(password, hashpw)
	password = '{}'.format(password).encode('utf8')
	hashpw = '{}'.format(hashpw).encode('utf8')
	print(password)
	if bcrypt.checkpw(password, hashpw):
		return True
	else:
		return False

