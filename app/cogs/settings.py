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

    # TODO: Change this to a env setting for staff roles.
    @commands.group(invoke_without_command=True)
    @commands.has_any_role(676592497249746954)
    async def membership(self, ctx):
        await ctx.reply("Parent command!")

    @membership.command()
    async def add(self, ctx, role=None, role2=None, role3=None):
        await ctx.reply(f"1: {role} 2: {role2} 3:{role3}")
        # r = await mongo.roles.intert_one()
    @membership.command()
    async def remove(self, ctx, role=None, role2=None, role3=None):
        await ctx.reply("Child command!")

    @membership.command()
    async def settings(self, ctx):
        await ctx.reply("Child command!")


    @membership.error
    async def membership_error(self, ctx, error):
        if isinstance(error, commands.MissingAnyRole):
            await ctx.reply("You do not have access to the command.")


def setup(bot: commands.Bot):
    bot.add_cog(Settings(bot))