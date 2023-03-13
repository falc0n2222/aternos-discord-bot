import discord
from discord.ext import commands
import os
import time
from python_aternos import Client, Lists

CHANNELID = 123456789 # CHANNELID.
DOMAIN = 'test123.aternos.me' # Put your domain here.
TOKEN = 'your discord bot token.' # Your discord bot token goes here.
intents = discord.Intents.all()
intents.message_content = True

client = commands.Bot(command_prefix='server ', intents=intents) ## You can change the prefix here
at = Client.from_credentials('your username', 'your password') # This is where you login with your aternos account (username and password)

servers = at.list_servers()

serv = None
for s in servers:
    if s.domain == DOMAIN: # Your Aternos Server IP goes here.
        serv = s

# Important check
if serv is None:
    print('The specified server was not found!') # If you didn't specify a correct Aternos Server IP.
    exit()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.command()
async def start(ctx):
    channel = client.get_channel(CHANNELID)
    serv.start()
    embed = Embed(title="Server Start", description="The server is starting. You will get an update when the server is online.", color=0x00ff00)
    await channel.send(embed=embed)

    while True:
        await asyncio.sleep(1) # wait for 1 second
        serv.fetch() # fetch server status
        if serv.status == "online":
            embed = Embed(title="Server Started", description="The server has been sucesfully started & you may join.", color=0x00ff00)
            await channel.send(embed=embed)
            break # exit loop once server is online

@client.command()
async def stop(ctx):
    channel = client.get_channel(CHANNELID)
    serv.stop()
    embed = Embed(title="Server Stop", description="The server is stopping. You will get an update when the server is offline.", color=0xff0000)
    await channel.send(embed=embed)

    while True:
        await asyncio.sleep(1) # wait for 1 second
        serv.fetch() # fetch server status
        if serv.status == "offline":
            embed = Embed(title="Server Stopped", description="The server has been sucesfully stopped.", color=0x00ff00)
            await channel.send(embed=embed)
            break # exit loop once server is online

@client.command()
async def whitelist(ctx, arg1):
    channel = client.get_channel(CHANNELID)
    whitelist = serv.players(Lists.whl)
    whitelist.add({arg1})
    embed = Embed(title="Whitelist", description=f"The user {arg1} has been successfully whitelisted.", color=0x00ff00)
    await channel.send(embed)

@client.command()
async def whitelist_remove(ctx, arg1):
    channel = client.get_channel(CHANNELID)
    whitelist = serv.players(Lists.whl)
    whitelist.remove({arg1})
    embed = Embed(title="Whitelist Removal", description=f"The user {arg1} has been removed from the whitelist.", color=0xff0000)
    await channel.send(embed=embed)

@client.command()
async def whitelisted(ctx):
    channel = client.get_channel(CHANNELID)
    whitelist = serv.players(Lists.whl)
    player_list = ", ".join(whitelist.list_players())
    embed = Embed(title="Whitelisted Players", description=f"The whitelisted people are: {player_list}", color=0xffff00)
    await channel.send(embed=embed)

@client.command()
async def ipban(ctx, arg1):
    channel = client.get_channel(CHANNELID)
    banlist = serv.players(Lists.ips)
    banlist.add({arg1})
    embed = Embed(title="IP Ban", description=f"The IP {arg1} has been successfully IP-banned. (Please note that an IP is required and not a player's username for an IP Ban)", color=0xff0000)
    await channel.send(embed=embed)

@client.command()
async def unbanip(ctx, arg1):
    channel = client.get_channel(CHANNELID)
    banlist = serv.players(Lists.ips)
    banlist.remove({arg1})
    embed = Embed(title="IP Unban", description=f"The IP {arg1} has been successfully unbanned.", color=0x00ff00)
    await channel.send(embed=embed)

@client.command()
async def ban(ctx, arg1):
    channel = client.get_channel(CHANNELID)
    banlist = serv.players(Lists.ban)
    banlist.add({arg1})
    embed = Embed(title="Ban", description=f"The user {arg1} has been successfully banned.", color=0xff0000)
    await channel.send(embed=embed)

@client.command()
async def unban(ctx, arg1):
    channel = client.get_channel(CHANNELID)
    banlist = serv.players(Lists.ban)
    banlist.remove({arg1})
    embed = Embed(title="Ban", description=f"The user {arg1} has been successfully unbanned.", color=0xff0000)
    await channel.send(embed=embed)

@client.command()
async def bans(ctx):
    channel = client.get_channel(CHANNELID)
    banlist = serv.players(Lists.ban)
    banlistips = serv.players(Lists.ips)
    ban_list = ", ".join(banlist.list_players()) # concatenate player list into string
    ban_listips = ", ".join(banlistips.list_players()) # concatenate player list into string

    embed = discord.Embed(title="Banned Users and IPs")
    embed.add_field(name="Banned Users", value=ban_list, inline=False)
    embed.add_field(name="Banned IPs", value=ban_listips, inline=False)

    await channel.send(embed=embed) # Send the embed to the channel

@client.command()
async def info(ctx):
    channel = client.get_channel(CHANNELID)
    servers = at.list_servers()

    serv = None
    for s in servers:
        if s.domain == DOMAIN:
            serv = s

            s.fetch()
            
            info = f"{s.address}"
            status = f"{s.status}"
            playercount = f"The amount of connected users are: {s.players_count}"
            ramusage = f"{s.ram}MB"
            version = f"{s.version}" + ", Software: " + s.software

            # Set the color of the embed based on the server's status
            if s.status == "online":
                color = 0x00ff00 # Green
            elif s.status == "offline":
                color = 0xff0000 # Red
            elif s.status == "loading":
                color = 0xffff00 # Yellow
            elif s.status == "starting":
                color = 0xffff00 # Yellow
            elif s.status == "saving":
                color = 0xffff00 # Yellow
            elif s.status == "stopping":
                color = 0xffff00 # Yellow

            # Create a new embed object
            embed = discord.Embed(title="Server Information", color=color)
            embed.add_field(name="IP & Port", value=info, inline=False)
            embed.add_field(name="Status", value=status, inline=False)
            embed.add_field(name="Player Count", value=playercount, inline=False)
            embed.add_field(name="RAM Available", value=ramusage, inline=False)
            embed.add_field(name="Version", value=version, inline=False)

            # Send the embed to the channel
            await channel.send(embed=embed)


client.run(TOKEN)
