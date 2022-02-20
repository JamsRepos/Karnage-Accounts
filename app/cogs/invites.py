import disnake
from datetime import datetime, timedelta
import time

from bot import mongo
from config import MEMBERSHIP_ROLES
from utlity import callJfaApi, readTemplate
from disnake import Member
from disnake.ext import commands

class Invites(commands.Cog):
    """Creates the invite cog which contains core invitation generation & management functionality."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_member_update(self, before: Member, after: Member) -> None:
        """Listens to see if there are any role updates on a member in the guild."""

        if before.roles == after.roles:
            return

        # Check to see if the new role is a membership role.
        if len(before.roles) < len(after.roles):
            newRole = next(role for role in after.roles if role not in before.roles)

            if str(newRole.id) in MEMBERSHIP_ROLES:
                today = datetime.now()
                today = int(time.mktime(today.timetuple())) # Formats to UNIX.

                expire = datetime.now() + timedelta(days=31)
                expire = int(time.mktime(expire.timetuple())) # Formats to UNIX.

                userExist = await mongo.user.find_one({
                    "discord_id": after.id
                })

                if not userExist:
                    await mongo.user.insert_one({
                        "discord_id": after.id,
                        "role_id": newRole.id,
                        "purchase_date": today,
                        "invite_reset": expire,
                        "total_invites": 0,
                        "invites_used": 0,
                        "invited": []
                    })
                else:
                    filter = {
                        "discord_id": userExist["discord_id"]
                    }
                    values = {
                        "$set":
                        {
                            "role_id": newRole.id,
                            "purchase_date": today,
                            "invite_reset": expire,
                        }
                    }
                    await mongo.user.update_one(filter, values)

        # Check to see if the old role is a membership role.
        else:
            oldRole = next(role for role in before.roles if role not in after.roles)

            if str(oldRole.id) in MEMBERSHIP_ROLES:
                userExist = await mongo.user.find_one({
                "discord_id": after.id
                })

                filter = {
                    "discord_id": userExist["discord_id"]
                }

                values = {

                    "$set":
                    {
                        "role_id": 0,
                        "purchase_date": 0,
                        "invite_reset": 0,
                        "invites_used": 0,
                    },
                }
                await mongo.user.update_one(filter, values)



    @commands.slash_command(description="Sends an invite to the target User.")
    # TODO: Make these dynamic with the database called 'roles'.
    @commands.has_any_role("./ developer")
    async def invite(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User):
        """Creates an invite"""

        callerName = str(inter.user)
        callerId = inter.user.id
        targetName = str(user)
        fetch = await mongo.user.find_one({
            "discord_id": callerId
        })
        callerCount = fetch["total_invites"]

        # TODO: Change this to a database called `roles` which can be updated via an admin command.
        if fetch["invites_used"] <= 3:
            # TODO: Figure out a way to make the expiry date actually work properly.
            data = await readTemplate(template="invite")
            data["send-to"] = targetName
            data["label"] = "Invite For: " + targetName + " | Invited By: " + callerName

            headers = {
                "Content-Type": "application/json",
                "accept": "application/json",
            }

            response = await callJfaApi(endpoint="invites", type="post", header=headers, body=data)
            if response.status == 200:
                await inter.response.send_message(
                    content = f"Invite created & private messaged to {targetName}!",
                    ephemeral = True
                )

                filter = {
                    "discord_id": fetch["discord_id"]
                }

                values = {
                    "$set":
                    {
                        "total_invites": callerCount + 1,
                        "invites_used": callerCount + 1,
                    },
                    "$push":
                    {
                        "invited": user.id
                    }
                }

                await mongo.user.update_one(filter, values)
            else:
                await inter.response.send_message(
                    content = f"Invite creation failed! ``Error code: http-{response.status}``",
                    ephemeral = True
                )
        else:
            await inter.response.send_message(
                content = f"You have reached your limit for this month!",
                ephemeral = True
            )

    @invite.error
    async def invite_error(self, inter: disnake.ApplicationCommandInteraction, error):
        if isinstance(error, commands.MissingAnyRole):
            await inter.response.send_message(
                content = "You do not have an active subscription. \nVisit https://pay.karna.ge/ to use this command.",
                ephemeral = True
            )



def setup(bot: commands.Bot):
    bot.add_cog(Invites(bot))
