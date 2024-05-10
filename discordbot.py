import discord
import asyncio
from discord.ext import commands
intent = discord.Intents.default()
intent.message_content = True
bot = commands.Bot(command_prefix='!', intents=intent)
manual='!사용법 - 봇 사용법 확인\n\n\
!회의 (팀 이름) (월) (일) (요일) (회의 내용) - 다음 회의 일정을 공지할 때 사용하세요\n\n\
!긴급회의 (팀 이름) (월) (일) (요일) (회의 내용) - 긴급 회의 일정을 공지할 때 사용하세요\n\n\
!회의있다 (팀 이름) - 그 날 회의가 있음을 공지할 때 사용하세요'

@bot.event
async def on_ready():
    print('다음으로 로그인합니다: ')
    print(bot.user.name)
    print('connection was succesful')
    await bot.change_presence(status=discord.Status.online, activity=None)

@bot.command(name='사용법')
async def how_to_use(ctx):
    await ctx.message.delete()
    await ctx.send(embed = discord.Embed(title = '사용법', description = manual, color = discord.Color.random()))

@bot.command(name='회의')
async def meeting(ctx, team, month, day, weekday, *, subject):
    if team == '기획': team = '<@&1087970825522643015>'
    say=month+'월 '+day+'일('+weekday+')'
    embed = discord.Embed(title = '회의 일정', color = discord.Color.random())
    embed.add_field(name='다음 회의 일자', value=say, inline=False)
    embed.add_field(name='다음 회의 내용', value=subject, inline=False)
    embed.add_field(name='', value=team, inline=False)
    await ctx.message.delete()
    await ctx.send(embed=embed)

@bot.command(name='긴급회의')
async def meeting(ctx, team, month, day, weekday, *, subject):
    if team == '기획': team = '<@&1087970825522643015>'
    say=month+'월 '+day+'일('+weekday+')'
    embed = discord.Embed(title = '☆긴급 회의 일정☆', color = discord.Color.random())
    embed.add_field(name='다음 회의 일자', value=say, inline=False)
    embed.add_field(name='다음 회의 내용', value=subject, inline=False)
    embed.add_field(name='', value=team, inline=False)
    await ctx.message.delete()
    await ctx.send(embed=embed)

@bot.command(name='회의있다')
async def how_to_use(ctx, team):
    if team == '기획': team = '<@&1087970825522643015>'
    say = '오늘 회의가 있습니다'
    embed = discord.Embed(title='회의', color=discord.Color.random())
    embed.add_field(name='', value=say, inline=False)
    embed.add_field(name='', value=team, inline=False)
    await ctx.message.delete()
    await ctx.send(embed = embed)

# bot.rum('토큰 값을 입력하세요')
