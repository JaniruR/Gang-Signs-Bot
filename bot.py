import discord, os, sys, ffmpeg, subprocess, asyncio
from discord.ext import commands

filepath = os.path.dirname(os.path.abspath(__file__))
bot = commands.Bot(command_prefix=[","])
bot.remove_command("help")

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
            await ctx.message.channel.send("Join a voice channel and try again")

@bot.command()
async def parrot(ctx, *args):
    a = ""
    for i in args:
        a += i
        a += " "
    await ctx.message.delete()
    await ctx.message.channel.send(a)

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
                if args[1][:3] == "<@!":
                    await ctx.message.delete()
                    await asyncio.sleep(1)
                    await ctx.message.channel.send(args[1])
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
            if len(details) == 1:
                await message.channel.send("You forgot to do a summary of the events. To add a summary type \"summary: \" followed by a summary (type it in one line please)")
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
            for i in open(filepath + "/events_" + str(message.author) + ".txt"):
                deets.append(i)
            if len(deets) == 3:
                await message.channel.send("Event name: " + deets[0].lower())
                await asyncio.sleep(1)
                await message.channel.send("Event summary: " + deets[1])
                await asyncio.sleep(1)
                await message.channel.send("Time and date: " + deets[2])
                await asyncio.sleep(2)
                await message.channel.send("If these details are correct, type \"send event\" to send the event to the announcements tab")
            else:
                await message.channel.send("Please finish typing all of the details")

        if message.content.lower() == "send event":
            final_deets = ""
            deets_count = []
            announcement = bot.get_channel(805349780124991499)
            for i in open(filepath + "/events_" + str(message.author) + ".txt"):
                final_deets += i
                deets_count.append(i)
            if len(deets_count) < 3:
                await message.channel.send("Please finish typing all of the details")
            else:
                await announcement.send(final_deets + "\n" + "@everyone")

    if message.guild != None:
        await bot.process_commands(message)

bot.run("ODA0MzI4MTA0MzY5NTg2MjA3" + ".YBKu6w.Rku0syKGmTGvYVuJ4jJ4ynQIe54") #client token is split in two sections to avoid dicord automatically picking it up and changing it
