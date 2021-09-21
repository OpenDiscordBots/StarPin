from discord import TextChannel
from discord.ext.commands import Cog, Context, command, has_guild_permissions
from emoji import emoji_count

from src.bot import Bot


class Config(Cog):
    """A cog to configure StarPins."""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @command(name="setup")
    @has_guild_permissions(manage_guild=True)
    async def setup(self, ctx: Context, channel: TextChannel = None, emoji: str = "⭐", count: int = 5) -> None:
        """Set up a starboard for a given channel, or the current channel."""

        if len(emoji) != 1 or emoji_count(emoji) != 1:
            await ctx.reply("You must provide a valid unicode emoji, or leave it as the default.")
            return

        channel = channel or ctx.channel

        await self.bot.pool.execute("""
            INSERT INTO Starboards VALUES ($1, $2, $3)
            ON CONFLICT (channel_id) DO UPDATE SET
            emoji = $2, required_stars = $3;
        """, channel.id, emoji, count)

        await ctx.send(f"Starboard created or updated with emoji {emoji}, requiring {count} reactions in #{channel.name}.")

        self.bot.dispatch("config_refresh")

    @command(name="remove")
    @has_guild_permissions(manage_guild=True)
    async def remove(self, ctx: Context, channel: TextChannel = None) -> None:
        """Remove a starboard for a given channel, or the current channel."""

        channel = channel or ctx.channel

        await self.bot.pool.execute("DELETE FROM Starboards WHERE channel_id = $1;", channel.id)

        await ctx.send(f"Starboard removed for #{channel.name}")

        self.bot.dispatch("config_refresh")


def setup(bot: Bot) -> None:
    bot.add_cog(Config(bot))
