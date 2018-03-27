from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib import auth
from django.contrib.auth.models import User
import json
from .models import Mission, MissionProxy

def auth_token_validated(request):
	try:
		return True if Token.objects.get(
			key=json.loads(request.body.decode('utf-8'))['auth_token']) else False
	except Token.DoesNotExist:
		return False
	except KeyError:
		return False

@api_view(['POST'])
def create_mission(request):

	# check auth token
	if not auth_token_validated(request):
		return HttpResponseBadRequest("Not valid access.")

	args = {'username':'',
			'mission_name':'',
			'mission_key':'',
			'score': 0,
			'created': False,
			'existed': False}

	try:
		json_data = json.loads(request.body.decode('utf-8'))
		username = json_data['username']
		mission_key = json_data['mission_key']
		# get or create user
		user, created = User.objects.get_or_create(username=username,
										  		   password=username) # [TODO] the password gen algo.
		# get mission
		mission, created = Mission.objects.get_or_create(key=mission_key)
		# get or create mission proxy
		mission_proxy, created = MissionProxy.objects.get_or_create(owner=user, mission=mission)
		# prepare and return mission info
		args['username'] = user.username
		args['mission_name'] = mission.name
		args['mission_key'] = mission.key
		args['proxy_key'] = mission_proxy.key
		args['score'] = mission_proxy.score
		args['created'] = created
		args['existed'] = not created
		return JsonResponse(args)
	except ValueError:
		return HttpResponseBadRequest("Not valid json data")
	except KeyError as error:
		return HttpResponseBadRequest("Required key not found in json data : %s" % str(error))

@api_view(['GET'])
def get_mission(request):
	pass

@api_view(['PUT'])
def update_mission(request):

	# check auth token
	if not auth_token_validated(request):
		return HttpResponseBadRequest("Not valid access.")

	args = {'badge': None}

	try:
		json_data = json.loads(request.body.decode('utf-8'))
		proxy_key = json_data['proxy_key']
		score = json_data['score']
		mission_proxy = MissionProxy.objects.get(key=proxy_key)
		mission_proxy.score = score
		mission_proxy.save()
		if mission_proxy.evaluate():
			args['badge'] = mission_proxy.mission.success_message
		return JsonResponse(args)
	except Mission.DoesNotExist:
		pass

@api_view(['DELETE'])
def delete_mission(request):
	pass