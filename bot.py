import discord, os, sys, ffmpeg, subprocess, asyncio

client = discord.Client()

def vc_test(person):
    test = person.author.voice
    if test == None:
        result = False
    else:
        result = True
    return result

def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.lower() == "rawr xd":
        amount, a, filepath = [], 0,  os.path.dirname(os.path.abspath(__file__))
        file = open(filepath + "/rawr_xd.txt", "r")
        for i in file:
            amount.append(list(i.strip().split()))
        file.close()
        for i in amount:
            i[1] = int(i[1])
        for i in amount:
            if i[0] == message.author.name:
                i[1] += 1
                a += 1
        if a == 0:
            amount.append([message.author.name,1])
        file = open(filepath + "/rawr_xd.txt", "w")
        for i in amount:
            file.write(str(i[0]) + "\t\t\t\t" + str(i[1]) + "\n")
        file.close()
        if vc_test(message) == True:
            await message.delete()
            vc = await message.author.voice.channel.connect()
            vc.play(discord.FFmpegPCMAudio(filepath + "/rawr_xd.mp3"))
            await asyncio.sleep(float(get_length(filepath + "/rawr_xd.mp3"))+0.00001)
            await vc.disconnect()
        else:
            await message.add_reaction("\U0001F606")
            await message.channel.send("Join a voice channel and try again")

    if message.content.lower() == "i am lonely":
        await message.delete()
        await message.channel.send("Good :)")

client.run("ODA0MzI4MTA0MzY5NTg2MjA3" + ".YBKu6w.Rku0syKGmTGvYVuJ4jJ4ynQIe54")
