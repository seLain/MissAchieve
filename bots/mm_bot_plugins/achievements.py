# -*- coding: utf-8 -*-

import re, json, inspect
import requests
from mattermost_bot.bot import listen_to
from mattermost_bot.bot import respond_to
from mattermost_bot.utils import allow_only_direct_message
from mm_bot_settings import AUTH_TOKEN, MA_SERVER_URL, PLUGIN_SETTINGS

@listen_to('.*', re.IGNORECASE)
def listen_to_all(message):
    talkman_mission(message)
    mentions_mission(message)

def talkman_mission(message):
    # corresponding mission settings
    mission_settings = PLUGIN_SETTINGS[inspect.stack()[0][3]]['missions']
    # get message content
    username = message.get_username()
    # try to get or create mission
    for key in mission_settings.keys():
        response = requests.post(MA_SERVER_URL+'/achievements/mission/create',
                                 json={'username': username,
                                       'mission_key': key,
                                       'mission_class_name': mission_settings[key],
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

def mentions_mission(message):
    # corresponding mission settings
    mission_settings = PLUGIN_SETTINGS[inspect.stack()[0][3]]['missions']
    # get message content
    username = message.get_username()
    mentions = len(message.get_mentions()) if message.get_mentions() is not None else 0
    # try to get or create mission
    for key in mission_settings.keys():
        response = requests.post(MA_SERVER_URL+'/achievements/mission/create',
                                 json={'username': username,
                                       'mission_key': key,
                                       'mission_class_name': mission_settings[key],
                                       'auth_token': AUTH_TOKEN})
        result = response.json()
        # update score
        if result['created'] is True or result['existed'] is True:
            mission_proxy_json = json.loads(result['mission_proxy'])
            response = requests.put(MA_SERVER_URL+'/achievements/mission/update',
                                    json={'proxy_key': mission_proxy_json[0]['fields']['key'],
                                          'score': mission_proxy_json[0]['fields']['score']+mentions,
                                          'auth_token': AUTH_TOKEN})
            result = response.json()
            if result['badge'] is not None:
                message.reply(result['badge'])

@respond_to('.*', re.IGNORECASE)
def response_to_all(message):
    talk_to_me_mission(message)
    keyword_mission(message)

def talk_to_me_mission(message):
    # corresponding mission settings
    mission_settings = PLUGIN_SETTINGS[inspect.stack()[0][3]]['missions']
    # get message content
    username = message.get_username()
    # try to get or create mission
    for key in mission_settings.keys():
        response = requests.post(MA_SERVER_URL+'/achievements/mission/create',
                                 json={'username': username,
                                       'mission_key': key,
                                       'mission_class_name': mission_settings[key],
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
    mission_settings = PLUGIN_SETTINGS[inspect.stack()[0][3]]['missions']
    # get message content
    username = message.get_username()
    content = message.get_message()
    # try to get or create mission
    for key in mission_settings.keys():
        response = requests.post(MA_SERVER_URL+'/achievements/mission/create',
                                 json={'username': username,
                                       'mission_key': key,
                                       'mission_class_name': mission_settings[key],
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

@respond_to('my badge', re.IGNORECASE)
def get_my_badges(message):
    # get message content
    username = message.get_username()
    # try to get badges
    response = requests.get(MA_SERVER_URL+'/achievements/badges',
                            json={'username': username,
                                  'auth_token': AUTH_TOKEN})
    result = response.json()
    # prepare reply message
    message.reply('\n'.join([badge['success_message'] for badge in result['badges']]))
