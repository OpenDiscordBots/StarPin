from discord import RawReactionActionEvent
from discord.utils import find
from discord.ext.commands import Cog
from loguru import logger

from src.bot import Bot


class Starboard(Cog):
    """The core listener cog for StarPins."""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.boards = {}

    @Cog.listener()
    async def on_config_refresh(self) -> None:
        self.boards = {}

        channels = await self.bot.pool.fetch("SELECT * FROM Starboards;")

        for channel in channels:
            self.boards[channel["channel_id"]] = {
                "emoji": channel["emoji"],
                "count": channel["required_stars"],
            }

        logger.info(f"Refreshed boards.")

    @Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent) -> None:
        if payload.channel_id not in self.boards:
            return

        config = self.boards[payload.channel_id]

        if str(payload.emoji) != config["emoji"]:
            return

        channel = self.bot.get_channel(payload.channel_id)

        sbm = await self.bot.pool.fetchval("SELECT * FROM StarboardMessages WHERE id = $1;", payload.message_id)

        if sbm:
            return

        message = await channel.fetch_message(payload.message_id)

        reactions = find(lambda r: str(r.emoji) == config["emoji"], message.reactions)
        if not reactions:
            return

        if reactions.count >= config["count"]:
            logger.info("pinning")
            pins = await channel.pins()

            if len(pins) == 50:
                await pins[-1].unpin()

            await message.pin()
            logger.info("pinned")


def setup(bot: Bot) -> None:
    bot.add_cog(Starboard(bot))
