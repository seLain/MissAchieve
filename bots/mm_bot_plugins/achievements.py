# -*- coding: utf-8 -*-

import re
import requests
from mattermost_bot.bot import listen_to
from mattermost_bot.bot import respond_to
from mattermost_bot.utils import allow_only_direct_message
from mm_bot_settings import AUTH_TOKEN, MA_SERVER_URL

@respond_to('(.*)', re.IGNORECASE)
@allow_only_direct_message()
def talk_to_me_mission(message, content):
    username = message.get_username()
    mission_key = 'c0faa0ed-d300-46b5-9b35-0fe522bc7d8d'
    # try to get or create mission
    response = requests.post(MA_SERVER_URL+'/achievements/mission/create',
                             json={'username': username,
                                   'mission_key': mission_key,
                                   'auth_token': AUTH_TOKEN})
    result = response.json()
    # update score
    if result['created'] is True or result['existed'] is True:
        response = requests.put(MA_SERVER_URL+'/achievements/mission/update',
                                json={'proxy_key': result['proxy_key'],
                                      'score': result['score']+1,
                                      'auth_token': AUTH_TOKEN})
        result = response.json()
        if result['badge'] is not None:
            message.reply(result['badge'])
