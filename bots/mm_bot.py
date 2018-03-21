from mattermost_bot.bot import Bot, PluginsManager
from mattermost_bot.mattermost import MattermostClient
from mattermost_bot.dispatcher import MessageDispatcher
import mm_bot_settings as local_settings

class MMBot(Bot):

    def __init__(self):
        self._client = MattermostClient(
            local_settings.BOT_URL, local_settings.BOT_TEAM,
            local_settings.BOT_LOGIN, local_settings.BOT_PASSWORD,
            local_settings.SSL_VERIFY
            )
        self._plugins = PluginsManager(local_settings.PLUGINS)
        self._dispatcher = MessageDispatcher(self._client, self._plugins)

if __name__ == "__main__":
	bot = MMBot()
	bot.run()