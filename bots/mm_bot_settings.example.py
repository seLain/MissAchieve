'''
Mattermost settings
'''
PLUGINS = [
    'mm_bot_plugins'
]

BOT_URL = 'http://mm.example.com/api/v3'
BOT_LOGIN = 'bot@example.com'
BOT_PASSWORD = None
BOT_TEAM = 'devops'
SSL_VERIFY = True

'''
MissAchieve settings
'''
AUTH_TOKEN = ''
MA_SERVER_URL = ''

'''
Plugin Settings
'''
PLUGIN_SETTINGS = {
	'PLUGIN_FUNCTION_NAME': {
		'missions': {
			'MISSION_INSTANCE_KEY': 'MISSION_CLASS_NAME',
			'MISSION_INSTANCE_KEY': 'MISSION_CLASS_NAME'
		}
	},
}