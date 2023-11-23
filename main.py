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
    await log_channel.send(f"{member.display_name} joined the server")
    await member.send("Hi, I just noticed you joined our server. Here's a brief on the server rules.")
    await member.send(""" Rules of the server:
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
- Don’t ping without legitimate reasoning behind them.""")

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
  """CAUTION!! Clears all the chats in current channel. CAUTION!!"""
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
    await ctx.send(f"Hey there User! Please choose what you need help with:\n"
                   "1. About rotaract\n"
                   "2. About 3191\n"
                   "3. About District Structure\n")

    # Wait for the user's choice
    try:
        # print(type(ctx.message))
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
        await ctx.send("Rotaract, a global service organization for young adults aged 18 to 30, fosters leadership, fellowship, and community service. Affiliated with Rotary International, Rotaract clubs engage in local and international projects, emphasizing professional development and social responsibility while empowering individuals to create positive change in their communities worldwide.",ephemeral=True)
        # Implement logic for technical support inquiries
    elif choice == '2' or choice == 'about 3191':
        await ctx.send("There's plenty to talk about 3191, why not head over to our [website](https://rotaract3191.org/) for some in-depth knowledge?",ephemeral=True)
        # Implement logic for billing inquiries
    elif choice == '3' or choice == 'about district structure':
        await ctx.send("All Rotaract Districts are represented by their DRRs (District Rotaract representatives). Each DRR has his own team who are responsible for the various levels of management. In 3191, the DRR’s core committee consists of the DRR – Elect, District Rotaract Secretaries (DRS’s) for Administration, Training and Initiatives, and Operations, and the District Joint Secretary (DJS). The various avenues of service are headed by the respective Directors from the Executive Council and their teammates from the District Committee. The District itself is divided into 4 administrative zones, each headed by two Zonal Rotaract Representatives (ZRRs). These ZRRs are assigned as the administrators of the clubs under their zones, led by the respective club Presidents. Further hierarchies are decided by these presidents. ",ephemeral=True)
        # Implement logic for general inquiries
    else:
        await ctx.send("Invalid choice. Please choose a valid option (1, 2, or 3).",ephemeral=True)
        return

bot.run("")
