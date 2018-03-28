from mattermost_bot.bot import Bot, PluginsManager
from mattermost_bot.mattermost import MattermostClient
from mattermost_bot.dispatcher import MessageDispatcher
import mm_bot_settings as local_settings
import time

class MMBot(Bot):

    def __init__(self):
        self._client = MattermostClient(
            local_settings.BOT_URL, local_settings.BOT_TEAM,
            local_settings.BOT_LOGIN, local_settings.BOT_PASSWORD,
            local_settings.SSL_VERIFY
            )
        self._plugins = PluginsManager(local_settings.PLUGINS)
        self._dispatcher = MessageDispatcher(self._client, self._plugins)

    def _keep_active(self):
        while True:
            time.sleep(60)
            self._client.ping()
            self._client.online()

if __name__ == "__main__":
	bot = MMBot()
	bot.run()