from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib import auth
from django.contrib.auth.models import User
from django.core import serializers
import json
from .models import Mission, MissionProxy
import importlib

def index(request):
	all_missions = [{'mission': m.name,
					 'content': m.content,
					 'desired_score': m.desired_score
					} for m in Mission.objects.all()]
	achieved_missions = [{'username': m.owner.username,
						  'mission': m.mission.name,
						  'message': m.mission.success_message,
						  #'date': m.achieved_date,
						  } for m in MissionProxy.objects.filter(achieved=True)]
	return render(request, 'achievements/index.html',
				  {'all_missions': all_missions,
				   'achieved_missions': achieved_missions})

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
		mission_class_name = json_data['mission_class_name']
		mission_module_name = 'achievements.models' # fixed paramter
		# get or create user
		user, created = User.objects.get_or_create(username=username,
										  		   password=username) # [TODO] the password gen algo.
		# get or create mission dynamically based on given mission class name
		# mechanism designed specifically for extendability of mission classes in models
		mission_module = importlib.import_module(mission_module_name)
		mission_class = getattr(mission_module, mission_class_name)
		mission, created = mission_class.objects.get_or_create(key=mission_key)
		# get or create mission proxy
		mission_proxy, created = MissionProxy.objects.get_or_create(owner=user, mission=mission)
		# prepare and return mission info
		args['username'] = user.username
		args['mission'] = serializers.serialize("json", [mission])
		args['mission_proxy'] = serializers.serialize("json", [mission_proxy])
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

@api_view(['GET'])
def get_badges(request):

	# check auth token
	if not auth_token_validated(request):
		return HttpResponseBadRequest("Not valid access.")

	args = {'badges': []} # [{'success_message':'xxx'}, ]

	try:
		json_data = json.loads(request.body.decode('utf-8'))
		user = User.objects.get(username=json_data['username'])
		achieved = MissionProxy.objects.filter(owner=user, achieved=True)
		for proxy in achieved:
			args['badges'].append({'success_message': proxy.mission.success_message})
		return JsonResponse(args)
	except ValueError:
		return HttpResponseBadRequest("Not valid json data")
	except User.DoesNotExist:
		return HttpResponseBadRequest("Not valid user")
	except MissionProxy.DoesNotExist:
		return JsonResponse(args)