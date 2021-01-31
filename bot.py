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
                    await ctx.message.channel.send(args[1])
                    await ctx.message.channel.send(ctx.message.author.mention + " was the one who mentioned you btw")
    except IndexError:
        await ctx.message.channel.send("Please tpye a number of e's to send")
        await asyncio.sleep(1)
        await ctx.message.channel.send("However...")
        await asyncio.sleep(1)
        await ctx.message.channel.send("ree")

bot.run("ODA0MzI4MTA0MzY5NTg2MjA3" + ".YBKu6w.Rku0syKGmTGvYVuJ4jJ4ynQIe54") #client token is split in two sections to avoid dicord automatically picking it up and changing it
