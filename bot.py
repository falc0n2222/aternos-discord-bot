# BOT MADE BY FALCON

import discord
from discord import app_commands
from discord.ext import commands
import os
import asyncio
from python_aternos import Client, Lists

atclient = Client()
aternos = atclient.account

# START OF CONFIG (CHANGE THESE NEXT VALUES ONLY)

GUILDID = 1255581836738826242  # YOUR GUILD ID
PERMISSION = 1261299621087678555 # ROLE ID FOR PERMISSIONS
TOKEN = 'discord bot token'  # Your discord bot token goes here.
atclient.login('username', 'password')  # This is where you login with your aternos account (username and password)

# END OF CONFIG (DON'T CHANGE ANY OF THE NEXT LINES IF YOU DON'T KNOW WHAT YOU'RE DOING)

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

servs = aternos.list_servers()
serv = servs[0]

# Check for any servers
if serv is None:
    print('No servers found!')
    exit()

# Error Handling
@tree.error
async def on_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    if isinstance(error, discord.app_commands.MissingRole):
        await interaction.response.send_message("You don't have permission to use this command!", ephemeral=True)
    else:
        await interaction.response.send_message("An error occurred: {}".format(error), ephemeral=True)


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILDID))
    print("Ready!")


@tree.command(
    name="start",
    description="Start the server",
    guild=discord.Object(id=GUILDID)
)
@discord.app_commands.checks.has_role(PERMISSION)
async def start(interaction: discord.Interaction):

    # Fetch the current server status
    serv.fetch()
    if serv.status == "online":
        embed = discord.Embed(title="Server is already running", description="The server is already running.", color=0xff0000)
        await interaction.response.send_message(embed=embed)
        return

    # Start if not already started
    serv.start()
    embed = discord.Embed(title="Server Start", description="The server is starting. You will get notified when the server is online.", color=0x00ff00)
    await interaction.response.defer()  # Defer the response
    await interaction.followup.send(embed=embed)  # Send the initial response

    while serv.status != "online":
        await asyncio.sleep(5)  # wait for 5 seconds
        serv.fetch()  # fetch server status

    embed = discord.Embed(title="Server Started", description="The server has been successfully started & you may join.", color=0x00ff00)
    await interaction.followup.send(embed=embed)  # Send a follow-up response when the server is online


@tree.command(
    name="stop",
    description="Stops the server",
    guild=discord.Object(id=GUILDID)
)
@discord.app_commands.checks.has_role(PERMISSION)
async def stop(interaction: discord.Interaction):
    serv.fetch()
    if serv.status == "offline":
        embed = discord.Embed(title="Server is already offline", description="The server is already offline/stopped.", color=0xff0000)
        await interaction.response.send_message(embed=embed)
        return

    serv.stop()
    embed = discord.Embed(title="Server Stop", description="The server is stopping. You will get notified when the server is offline.", color=0xff0000)
    await interaction.response.defer()  # Defer the response
    await interaction.followup.send(embed=embed)  # Send the initial response

    while serv.status != "offline":
        await asyncio.sleep(5)  # wait for 10 seconds
        serv.fetch()  # fetch server status

    embed = discord.Embed(title="Server Stopped", description="The server has been successfully stopped.", color=0x00ff00)
    await interaction.followup.send(embed=embed)
    
    
@tree.command(
    name="whitelisted",
    description="Get the list of whitelisted users",
    guild=discord.Object(id=GUILDID)
)
@discord.app_commands.checks.has_role(PERMISSION)
async def whitelisted(interaction: discord.Interaction):
    whitelist = serv.players(Lists.whl)
    player_list = ", ".join(whitelist.list_players())
    embed = discord.Embed(title="Whitelisted Players", description=f"The whitelisted users are: {player_list}", color=0xffff00)

    await interaction.response.send_message(embed=embed)
    

@tree.command(
    name="bans",
    description="Lists all server bans",
    guild=discord.Object(id=GUILDID)
)
@discord.app_commands.checks.has_role(PERMISSION)
async def bans(interaction: discord.Interaction):
    banlist = serv.players(Lists.ban)
    banlistips = serv.players(Lists.ips)
    ban_list = ", ".join(banlist.list_players())  # concatenate player list into string
    ban_listips = ", ".join(banlistips.list_players())  # concatenate player list into string

    embed = discord.Embed(title="Banned Users and IPs")
    embed.add_field(name="Banned Users", value=ban_list, inline=False)
    embed.add_field(name="Banned IPs", value=ban_listips, inline=False)

    await interaction.response.send_message(embed=embed)
    

@tree.command(
    name="info",
    description="Fetches the Server's current Status.",
    guild=discord.Object(id=GUILDID)
)
async def info(interaction: discord.Interaction):
    serv.fetch()
    
    info = f"{serv.address}"
    status = f"{serv.status}"
    playercount = f"There are currently {serv.players_count} players online"
    ramusage = f"{serv.ram}MB"
    version = f"{serv.version}" + ", Software: " + serv.software

    # Set the color of the embed based on the server's status
    status_colors = {
        "online": 0x00ff00,
        "offline": 0xff0000,
        "loading": 0xffff00,
        "starting": 0xffff00,
        "saving": 0xffff00,
        "stopping": 0xffff00
    }
    color = status_colors.get(serv.status, 0x000000)  # Default to black if status is unknown so that we don't get an error or smth

    # Create a new embed object
    embed = discord.Embed(title="Server Information", color=color)
    embed.add_field(name="IP & Port", value=info, inline=False)
    embed.add_field(name="Status", value=status, inline=False)
    embed.add_field(name="Player Count", value=playercount, inline=False)
    embed.add_field(name="RAM Available", value=ramusage, inline=False)
    embed.add_field(name="Version", value=version, inline=False)

    # Send the embed to the channel
    await interaction.response.send_message(embed=embed)

client.run(TOKEN)
