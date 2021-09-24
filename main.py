# bot.py
import os
import sys
import discord
from discord.ext import commands
from query import *
import datetime

posts = []
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    sys.stdout.flush()
@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'操你媽 {member.name}\n'
        , f'!q 查詢課程'
    )


@bot.event
async def on_error(event, *args, **kwargs):
    print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')


@bot.command(name='sex')
async def query(ctx, arg):
    global posts
    print(ctx.author, ' quried at ', datetime.datetime.now())
    if not arg:
        await ctx.send('!help for details of command')
    if arg == 'help':
        text = ''
        text += '!sex poular 熱門文章\n'
        text += '!sex newest 最新文章\n'
        text += '!sex {文章編號} 檢視文章\n'
        await ctx.send(text[:2000])
    elif not arg.isdigit():
        posts = querySex(arg)
        index = 0
        text = ''
        for content in posts:
            text += str(index) + '.' + content['title'] + '\n'
            index += 1
        while text:
            await ctx.send(text[:2000])
            text = text[2000:]

    elif arg.isdigit() and posts:
        text = ''
        index = int(arg)
        post = querySex(posts[index]['id'])
        #text += posts[index]['link'] + '\n'
        if not post['anonymousSchool']:
            text += post['school'] + '\n'
        text += post['title'] + '\n'
        text += post['content'] + '\n'
        #text += posts[index]['url'] + '\n'
        await ctx.send(text[:2000])



    



@bot.command(name='q')
async def query(ctx, arg):
    print(ctx.author, ' quried at ', datetime.datetime.now())
    text = queryCourse(arg)
    while text:
        await ctx.send(text[:2000])
        text = text[2000:]
if __name__ == "__main__":
    bot.run(TOKEN)