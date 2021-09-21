from os import environ as env
from pathlib import Path
from traceback import format_exc
from typing import List

from asyncpg import create_pool
from discord.ext.commands import Bot as _Bot
from loguru import logger


class Bot(_Bot):
    """A subclass of `discord.ext.commands.Bot` to add functionality."""

    def __init__(self, *args, **kwargs) -> None:
        super(Bot, self).__init__(*args, **kwargs)

        self.pool = None

    def load_extensions(self, exts: List[str]) -> None:
        ld = 0

        for ext in exts:
            try:
                self.load_extension(ext)
                logger.info(f"Successfully loaded extension {ext}")
                ld += 1
            except Exception as e:
                logger.error(
                    f"Error occurred while loading extension {ext}: {e}\n{format_exc()}"
                )

        logger.info(
            f"Extension loading complete. {ld} extensions loaded, {len(exts) - ld} failed."
        )

    async def on_ready(self) -> None:
        logger.info(f"Bot is ready. Connected to {len(self.guilds)} guilds.")

        self.dispatch("config_refresh")

    async def on_connect(self) -> None:
        logger.info("Bot is connected to the gateway.")

        self.pool = await create_pool(dsn=env["DB_URI"])

        await self.pool.execute(Path("src/data/init.sql").read_text())

        logger.info("Database connection established and set up.")
