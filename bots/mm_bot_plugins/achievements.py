# -*- coding: utf-8 -*-

import re, json
import requests
from mattermost_bot.bot import listen_to
from mattermost_bot.bot import respond_to
from mattermost_bot.utils import allow_only_direct_message
from mm_bot_settings import AUTH_TOKEN, MA_SERVER_URL

@respond_to('.*', re.IGNORECASE)
@allow_only_direct_message()
def response_to_all(message):
    talk_to_me_mission(message)
    keyword_mission(message)

def talk_to_me_mission(message):
    # corresponding mission settings
    mission_key = '21df60eb-54ad-4f8b-a98c-dc44677d9299'
    mission_class_name = 'Mission'
    # get message content
    username = message.get_username()
    # try to get or create mission
    response = requests.post(MA_SERVER_URL+'/achievements/mission/create',
                             json={'username': username,
                                   'mission_key': mission_key,
                                   'mission_class_name': mission_class_name,
                                   'auth_token': AUTH_TOKEN})
    result = response.json()
    # update score
    if result['created'] is True or result['existed'] is True:
        mission_proxy_json = json.loads(result['mission_proxy'])
        response = requests.put(MA_SERVER_URL+'/achievements/mission/update',
                                json={'proxy_key': mission_proxy_json[0]['fields']['key'],
                                      'score': mission_proxy_json[0]['fields']['score']+1,
                                      'auth_token': AUTH_TOKEN})
        result = response.json()
        if result['badge'] is not None:
            message.reply(result['badge'])

def keyword_mission(message):
    # corresponding mission settings
    mission_key = 'be8a9564-4de3-4590-bb43-455b9b9aaeef'
    mission_class_name = 'KeywordMission'
    # get message content
    username = message.get_username()
    content = message.get_message()
    # try to get or create mission
    response = requests.post(MA_SERVER_URL+'/achievements/mission/create',
                             json={'username': username,
                                   'mission_key': mission_key,
                                   'mission_class_name': mission_class_name,
                                   'auth_token': AUTH_TOKEN})
    result = response.json()
    # update score
    if result['created'] is True or result['existed'] is True:
        # check if keyword match in content
        mission_json = json.loads(result['mission'])
        keyword = mission_json[0]['fields']['keyword']
        occurences = len(re.findall(keyword, content, re.IGNORECASE))
        mission_proxy_json = json.loads(result['mission_proxy'])
        # if yes, increase the score by occurences
        response = requests.put(MA_SERVER_URL+'/achievements/mission/update',
                                json={'proxy_key': mission_proxy_json[0]['fields']['key'],
                                      'score': mission_proxy_json[0]['fields']['score']+occurences,
                                      'auth_token': AUTH_TOKEN})
        result = response.json()
        if result['badge'] is not None:
            message.reply(result['badge'])
