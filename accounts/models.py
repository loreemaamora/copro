# accounts/models.py
# ----

from authemail.models import EmailUserManager, EmailAbstractUser

class MyUser(EmailAbstractUser):
	# Custom fields


	# Required
	objects = EmailUserManager()
