import disnake
import json
from datetime import datetime, timedelta
import time

from bot import mongo
from config import GUILD_ID, MEMBERSHIP_ROLES
from utlity import callJfaApi, readTemplate
from disnake import Member
from disnake.ext import commands

class Invites(commands.Cog):
    """This will be for a ping command."""

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

                user = mongo.user.find_one({
                    "discord_id": after.id
                })
                if not user:
                    mongo.user.insert_one({
                        "discord_id": after.id,
                        "role_id": newRole.id,
                        "purchase_date": today,
                        "invite_reset": expire,
                        "total_invites": 0,
                        "invites_used": 0,
                        "invited": []
                    })

        # Check to see if the old role is a membership role.
        if len(before.roles) > len(after.roles):
            oldRole = next(role for role in before.roles if role not in after.roles)

            if str(oldRole.id) in MEMBERSHIP_ROLES:
                print('role removed')
                # TODO: Add the logic for when the role is removed such as removing role_id, purchase_date, invite_reset, invites_used.



    @commands.slash_command(description="Sends an invite to the target User.")
    async def invite(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User):
        """Creates an invite"""

        callerName = str(inter.user)
        callerId = inter.user.id
        targetName = str(user)
        fetch = mongo.user.find_one({
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

            response, code = await callJfaApi(endpoint="invites", type="post", header=headers, body=data)
            if code == 200:
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

                mongo.user.update_one(filter, values)
            else:
                await inter.response.send_message(
                    content = f"Invite creation failed! ``Error code: http-{code}``",
                    ephemeral = True
                )
        else:
            await inter.response.send_message(
                content = f"You have reached your limit for this month!",
                ephemeral = True
            )




def setup(bot: commands.Bot):
    bot.add_cog(Invites(bot))
