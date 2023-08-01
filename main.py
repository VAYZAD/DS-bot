import discord
import json
import datetime
import discord.ui
import os
import random
from discord.ext import commands
from discord.ui import View, Button, Select


# for token
file = open ('config.json', 'r') 
config = json.load(file)

# /
bot = commands.Bot(command_prefix=config['prefix'], intents=discord.Intents.all())

# remove basic command help
bot.remove_command("help")


# run
@bot.event 
async def on_ready():
    print('BOT ONLINE')


# /hi
@bot.command(name='hi')
async def ping(ctx):
    await ctx.send(f'{ctx.author.mention} Hi!')


# /title 
@bot.command(name="title")
async def ping(ctx: commands.context, *, args):
    result = str(args)
    await ctx.send(embed=discord. Embed(title=f'{result}', color=0x64ff8a))


# /ban
@bot.command()
@commands.has_any_role("Moderator", "Administrator", "Owner")
async def ban(ctx, member:discord.member, *, reason):
    if reason == None:
        reason = "This user is banned by" + ctx.message.author.name 
    await member.ban(reason=reason)
    await ctx.send(f"***{member.name} was banned***")
    modlogs = bot.get_channel(1135308337437749380)
    await ctx.send(f"{member.name} was just banned, they were banned by {ctx.message.author.name}")


# /kick
@bot.command()
@commands.has_any_role("Moderator", "Administrator", "Owner")
async def kick(ctx, member:discord.member, *, reason):
    if reason == None:
        reason = "This user is kicked by" + ctx.message.author.name 
    await member.kick(reason=reason)
    await ctx.send(f"***{member.name} was kicked***")
    modlogs = bot.get_channel(1135308337437749380)
    await ctx.send(f"{member.name} was just kicked, they were kicked by {ctx.message.author.mention}")

# /mute
@bot.command()
async def mute(ctx, member:discord.Member, timelimit):
    if "s" in timelimit:
        gettime = timelimit.strip("s")
        if int(gettime) > 3024000:
            await ctx.send ("The time amount can`t be bigger than 35 days")
        newtime =  datetime.timedelta(seconds=int(gettime))
        await member.edit(timed_out_until=discord.utils.utcnow()+ newtime)
        modlogs = bot.get_channel(1135308337437749380)
        await ctx.send(f"{member.name} was just muted for {str(gettime)} seconds, they were muted by {ctx.message.author.mention}")
    elif "m" in timelimit:
        gettime = timelimit.strip("m")
        if int(gettime) > 50400:
            await ctx.send ("The time amount can`t be bigger than 35 days")
        newtime =  datetime.timedelta(minutes=int(gettime))
        await member.edit(timed_out_until=discord.utils.utcnow()+ newtime)
        modlogs = bot.get_channel(1135308337437749380)
        await ctx.send(f"{member.name} was just muted for {str(gettime)} minutes, they were muted by {ctx.message.author.mention}")
    elif "h" in timelimit:
        gettime = timelimit.strip("h")
        if int(gettime) > 840:
            await ctx.send ("The time amount can`t be bigger than 35 days")
        newtime =  datetime.timedelta(hours=int(gettime))
        await member.edit(timed_out_until=discord.utils.utcnow()+ newtime)
        modlogs = bot.get_channel(1135308337437749380)
        await ctx.send(f"{member.name} was just muted for {str(gettime)} hours, they were muted by {ctx.message.author.mention}")
    elif "d" in timelimit:
        gettime = timelimit.strip("d")
        if int(gettime) > 35:
            await ctx.send ("The time amount can`t be bigger than 35 days")
        newtime =  datetime.timedelta(days=int(gettime))
        await member.edit(timed_out_until=discord.utils.utcnow()+ newtime)
        modlogs = bot.get_channel(1135308337437749380)
        await ctx.send(f"{member.name} was just muted for {str(gettime)} days, they were muted by {ctx.message.author.mention}")
    elif "w" in timelimit:
        gettime = timelimit.strip("w")
        if int(gettime) > 5:
            await ctx.send ("The time amount can`t be bigger than 35 days")
        newtime =  datetime.timedelta(weeks=int(gettime))
        await member.edit(timed_out_until=discord.utils.utcnow()+ newtime)
        modlogs = bot.get_channel(1135308337437749380)
        await ctx.send(f"{member.name} was just muted for {str(gettime)} weeks, they were muted by {ctx.message.author.mention}")


# /unmute
@bot.command()
@commands.has_any_role ("Moderator", "Administrator", "Owner")
async def unmute (ctx, member:discord. Member): 
    await member.edit(timed_out_until=None)
    await ctx.send(f"{member.mention} was just unmuted")
    modlogs = bot.get_channel(1135308337437749380)
    await ctx.send(f"{member.name} was just unmuted by {ctx.message.author.mention}")


# /help
@bot.command()
async def help(ctx): 
    embed= discord.Embed (title="Help", description="This command displays all the commands available to use with this bot", color=0x0225A3)
    embed.add_field(name="/ban", value="This command bans a user, must have moderator permissions or higher", inline=False) 
    embed.add_field(name="/kick", value="This command kicks a user, must have moderator permissions or higher", inline=False) 
    embed.add_field(name="/mute", value="This command mutes a user, must have moderator permissions or higher", inline=False) 
    embed.add_field(name="/unmute", value="This command unmutes a user, must have moderator permissions or higher", inline=False) 
    await ctx.send(embed=embed)


# for /ticket
async def ticketcallback(interaction):
    guild = interaction.guild
    role = discord.utils.get(guild.roles, name="Moderator")
    overwrites = {
        guild.default_role:discord.PermissionOverwrite(view_channel=False), 
        interaction.user: discord.PermissionOverwrite (view_channel=True),
        role: discord.PermissionOverwrite(view_channel=True)
    }

    select = Select (options=[
        discord.SelectOption (label="Help Ticket", value="01", emoji="✅", description="This will open a help ticket"),
        discord.SelectOption (label="Other ticket", value="02", emoji="❌", description="This will open a ticket in the other section")
    ])

    async def my_callback (interaction):
        if select.values[0] == "01":
            category = discord.utils.get(guild.categories, name="Tickets")
            channel = await guild.create_text_channel(f"{interaction.user.name}-ticket", category=category, overwrites=overwrites) 
            await interaction.response.send_message(f"Created ticket - <#{channel.id}>", ephemeral=True) 
            await channel.send("Hello, how can I help?")
        elif select.values[0] == "02":
            category= discord.utils.get(guild.categories, name="Other tickets")
            channel = await guild.create_text_channel(f" {interaction.user.name}-ticket", category=category, overwrites=overwrites)
            await interaction.response.send_message(f"Created ticket - <#{channel.id}>", ephemeral=True) 
            await channel.send("Hello, how can I help?")

    select.callback = my_callback
    view = View(timeout=None)
    view.add_item(select)
    await interaction.response.send_message("Choose an option below", view-view, ephemeral=True)

# /ticket
@bot.command()
async def ticket(ctx):
    button = Button (label="📥 Create Ticket", style=discord.ButtonStyle.green)
    button.callback = ticketcallback
    view = View(timeout=None)
    view.add_item(button)
    await ctx.send("Open a ticket below", view=view)


# logs join/leave
@bot.event 
async def on_member_join(member):
    logschannel = bot.get_channel(1135137019845169232)
    embed=discord.Embed(title="New Member Joined", description=f"{member.mention} joined the server!", color=0x79D823)
    embed.set_footer(text="This is vayzad`s server")
    await logschannel.send(embed=embed)

@bot.event 
async def on_member_remove(member):
    logschannel = bot.get_channel(1135137019845169232)
    embed=discord.Embed(title="A member just left", description=f"{member.mention} just left the server...", color=0xE22914)
    embed.set_footer(text="This is vayzad`s server")
    await logschannel.send(embed=embed)

# economy system/database
@bot.command()
async def balance(ctx):
    userid = ctx.message.author.id
    if os.path.isfile(f"database/{userid}.txt"):
        file = open(f"database/{userid}.txt", "r")
        await ctx.send(f"Your balance is **{file.read()}** coins")
    else: 
        file = open(f"database/{userid}.txt", "w")
        file.write("0")
        file.close()
        file = open(f"database/{userid}.txt", "r")
        await ctx.send(f"Your balance is **{file.read()}** coins")

        
# /coinflip
@bot.command()
async def coinflip(ctx, message):
    userid = ctx.message.author.id
    choices = ["heads", "tails"]    
    botchoice = random.choice (choices)
    if message == botchoice:
        if os.path.isfile(f"database/{userid}.txt"):
            file = open(f"database/{userid}.txt", "r")
            coins = int(file.read())
            file.close()
            newcoins = coins + 10
            file = open(f"database/{userid}.txt", "w")
            file.write(str(newcoins))
            file.close()
            await ctx.send(f"You picked {message} and the bot picked {botchoice} so you won **10 coins!**")
        else:
            file = open("database/(userid).txt", "w")
            file.write("10")
            file.close()
            await ctx.send(f"You picked {message} and the bot picked {botchoice} so you won **10 coins!**")
    else:
        await ctx.send(f"You picked {message} and the bot picked {botchoice} so you did not win any coins for picking the wrong option")

 
# go to token 
bot.run(config['token'])