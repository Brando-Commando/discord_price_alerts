''' 
This application is a Discord bot created to ping a user on updates to a price change of 
either a crypto currency, or of a share price. 

This process will include several phases described below. These will be rather small jumps in the scope of the project.

Phase A: Simply getting the bot online, and able to connect to a GUILD.
### Complete ###

Phase B: Implementing either an actual API or a webscraping API to gather data with a hardcoded currency to watch and monitor. 

Phase C: Work on taking user input on what to monitor, either through private messaging or a chat channel.

Phase D: Have user created parameters on either; the minimum percentage change for which to report, or specifiic USD values to initiate a ping.

Phase E: Allow more than one currency/stock to be monitored by the bot. Probably through either a private message or a ping with a specific phrase.

--- Optional Phases ---

Optional Phase A: Allow the bot to be set to work through private messages, a chat channel or both.

Optional Phase B: 


'''

import discord
import os
from dotenv import load_dotenv


# This helps grab data from the .env file.
load_dotenv()

# Attributes from the .env file.
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


    
    for guild in client.guilds:
        if guild.name == GUILD:
            break
        
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    

client.run(TOKEN)