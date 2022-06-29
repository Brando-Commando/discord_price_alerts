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

import os
from dotenv import load_dotenv
from discord.ext import commands
from numpy import true_divide
import asyncio
import yfinance as yahooFinance
import traceback



# This helps grab data from the .env file.
load_dotenv()

# Attributes from the .env file.
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


# Prefix the bot will need to recognize commands
bot = commands.Bot(command_prefix='-')

# on_ready(): means on bot startup and connection

############################
####### BOT COMMANDS #######
############################


############################
# PRICE CHECK COMMAND
############################

# This command will be structured like "-check Bitcoin" and will return a price.
@bot.command(name='check', help='This checks the current price of a security. Use the symbol (TSLA, AAPL) for a crypto, use symbol and end with -USD (BTC-USD, MANA-USD).')
async def response(ctx, search_name):

    # Tickers are a value of the stock symbol, so TSLA, AAPL, etc is a ticker.
    try: 
        ticker = yahooFinance.Ticker(search_name)
        current_data = ticker.history(period='id')
        # Rounds to two decimal places
        current_data = round(current_data['Close'][0], 3)
        # Adds comma to help format the number
        current_data = ('{:,}'.format(current_data))

        # Return message
        # message = (search_name + " has been last reported at $" + str(current_data))
        message = ("```bash\n" + ' "' + search_name + " has been last reported at $ " + str(current_data) + '"' + ' ```')

        await ctx.send(message)


    # Error message
    except: 
        await ctx.send("That was not a valid security/crypto, for a security use their symbol, for crypto end with -USD.")





############################
# ASSIGN COMMAND
############################

# This command is to assign a stock or crypto to be monitored
@bot.command(name='assign', help='This will assign a security/crypto to a time based alert. EX: -assign AAPL 1 minute, or -assign AAPL 1 hour')
async def response(ctx, search_name, time_delay: int, time_delay_type):

    try:
        ticker = yahooFinance.Ticker(search_name)

            # Time_delay = integer, time_delay_type = minutes or hour
            
        #    if time_delay_type == "hour" or "hours":
        #        delay_type = 3600


        # an hour equals 3600 seconds
        if time_delay_type in ("hour", "hours"):
            delay_type = 3600

        #    elif time_delay_type == "minute" or "minutes":
        #        delay_type = 60

        # a minute equals 60 seconds
        elif time_delay_type in ("minute", "minutes"):
            delay_type = 60
                
            
        else: 
            await ctx.send("That was not a valid measure of time.")

        reminder_message = ("We will update you every " + str(time_delay) + " " + time_delay_type)
        await ctx.send(reminder_message)


        while True:
            current_data = ticker.history(period='id')
            # Rounds to two decimal places
            current_data = round(current_data['Close'][0], 3)
            # Adds comma to help format the number
            current_data = ('{:,}'.format(current_data))


            # the ```bash\n is what formats the text into cyan and a codeblock, the extra " is needed to format text. 
            # color formatted text is used in the following format in one message:
                # ```bash 
                #   "test message"
                # ```
            # this is recreating the format in text.
            message = ("```bash\n" + ' "' + search_name + " has been last reported at $ " + str(current_data) + '"' + ' ```')
            await ctx.send(message)


            # Time delay function
            # asyncio allows other processes to run as normal while time halts the entire program,
            # I am not sure if asyncio is needed with discord but I havent tested this with just time.
            # This statement uses the string for data type turned into the integer delay type, multiplied by the 
            # stated time_delay
            await asyncio.sleep(time_delay * delay_type)

        

    # This is a catch all except, an error is ran everytime the -assign command is used. 
    # traceback.print_exec() prints the error traceback into the terminal. This can also be used to export all error
    # messages into a database or other external format. 
    except:    
        await ctx.send("That was not a valid security/crypto, for a security use their symbol, for crypto end with -USD.")
        traceback.print_exc()



############################
# 
############################


# Bot token required for start.
bot.run(TOKEN)