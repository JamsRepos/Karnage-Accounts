# [ ]: Make a `!membership add <ROLE> <ROLE2> <ROLE3>` command to add a role to a membership plan.
# [ ]: Make a `!membership remove <ROLE> <ROLE2> <ROLE3>` command to remove a role from a membership plan.
# [ ]: Make a `!membership settings` command to specify individual settings for the added roles.
# [ ]: Make a `!api <SERVICE> <KEY>` command to add the API Key for each service.
import disnake

from bot import mongo
from disnake.ext import commands

class Settings(commands.Cog):
    """Creates the invite cog which contains core invitation generation & management functionality."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(description="Adds/Removes someone from accessing media libraries.")
    # TODO: Make these dynamic with the database called 'roles'.
    @commands.has_any_role('Infected')
    async def whitelist(self, inter: disnake.ApplicationCommandInteraction, userid: str):
        """Creates an invite"""

    @whitelist.error
    async def whitelist_error(self, inter: disnake.ApplicationCommandInteraction, error):
        if isinstance(error, commands.MissingAnyRole):
            await inter.response.send_message(
                content = "You do not have permission to run this command.",
                ephemeral = True
            )
        raise error


def setup(bot: commands.Bot):
    bot.add_cog(Settings(bot))