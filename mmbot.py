#Class libraries

import discord
from ec2_metadata import ec2_metadata
import os

# Setting up events and print message for 
# when the bot is ready to start working.
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    print("Bot is ready and listening for commands.")

#Setting up bot for messages 
@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Ignore messages from the bot itself

    try:
        #Setting up bot to responde with "Hello!" when the bot recieves
        #the message "hello world."
        if message.content.lower() == "hello world":
            await message.channel.send("Hello!")

        # Setting up bot to provide server information when the command "tell me about my server!" is received.
        elif message.content.lower() == "tell me about my server!":
            try:
                info = (
                    f"**Server Info:**\n"
                    f"- **Public IP:** {ec2_metadata.public_ipv4 or 'Not Available'}\n"
                    f"- **Region:** {ec2_metadata.region or 'Not Available'}\n"
                    f"- **Availability Zone:** {ec2_metadata.availability_zone or 'Not Available'}"
                )
                await message.channel.send(info)
            except Exception as e:
                await message.channel.send(f"Error fetching server data: {e}")

        # Setting up a default response for unknown commands.
        else:
            await message.channel.send("Sorry, I don't understand that command.")
    except Exception as general_error:
        await message.channel.send(f"An error occurred: {general_error}")

# This code saves errors that occur in the Discord bot to a file. To help when debugging and monitoring the bot. 
@client.event
async def on_error(event, *args, **kwargs):
    with open("error.log", "a") as log_file:
        log_file.write(f"Error in {event}: {args}\n")

# This code checks for Discord bot token in the enviroment variables.
#It also provides an error message if the token is missing.
token = os.getenv('TOKEN')
if not token:
    print("Error: Discord bot token not found in environment variables.")
else:
    client.run(token)
