# [ ]: Make a `!membership add <ROLE> <ROLE2> <ROLE3>` command to add a role to a membership plan.
# [ ]: Make a `!membership remove <ROLE> <ROLE2> <ROLE3>` command to remove a role from a membership plan.
# [ ]: Make a `!membership settings` command to specify individual settings for the added roles.
# [ ]: Make a `!api <SERVICE> <KEY>` command to add the API Key for each service.

import disnake
import asyncio

from bot import mongo
from disnake.ext import commands

class Settings(commands.Cog):
    """Creates the invite cog which contains core invitation generation & management functionality."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(description="Mongo Test")
    async def mongo(self, inter: disnake.ApplicationCommandInteraction):

        payload = {
            'cunt': 'cunt'
        }
        result = await mongo.settings.insert_one(payload)
        await inter.response.send_message(
            content= f'It worked. {result.inserted_id}',
            ephemeral= True
        )


def setup(bot: commands.Bot):
    bot.add_cog(Settings(bot))