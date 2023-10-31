import nextcord
import json
import asyncio
from nextcord import Interaction, SlashOption
from nextcord.ext import commands

with open("config.json", mode="r") as config_file:
    config = json.load(config_file)

NSFWWORDS = config["swearing"]

intents = nextcord.Intents.default()
intents = nextcord.Intents().all()

bot = commands.Bot(command_prefix="!",intents=intents)

logging=True
logschannel = config["logchannel"]

async def validateNSFW(message):
        for i in message.content.split():
            if i in NSFWWORDS:
                message=f"*WARNING ISSUED* to {message.author.name} for abusive language ||{i}||"
                await bot.get_channel(logschannel).send(message)

async def validateUsername(member):
    new_guild = bot.get_guild(config["guild_id"])
    role = new_guild.get_role(config["transgressor"])
    for i in NSFWWORDS:
        if i in member.display_name:
            await member.add_roles(role)
            break
    else:
        await member.remove_roles(role)

@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready!")

@bot.event
async def on_message(message):
    if message.channel.id != logschannel:
        # print(f"{message.author.name}: {message.content}")
        await validateNSFW(message)
        await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    log_channel = bot.get_channel(logschannel)
    await validateUsername(member)
    await log_channel.send(f"DisplayName: {member.display_name} joined the server")
    await member.send("Hi, I just noticed you joined our server. Here's a brief on teh server rules.")

@bot.event
async def on_member_update(before, after):
    log_channel = bot.get_channel(logschannel)
    if (before.display_name != after.display_name):
        await validateUsername(after)
        await log_channel.send(f"Member {before.display_name} updated their nickname to {after.display_name}")

# @bot.slash_command(name='set_log_channel')
# async def set_log_channel(ctx,chl:str):
#     """Set the channel for the bot to report its logs to"""
#     global logschannel
#     with open("config.json", mode="w") as config_file:
#         config_file["logchannel"]=chl
#     logschannel=chl
#     ctx.send("Log channel updated")

@bot.slash_command(name="clearchat")
async def clear(ctx):
  """CAUTION!! Clears all the chats in current channel CAUTION!!"""
  await ctx.channel.purge()
  await ctx.send("Channel cleared.")

@bot.slash_command(name="rules")
async def rules(ctx):
  """Displays the server rules."""
  await ctx.send(""" Rules of the server:
- Be respectful, civil, and welcoming.
- No inappropriate or unsafe content.
- Do not misuse or spam any of the channels.
- No self-promotion, soliciting, or advertising.
- NSFW content is not allowed.
- Do not buy, sell, trade, or give away anything.
- Do not use the server as a dating site.
- Please communicate in English only.
- Discord names and avatars must be appropriate.
- Spamming in any form is not allowed.
- Controversial topics like religion and politics are not allowed.
- Do not attempt to bypass any blocked words.
- Don’t ping without legitimate reasoning behind them.""", ephemeral=True)

@bot.slash_command(name="hello")
async def hello(ctx):
    """For any kind of rotaract assitance that you might need. """
    await ctx.send(f"Hey there User! Please choose a what you need help with:\n"
                   "1. About rotaract\n"
                   "2. About 3191\n"
                   "3. About District Structure\n"
                   "4. Details about my club")

    # Wait for the user's choice
    try:
        print(type(ctx.message))
        response = await bot.wait_for(
            'message',
            # check=lambda message: message.author == ctx.author and message.channel == ctx.channel,
            check=lambda message: True and message.channel == ctx.channel,
            timeout=50  # Adjust the timeout as needed
        )
    except asyncio.TimeoutError:
        await ctx.send("You took too long to make a choice. Please start over.",ephemeral=True)
        return

    # Process the user's choice
    choice = response.content.lower()
    if choice == '1' or choice == 'about rotaract':
        await ctx.send("Some brief info about Rotaract and rotary. might possiblly span 10-15 lines.",ephemeral=True)
        # Implement logic for technical support inquiries
    elif choice == '2' or choice == 'about 3191':
        await ctx.send("Some brief info about RID3191. DRR info, zones etc.",ephemeral=True)
        # Implement logic for billing inquiries
    elif choice == '3' or choice == 'about district structure':
        await ctx.send("Administrative heirarchy. List of facilitators. District roles etc.",ephemeral=True)
        # Implement logic for general inquiries
    elif choice == '4' or choice == 'details about my club':
        await ctx.send("further branching",ephemeral=True)
        # Implement logic for general inquiries
    else:
        await ctx.send("Invalid choice. Please choose a valid option (1, 2, or 3).",ephemeral=True)
        return


bot.run("${{secrets.YOUR_SECRET_NAME}}")
