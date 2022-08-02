# [ ]: Make a `!membership add <ROLE> <ROLE2> <ROLE3>` command to add a role to a membership plan.
# [ ]: Make a `!membership remove <ROLE> <ROLE2> <ROLE3>` command to remove a role from a membership plan.
# [ ]: Make a `!membership settings` command to specify individual settings for the added roles.
# [ ]: Make a `!api <SERVICE> <KEY>` command to add the API Key for each service.
import disnake
import aiohttp
import base64
import asyncio

from bot import mongo
from disnake.ext import commands
from config import WHITELIST_API_KEY, WHITELIST_IP, WHITELIST_PORT

class Settings(commands.Cog):
    """Creates the invite cog which contains core invitation generation & management functionality."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        http = aiohttp.ClientSession()

    @commands.slash_command(description="Add/Remove a user to a membership plan.")
    @commands.has_role("Support")
    async def membership(self, inter: disnake.ApplicationCommandInteraction, username: str = commands.Param(description="This must be case-sensitive, otherwise it will not work."), duration: str = commands.Param(description="This should be formatted as +1 month(s) or +14 day(s)."), package: str = commands.Param(choices=["Survivor", "Bandit"], description="Which package should be given to them. If this is different to what they have already, it will reset their time.") ):
        """Add/Remove a user to a membership plan."""
        discordId = inter.author.id
        http = aiohttp.ClientSession()
        url = f"https://kofi.karna.ge/webhook.php?staffDiscordID={discordId}&targetKarnageName={username}&targetTimeLength={duration}&targetTierPackage={package}"

        async with http as session:
            async with session.get(url) as response:
                if response.status == 200:
                    await inter.response.send_message(
                        content = "The action was successful. Please double check <#935859459580899388> to ensure it was applied.",
                        ephemeral = True
                    )

    @commands.slash_command(description="Adds/Removes someone from accessing media libraries.")
    # TODO: Make these dynamic with the database called 'roles'.
    @commands.has_any_role('Support')
    async def whitelist(self, inter: disnake.ApplicationCommandInteraction, type: str = commands.Param(choices=["add", "remove"]), userid: str = commands.Param(name="userid"), access: str = commands.Param(choices=["shows", "livetv"])):
        """Creates an invite"""
        http = aiohttp.ClientSession()
        url = f"http://{WHITELIST_IP}:{WHITELIST_PORT}"
        if access == "shows":
            content = ["episode"]
        elif access == "livetv":
            content = ["tvchannel"]
        json = {"UserId": userid, "MediaTypes": content}
        headers = {
            "Authorization": "Basic " + base64.b64encode(
                f":{WHITELIST_API_KEY}".encode()
            ).decode()
        }

        if type == "add":
            async with http.post(url, json=json, headers=headers) as resp:
                if resp.status == 200:
                    await inter.response.send_message(
                        content = "Success.",
                        ephemeral = True
                    )
                else:
                    await inter.response.send_message(
                        content = f"There was an error: {resp.status}",
                        ephemeral = True
                    )
        elif type == "remove":
            async with http.delete(url, json=json, headers=headers) as resp:
                if resp.status == 200:
                    await inter.response.send_message(
                        content = "Success.",
                        ephemeral = True
                    )
                else:
                    await inter.response.send_message(
                        content = f"There was an error: {resp.status}",
                        ephemeral = True
                    )

        await http.close()

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