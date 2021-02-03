import discord, os, sys, ffmpeg, subprocess, asyncio, random, gtts
from gtts import gTTS
from discord.ext import commands

filepath = os.path.dirname(os.path.abspath(__file__))
bot = commands.Bot(command_prefix=[","])
bot.remove_command("help")
slurs = ["Turbinator", "Pinunderjip", "Kuthi", "Macaca", "Kalu", "Ganesh"]

def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)

def vc_test(person):
    test = person.author.voice
    if test == None:
        result = False
    else:
        result = True
    return result

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

@bot.command()
async def status(ctx, *args):
    if str(ctx.author) == "xemnas2004#4845":
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
            await bot.change_presence(activity = None, status=None)
    else:
        await ctx.channel.send("No")

@bot.command()
async def help(ctx, *args):
    commands_list, commands = [], "```"
    if len(args) == 0:
        for i in open(filepath + "/help_file.txt"):
            commands_list.append(i)
        for i in commands_list:
            commands += str(i)
            commands += "\n"
        commands += "```"
    if len(args) == 1:
        for i in open(filepath + "/help_details.txt"):
            line = i.split()
            if line[0] == args[0]:
                for j in line[1:]:
                    commands += j
                    commands += " "
                commands += "\n\n"
        commands += "```"
        await ctx.message.channel.send("```json\n\"" + args[0] + "\"\n```")
    if commands != "``````":
        await ctx.message.channel.send(commands)
    else:
        await ctx.message.channel.send("Type a valid command to get help for")

@bot.command()
async def rawr_xd(ctx, *args):
    if len(args) == 0:
        if vc_test(ctx.message) == True:
            vc = await ctx.message.author.voice.channel.connect()
            vc.play(discord.FFmpegPCMAudio(filepath + "/rawr_xd.mp3"))
            await asyncio.sleep(float(get_length(filepath + "/rawr_xd.mp3")) + 0.00001) #waits for the mp3 file to finish
            await vc.disconnect()
        else:
            await ctx.message.add_reaction("\U0001F606")
            rawr = await ctx.message.channel.send("Join a voice channel and try again")
            await asyncio.sleep(0.1)
            await ctx.message.add_reaction(":emoji_3:805337017168297986")
            await ctx.message.add_reaction("\U0001F1E6")
            await ctx.message.add_reaction("\U0001F1FC")
            await ctx.message.add_reaction("\U0001F1F7")
            await ctx.message.add_reaction("\U0001F1FD")
            await ctx.message.add_reaction("\U0001F1E9")
            await rawr.add_reaction(":emoji_3:805337017168297986")
            await rawr.add_reaction("\U0001F1E6")
            await rawr.add_reaction("\U0001F1FC")
            await rawr.add_reaction("\U0001F1F7")
            await rawr.add_reaction("\U0001F1FD")
            await rawr.add_reaction("\U0001F1E9")

@bot.command()
async def parrot(ctx, *args):
    a = ""
    for i in args:
        a += i
        a += " "
    if "bobby" in ctx.message.content.lower():
        b = 1
    await ctx.message.delete()
    await asyncio.sleep(1)
    repeat = await ctx.message.channel.send(a)
    if b == 1:
        await repeat.add_reaction(":poggers:806108825018695681")

@bot.command()
async def ree(ctx, *args):
    try:
        if args[0].isnumeric() == False:
            await ctx.message.channel.send("Type a vaild number")
        else:
            if int(args[0]) < 2000:
                message = "r" + "e"*int(args[0])
                await ctx.message.channel.send(message)
            else:
                await ctx.message.add_reaction("emoji_3:805337017168297986")
                await ctx.message.add_reaction("<:emoji_2:805336901644320778>")
                await ctx.message.add_reaction(":emoji_1:805336868077830175")
                await ctx.message.channel.send("Lmao that's too many e's even for me")
            if len(args) == 2:
                if args[1][:2] == "<@":
                    await ctx.message.delete()
                    await asyncio.sleep(1)
                    await ctx.message.channel.send(args[1])
                    if ctx.message.author != "xemnas2004#4845":
                        if random.choice(["0","1"]) != "0":
                            await ctx.message.channel.send(ctx.message.author.mention + " was the one who mentioned you btw")

    except IndexError:
        await ctx.message.channel.send("Please type a number of e's to send")
        await asyncio.sleep(1)
        await ctx.message.channel.send("However...")
        await asyncio.sleep(1)
        await ctx.message.channel.send("ree")

@bot.command()
async def event(ctx, *args):
    dm = await ctx.message.author.create_dm()
    await dm.send("Type \"event\" in this dm to start creation of an event")
    await asyncio.sleep(1)
    await dm.send("For future reference, you can initiate this command straight from the dm next time")

@bot.command()
async def timer(ctx, seconds):
    try:
        secondint = int(seconds)
        if secondint > 300:
            await ctx.send("I dont think im allowed to do go above 300 seconds.")
            raise BaseException
        if secondint <= 0:
            await ctx.send("I dont think im allowed to do negatives")
            raise BaseException
        message = await ctx.send("Timer: {seconds}")
        while True:
            secondint -= 1
            if secondint == 0:
                await message.edit(content="Ended!")
                break
            await message.edit(content=f"Timer: {secondint}")
            await asyncio.sleep(1)
        await ctx.send(f"{ctx.author.mention} Your countdown Has ended!")
    except ValueError:
        await ctx.send("Must be a number!")

@bot.command()
async def slur(ctx):
    await ctx.channel.send(random.choice(slurs))

@bot.command()
async def speak(ctx, *args):
    speech = ""
    for i in args:
        speech += i
        speech += " "
    if ctx.voice_client != None:
        await ctx.message.channel.send("Please wait until i finish speaking")
        return
    else:
        try:
            gTTS(speech).save(filepath + "/message.mp3")
            vc = await ctx.author.voice.channel.connect()
            vc.play(discord.FFmpegPCMAudio(filepath + "/message.mp3"))
            await asyncio.sleep(float(get_length(filepath + "/message.mp3")) + 0.0001)
            await vc.disconnect()
        except AttributeError:
            await ctx.message.channel.send("Join a voice channel and try again")

@bot.event
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
            announcement = bot.get_channel(723788723380289537)
            for i in open(filepath + "/events_" + str(message.author) + ".txt"):
                final_deets += i
                deets_count.append(i)
            if len(deets_count) < 3:
                await message.channel.send("Please finish typing all of the details")
            else:
                announce = await announcement.send(final_deets + "\n" + "@everyone")
                await announce.add_reaction("\U0001F4C5")
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
