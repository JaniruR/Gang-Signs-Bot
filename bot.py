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
    print('We have logged in as {0.user}'.format(bot))

@bot.command() #used for changing status of bot
async def status(ctx, *args):
    if args[0] == "play":
        game = ""
        for i in args[1:]:
            game += i
            game += " "
            await bot.change_presence(activity=discord.Game(game))
    if args[0] == "stream":
        stream = ""
        for i in args[1:-1]:
            stream += i
            stream += " "
        await bot.change_presence(activity=discord.Streaming(name=stream, url=args[-1]))
    if args[0] == "listen":
        song = ""
        for i in args[1:]:
            song += i
            song += " "
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=song))
    if args[0] == "watch":
        video = ""
        for i in args[1:]:
            video += i
            video += " "
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=video))
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
        embed.add_field(name="Please type a valid command", value="Lmao you didn't even type a vaild command", inline=False) #if there are 0 lines, adds a line to the embed telling user to type a valid command
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
async def ree(ctx, *args):
    try:
        if args[0].isnumeric() == False:
            await ctx.send("Type a vaild number")
        else:
            if int(args[0]) < 2000:
                await ctx.send("r" + "e"*int(args[0]))
            else:
                await ctx.message.add_reaction("emoji_3:805337017168297986")
                await ctx.message.add_reaction("<:emoji_2:805336901644320778>")
                await ctx.message.add_reaction(":emoji_1:805336868077830175")
                await ctx.send("Lmao that's too many e's even for me")
            if len(args) == 2:
                if args[1][:2] == "<@":
                    await ctx.message.delete()
                    await asyncio.sleep(1)
                    await ctx.send(args[1])
                    if random.choice(["0","1"]) != "0": #author will have a 50% chance of being exposed
                        await ctx.send(ctx.author.mention + " was the one who mentioned you btw")
    except IndexError: #an argument was not supplied
        await ctx.send("Please type a number of e's to send")

@bot.command() #creates a dm with you
async def create_dm(ctx):
    dm = await ctx.author.create_dm() #creates the dm
    await dm.send("Type \"event\" in this dm to start creation of an event")
    await asyncio.sleep(1)
    await dm.send("For future reference, you can initiate this command straight from the dm next time by doing \"event\"")

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
    speech = ""
    for i in args:
        speech += i
        speech += " "
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
    await ctx.send(args)
    filename = args[0]
    try:
        with open(filepath + "/" + filename, "rb") as file:
            await ctx.send("Here you go:", file=discord.File(file, filename)) #if the file is found, will send
    except FileNotFoundError: #the argument that was give was not found in the files list
        await ctx.send("This file was not found")
        await ctx.send("You may have forgotten the file extension or added an unecessary")

@bot.event
async def on_voice_state_update(member, before, after,):
    channel = bot.get_channel(810100291147399198)
    if before.channel == None and after.channel != None and member != bot.user and not member.bot:
        await channel.send(str(member.mention) + " has joined " + str(after.channel))
    if after.channel == None and before.channel != None and member != bot.user and not member.bot:
        await channel.send(str(member.mention) + " has left " + str(before.channel))

@bot.event #when a message is received
async def on_message(message):
    if message.author == bot.user:
        return

    if message.guild == None:
        if message.content[:5] == "event":
            await message.channel.send("I see you would like to start an event?")
            await asyncio.sleep(0.5)
            await message.channel.send("I'm not very smart so I don't understand context (I would also like it if you don't try to do these commands out of order cuz I'm not very smart), if you really want to start an event, type \"name of event: \" before your next sentence to type in the name of the event")
            await asyncio.sleep(1)
            await message.channel.send("Like this:")
            await asyncio.sleep(0.5)
            await message.channel.send("name of event: my birthday")

        if message.content[:15].lower() == "name of event: ":
            event_name = message.content[15:]
            await message.channel.send("Okay, the name of the event is")
            await asyncio.sleep(0.5)
            await message.channel.send(event_name)
            await asyncio.sleep(0.5)
            await message.channel.send("If this is wrong, please do the event message again")
            file = open(filepath + "/events_" + str(message.author) + ".txt", "w+")
            file.write(event_name.upper())
            file.close()
            await asyncio.sleep(1)
            await message.channel.send("If this is correct, please type out a summary of the event (day/time isn't part of the summary) using \"summary: \" before the summary like last time (type the summary in one line please cuz it just makes it easier for me)")

        if message.content[:9].lower() == "summary: ":
            details = []
            for i in open(filepath + "/events_" + str(message.author) + ".txt"):
                details.append(i)
            if len(details) == 0:
                await message.channel.send("Lmao silly billy don't do the commands out of order")
            event_summary = message.content[9:]
            await message.channel.send("This is your event summary")
            await asyncio.sleep(0.5)
            await message.channel.send(event_summary)
            await asyncio.sleep(0.5)
            await message.channel.send("If this is correct, type \"time: \" to add the date and time")
            file = open(filepath + "/events_" + str(message.author) + ".txt", "w+")
            file.write(details[0] + "\n")
            file.write(event_summary)
            file.close()

        if message.content.lower()[:6] == "time: ":
            details = []
            for i in open(filepath + "/events_" + str(message.author) + ".txt"):
                details.append(i)
            if len(details) == 0:
                await message.channel.send("Lmao you haven't even started the process, don't think I'm going to let you have the chance to break me")
                return
            if len(details) == 1:
                await message.channel.send("You forgot to do a summary of the events. To add a summary type \"summary: \" followed by a summary (type it in one line please)")
                return
            time = message.content[6:]
            await message.channel.send("This is the date and time that you have input")
            await asyncio.sleep(0.5)
            await message.channel.send(time)
            file = open(filepath + "/events_" + str(message.author) + ".txt", "w+")
            file.write(details[0])
            file.write(details[1] + "\n")
            file.write("*" + str(time) + "*")
            file.close()
            await message.channel.send("Type \"details\" to see details about the event")

        if message.content.lower() == "details":
            deets = []
            try:
                for i in open(filepath + "/events_" + str(message.author) + ".txt"):
                    deets.append(i)
            except FileNotFoundError:
                await message.channel.send("You haven't even started yet smh")
                return
            if len(deets) == 3:
                await message.channel.send("Event name: " + deets[0].lower())
                await asyncio.sleep(1)
                await message.channel.send("Event summary: " + deets[1])
                await asyncio.sleep(1)
                await message.channel.send("Time and date: " + deets[2])
                await asyncio.sleep(2)
                await message.channel.send("Make sure these details are correct")
                await asyncio.sleep(1)
                await message.channel.send("type \"send event\" to send this event to the announcements tab")

        if message.content.lower() == "send event":
            final_deets = ""
            deets_count = []
            current_events = []
            announcement = bot.get_channel(723788723380289537)
            for i in open(filepath + "/events_" + str(message.author) + ".txt"):
                final_deets += i
                deets_count.append(i)
            if len(deets_count) < 3:
                await message.channel.send("Please finish typing all of the details")
            else:
                await announcement.send(final_deets + "\n" + "@everyone. React with \U0001F44D to express interest in this event")
                await announce.add_reaction("\U0001F44D")
                await message.add_reaction("\U0001F44D")
                os.remove(filepath + "/events_" + str(message.author) + ".txt")

    if message.guild != None:
        if "bobby" in message.content.lower():
            await message.add_reaction(":poggers:806108825018695681")
            await message.add_reaction("\U0001F1F5")
            await message.add_reaction("\U0001F1F4")
            await message.add_reaction("\U0001F1EC")
            await asyncio.sleep(1)
            pog = await message.channel.send("Poggers")
            await pog.add_reaction(":poggers:806108825018695681")
            await pog.add_reaction("\U0001F1F5")
            await pog.add_reaction("\U0001F1F4")
            await pog.add_reaction("\U0001F1EC")
            return
        if "poggers" in message.content.lower() or "pog" in message.content.lower():
             await message.add_reaction(":poggers:806108825018695681")
             await message.add_reaction("\U0001F1F5")
             await message.add_reaction("\U0001F1F4")
             await message.add_reaction("\U0001F1EC")
             await asyncio.sleep(1)
             pog = await message.channel.send("Poggers")
             await pog.add_reaction(":poggers:806108825018695681")
             await pog.add_reaction("\U0001F1F5")
             await pog.add_reaction("\U0001F1F4")
             await pog.add_reaction("\U0001F1EC")
             return
        await bot.process_commands(message)

bot.run("ODA0MzI4MTA0MzY5NTg2MjA3" + ".YBKu6w.Rku0syKGmTGvYVuJ4jJ4ynQIe54") #client token is split in two sections to avoid dicord automatically picking it up and changing it
