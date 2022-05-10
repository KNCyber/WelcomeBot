import discord
import logging
from os import getenv


logging.basicConfig(level=logging.INFO)
client = discord.Client()
FLAG = getenv("FLAG")
TOKEN = getenv("TOKEN")
GUILD_ID = 746067092695941201
ROLE_ID = 973663565439467541
ADMIN_ID = 137662189891878913


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    print(client.guilds)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if not isinstance(message.channel, discord.DMChannel):
        return

    if FLAG not in message.content:
        logging.info("%s invalid flag (%s)", message.author.id, message.content)
        return await message.channel.send(f"It appears that the flag is not correct, try again?")

    guild = client.get_guild(GUILD_ID)
    role = guild.get_role(ROLE_ID)
    if not guild or not role:
        logging.warning("guild: %s, role: %s", guild, role)
        return await message.channel.send(f"Something horrible has happened. Please contact <@{ADMIN_ID}>")

    member = await guild.fetch_member(message.author.id)

    if not member:
        logging.info("%s sent flag, but is not in the guild", message.author.id)
        return await message.channel.send(f"It appears that you're not a member of KNCyber server.")

    logging.info("adding role to '%s'", message.author.id)
    await member.add_roles(role)
    await message.channel.send("Your flag seems to be correct! Welcome to KNCyber :)")


client.run(TOKEN)
