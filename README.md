## BE AWARE THAT PERMISSIONS ARE NOT SET-UP ANYONE WILL BE ABLE TO USE THE COMMANDS AND DO HARM. THIS IS TO SEMI-PREVENT THE USAGE OF THIS BOT IN A PUBLIC GUILD. USE ONLY IN A PRIVATE SERVER!!! ##

## THIS BREAKS ATERNOS'S TOS, USE AT YOUR OWN RISK ##

# ATERNOS DISCORD BOT
Ban, Whitelist, Start, Stop, Show information about your Aternos server &amp; etc, all available thru a simple Discord bot.

Credits to
Python-Aternos. // https://pypi.org/project/python-aternos/ // for the API itself.

## How to use the Bot ##

Start off by putting your Channel ID Where specified, put your server address where the "DOMAIN = " part is, put your discord bot token where the "TOKEN = " part is.

To input your Aternos username and password head over to line 14 and put your username where it says "your username" and your password where it says "your password".

After this is done go into cmd and type

"pip install python-aternos" then "pip install discord" without the "" ofc.

## How to change Prefix ##
You can change the prefix by going to line 13 and looking for this line
"command_prefix='server '" from here change "server" to your new desired prefix.

## Commands list ##

"start" Pretty self explanatory.

"stop" Pretty self explanatory.

"info" Shows information about your server. 

"whitelist" Adds someone to the whitelist. Usage: server whitelist username

"whitelist-remove" Removes someone from the whitelist. Usage: server whitelist-remove username

"whitelisted" Shows people that are whitelisted. 

"ipban" IP ban's a specific IP. Usage: server ipban put.an.ip.address.here (MUST BE A IP AND NOT A USERNAME!!!).

"unbanip" Unban's a specific IP. Usage: server unbanip put.an.ip.address.here.

"ban" Bans a specific player. Usage: server ban username.

"unban" Unban's a specific IP. Usage: server unban username.

"bans" Show's the ban list. 

This was written in like a day and a half. So excuse the horrible code & bad documentation.
