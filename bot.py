import discord, os, sys, ffmpeg, subprocess, asyncio, random, gtts
from gtts import gTTS
from discord import utils
from discord.ext import commands
from discord.utils import get

filepath = os.path.dirname(os.path.abspath(__file__))
bot = commands.Bot(command_prefix=[","])
bot.remove_command("help")

def get_length(filename): #gets the length of an mp3 file
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)

def vc_test(person): #tests if the person doing the command is in a voice channel
    test = person.voice
    if test == None:
        result = False
    else:
        result = True
    return result

@bot.event #purely for console update
async def on_ready():
    print('Logged in as {0.user}'.format(bot))
    await bot.get_channel(805349681432887328).send("I'm online")

@bot.command() #used for changing status of bot
async def status(ctx, *args):
    if args[0] == "play":
        await bot.change_presence(activity=discord.Game(" ".join(args[1:])))
    if args[0] == "stream":
        await bot.change_presence(activity=discord.Streaming(name=" ".join(args[1:-1]), url=args[-1]))
    if args[0] == "listen":
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=" ".join(args[1:])))
    if args[0] == "watch":
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=" ".join(args[1:])))
    if args[0] == "reset":
        await bot.change_presence(activity=None, status=None)

@bot.command() #help command
async def help(ctx, *args):
    a = 0 #how many lines are in the embed
    embed = discord.Embed(title="Help", color=random.randint(0,0xffffff)) #creates an embed with a random colour
    if len(args) == 0: #if no argument is given, will open help_file.txt
        for i in open(filepath + "/help_file.txt"):
            command = i.strip().split(":") #splits each line of help_file.txt into [command: description]
            embed.add_field(name=str(command[0]), value=str(command[1]), inline=False) #adds each line of the file into the embed
            a += 1
        embed.set_footer(text="Type \",help [command]\" to get detailed help for each command")
    if len(args) == 1: #if an argument is given, will open help_details.txt
        if str(args[0]) == "status":
            for i in open(filepath + "/status.txt"):
                line = i.strip().split(":")
                embed.add_field(name=str(line[0]), value=str(line[1]), inline=False)
            a += 1
        else:
            for i in open(filepath + "/help_details.txt"):
                command = i.strip().split(":") #splits each line of help_details.txt into [command: description]
                if command[0] == args[0]: #checks for the command requested
                    embed.add_field(name=str(command[0]), value=str(command[1]), inline=False) #if the command requested is found, will add to the embed
                    a += 1
        embed.set_footer(text="Have a good day")
    if a == 0:
        embed.set_image(url="https://i.pinimg.com/originals/b5/80/a3/b580a383ce5cee47ab6156b0e84843cc.jpg")
        embed.add_field(name="lmao look at this clownery of a message", value=ctx.message.content, inline=True)
        embed.add_field(name="Please type a valid command", value="Lmao you didn't even type a vaild command", inline=True) #if there are 0 lines, adds a line to the embed telling user to type a valid command
        embed.set_footer(text="Lmao " + ctx.message.content + "? What kind of command is that?")
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url) #user name and profile picture
    await ctx.send(embed=embed) #sends the embed

@bot.command() #send rawr_xd.mp3
async def rawr_xd(ctx, *args):
    if len(args) == 0:
        if len(bot.voice_clients) != 0: #if bot is already saying something, skips the command
            await ctx.send("Please wait for me to finish speaking")
            return
        if vc_test(ctx.author) == True:
            vc = await ctx.author.voice.channel.connect()
            vc.play(discord.FFmpegPCMAudio(filepath + "/rawr_xd.mp3")) #plays the audio through FFmpeg
            await asyncio.sleep(float(get_length(filepath + "/rawr_xd.mp3")) + 0.00001) #waits for the mp3 file to finish
            await vc.disconnect()
        else:
            await ctx.message.add_reaction("\U0001F606") #laughing emoji
            await ctx.send("Join a voice channel and try again")
            await asyncio.sleep(0.1)
            await ctx.message.add_reaction(":emoji_3:805337017168297986") #red r
            await ctx.message.add_reaction("\U0001F1E6") #a
            await ctx.message.add_reaction("\U0001F1FC") #w
            await ctx.message.add_reaction("\U0001F1F7") #r
            await ctx.message.add_reaction("\U0001F1FD") #x
            await ctx.message.add_reaction("\U0001F1E9") #d

@bot.command() #copies what you say
async def parrot(ctx, *args):
    await ctx.message.delete()
    await asyncio.sleep(1)
    await ctx.send(" ".join(args))

@bot.command() #sends a ree
async def ree(ctx, amount):
    try:
        if amount.isnumeric() == False:
            await ctx.send("Type a vaild number")
        else:
            if int(amount) < 2000:
                await ctx.send("r" + "e"*int(amount))
            else:
                await ctx.message.add_reaction("emoji_3:805337017168297986")
                await ctx.message.add_reaction("<:emoji_2:805336901644320778>")
                await ctx.message.add_reaction(":emoji_1:805336868077830175")
                await ctx.send("Lmao that's too many e's even for me")
    except IndexError: #an argument was not supplied
        await ctx.send("Please type a number of e's to send")

@bot.command() #creates a dm with you
async def event(ctx):
    dm = await ctx.author.create_dm() #creates the dm
    await dm.send("Hello there, type \"event\" to get started")
    await asyncio.sleep(1)
    await dm.send("Note that you can also type \"event\" to restart the process if you ever type something wrong or \"cancel\" to stop the process completely")

@bot.command() #creates a timer in seconds
async def timer(ctx, seconds):
    try:
        secondint = int(seconds)
        if secondint > 300:
            await ctx.send("I dont think im allowed to do go above 300 seconds.")
            raise BaseException
        if secondint <= 0:
            await ctx.send("I dont think im allowed to do negatives")
            raise BaseException
        message = await ctx.send("Timer: " + str(seconds))
        while True:
            secondint -= 1
            if secondint == 0:
                await message.edit(content="Ended!")
                break
            await message.edit(content=f"Timer: {secondint}")
            await asyncio.sleep(1) #one second
        await ctx.send(f"{ctx.author.mention} Your countdown Has ended!")
    except ValueError:
        await ctx.send("Must be a number!")

@bot.command() #says a random slur
async def slur(ctx):
    await ctx.send(random.choice(["Turbinator", "Pinunderjip", "Kuthi", "Macaca", "Kalu", "Ganesh"]))

@bot.command() #speaks your word/phrase aloud
async def speak(ctx, *args):
    speech = " ".join(args)
    if len(bot.voice_clients) != 0: #checks if the bot is in a voice channel, returns if in a voice channel
        await ctx.send("Please wait for me to finish speaking")
        return
    try:
        gTTS(speech).save("message.mp3") #runs the text in Google's tts engine and saves it as "message.mp3"
        vc = await ctx.author.voice.channel.connect() #joins the voice channel that the user is in
        vc.play(discord.FFmpegPCMAudio("message.mp3")) #plays "message.mp3" through FFmpeg
        await asyncio.sleep(float(get_length("message.mp3")) + 0.0001) #waits 0.0001 seconds after message.mp3 is finished before leaving
        await vc.disconnect() #leaves
    except AttributeError: #user isn't in a voice channel
        await ctx.send("Join a voice channel and try again")

@bot.command() #downloads file
async def download(ctx, *args):
    await ctx.send("".join(args))
    filename = args[0]
    try:
        with open(filepath + "/" + filename, "rb") as file:
            await ctx.send("Here you go:", file=discord.File(file, filename)) #if the file is found, will send
    except FileNotFoundError: #the argument that was give was not found in the files list
        await ctx.send("This file was not found")
        await ctx.send("You may have forgotten the file extension")

@bot.event
async def on_voice_state_update(member, before, after,):
    channel = bot.get_channel(810100291147399198)
    afk = bot.get_channel(820619174275448852)
    guild = bot.get_guild(704120332486967296)
    if member.guild == guild and before.channel != afk and member != bot.user and not member.bot:
        if after.channel != afk and before.channel == None and after.channel != None:
            await channel.send(str(member.mention) + " has joined " + str(after.channel))
        if  after.channel == None and before.channel != None:
            await channel.send(str(member.mention) + " has left " + str(before.channel))

@bot.event #when a message is received
async def on_message(text):
    if text.author == bot.user:
        return

    if text.content.lower() == "event":
        details = []
        await text.channel.send("Type the name of the event")
        name = await bot.wait_for("message", check = lambda message: message.author == text.author and message.guild == None)
        if name.content.lower() == "event" or name.content.lower() == "cancel":
            return
        await name.channel.send("This is the name of the event you chose")
        await name.channel.send(name.content)
        await name.channel.send("Now type a short summary of the event (don't include the time/date in the summary)")
        details.append(name.content)
        summary = await bot.wait_for("message", check = lambda message: message.author == text.author and message.guild == None)
        if summary.content.lower() == "event" or name.content.lower() == "cancel":
            return
        await summary.channel.send("This is the summary of the event you made")
        await name.channel.send(summary.content)
        await summary.channel.send("Now type the date and time of your event")
        details.append(summary.content)
        time = await bot.wait_for("message", check = lambda message: message.author == text.author and message.guild == None)
        if time.content.lower() == "event" or name.content.lower() == "cancel":
            return
        details.append(time.content)
        await time.channel.send("Name of event: " + str(details[0]))
        await time.channel.send("Summary of event: " + str(details[1]))
        await time.channel.send("Time: " + str(details[2]))
        await time.channel.send("If these details are correct, send \"send event\" to send the event, else type \"event\" to restart the process or \"cancel\" to cancel")
        event = await bot.wait_for("message", check = lambda message: message.author == text.author and message.guild == None)
        if event.content.lower() == "event" or name.content.lower() == "cancel":
            return
        else:
            if event.content.lower() == "send event":
                announcement = bot.get_channel(723788723380289537)
                embed = discord.Embed(title=details[0], colour=random.randint(0,0xffffff))
                await event.add_reaction("\U0001F44D")
                embed.add_field(name="Summary", value=details[1], inline=False)
                embed.add_field(name="Time", value=details[2], inline=False)
                embed.set_author(name=event.author.display_name, icon_url=event.author.avatar_url)
                embed.set_footer(text="React with \U0001F44D to express interest")
                announce = await announcement.send(embed=embed)
                await announcement.send("@everyone")
                await announce.add_reaction("\U0001F44D")

    if text.guild != None:
        if not text.author.bot:
            if random.randint(1,1000) == 1:
                await text.reply("Nice you got a shiny message")
            if "bobby" in text.content.lower() or "poggers" in text.content.lower() or "pog" in text.content.lower():
                await text.add_reaction(":poggers:806108825018695681")
                await asyncio.sleep(1)
                await text.channel.send("Poggers")
                return
            await bot.process_commands(text)

code = []

for i in open(filepath + "/authentication_code.txt"):
    code.append(i.strip())
authenticator = "".join(code)
bot.run(authenticator)
