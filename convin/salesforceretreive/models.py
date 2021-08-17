from django.db import models

# Create your models here.
class SalesforceAuth(models.Model):
	auth_id=models.AutoField(primary_key=True)
	user_id=models.IntegerField(blank=False)
	refresh_token=models.TextField(blank=False)
	access_token=models.TextField(blank=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class UserData(models.Model):
	Contact_id=models.AutoField(primary_key=True)
	user_id=models.IntegerField(blank=False)
	data_type=models.CharField(max_length=50)
	name=models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True)

