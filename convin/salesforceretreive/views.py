from django.shortcuts import render
import requests
from django.views import View
# Create your views here.
from django.http import HttpResponse
from .models import SalesforceAuth,UserData

class CallErrors(Exception):
        pass

class UserAccessToken(View):
	def post(self,request):
		code=request.GET.get('code')
		user_id=request.GET.get('state')
		"""using state variable to know which
		   user is giving access to the app"""
		return self.authorize_token(code,user_id)
		#return self.fetch_user_data(user_id,{})
	def authorize_token(self,code,user_id):
		client_id="3MVG9fe4g9fhX0E47NvczVXrs0a9quX3L4.gzwMTDGQqbE8F7LSr1JKxt44bR2sRwKhBoMjr7e6d6BR38C5mw"
		client_secret="098CB0BE5E594FCED4332EA4C785A3656C510F9DF36E50552F4FDFEE3E2E354F"
		params={"client_id":client_id,
				"client_secret":client_secret,
				"grant_type":"authorization_code",
				"code":code,
				"redirect_uri":"https://convin.ai/"
				}
		url="https://login.salesforce.com/services/oauth2/token"
		response=requests.post(url,data=params)
		if(response.status_code==200):
			data=response.json()
			user_instance=SalesforceAuth(user_id=user_id,
					refresh_token=data['refresh_token'],
					access_token=data['access_token'])
			user_instance.save()
			self.fetch_user_data(user_id,data)
			return HttpResponse('ok',status=200)
		else:
			raise CallErrors(
				"Getting tokens unsuccesfull")

	def fetch_user_data(self,id,data):
		url='https://convin2-dev-ed.my.salesforce.com/services/data/v52.0/sobjects/'
		self.call_salesforce_api(url+'contact',id,data)
		self.call_salesforce_api(url+'account',id,data)
		self.call_salesforce_api(url+'user',id,data)
		return HttpResponse('ok')
	def call_salesforce_api(self,url,user_id,data):
		datas={"Content-Type":"application/json",
				"Authorization":'Bearer '+data['access_token']}
		response=requests.get(url,headers=datas)
		print(response.json())
		if(response.status_code==200):
			self.store_user_data(user_id,response.json())
		return HttpResponse('ok',status=200)

	def store_user_data(self,id,data):
		for row in data['recentItems']:
			info_type=row['attributes']['type']
			info_name=row['Name']
			user_data=UserData(user_id=id,data_type=info_type,name=info_name)
			user_data.save()
		return 0
	