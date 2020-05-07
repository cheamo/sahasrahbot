import asyncio

from alttprbot.util import orm
from config import Config as c
from alttprbot_discord.bot import discordbot
from alttprbot_api.api import sahasrahbotapi

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
#    loop.create_task(orm.create_pool(loop))
    loop.create_task(discordbot.start(c.DISCORD_TOKEN))
    loop.create_task(sahasrahbotapi.run(host='127.0.0.1', port=5001, use_reloader=False, loop=loop))
    loop.run_forever()
