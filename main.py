import requests
from bs4 import BeautifulSoup
from datetime import date
import re
import discord
from discord.ext import commands
import time
import urllib.request
import datetime


client = commands.Bot(command_prefix="!", help_command=None)
TOKEN = ("YOUR DISCORD BOT TOKEN HERE")
DISCORD_CHANNEL_NAME = "nba-result"
url_start = "https://sports.yahoo.com"
today = date.today()


def getdata(url):
    r = requests.get(url)
    return r.text


@client.command()
async def nba(ctx):
    while True:
        today = datetime.date.today()
        Previous_Date = today - datetime.timedelta(days=1)
        print(Previous_Date)
        name, score, space, link_game_name, nu, a = "", "", 0, list(), 0, 0
        odd_name = list()
        even_name = list()
        odd_score = list()
        even_score = list()
        htmldata = getdata(f"https://sports.yahoo.com/nba/scoreboard/?confId=&dateRange={Previous_Date}&schedState=")
        soup = BeautifulSoup(htmldata, 'html.parser')
        embed = discord.Embed(
            title=f"NBA Results {today}",
            colour=discord.Colour.blue()
        )

        for link_game in soup.find_all('a', attrs={'href': re.compile("/nba/")}):
            if nu > 11:
                link_game_name.append(link_game.get('href'))
                nu += 1
            else:
                nu += 1

        for name, score in zip(soup.find_all(class_="YahooSans Fw(700)! Fz(14px)!"),
                               soup.find_all(class_="YahooSans Fw(700)! Va(m) Fz(24px)!")):
            space += 1
            if (space % 2) == 0:
                even_name.append(name.get_text())
                even_score.append(score.get_text())
                a += 1
            else:
                odd_name.append(name.get_text())
                odd_score.append(score.get_text())

        for name_o, score_o, name_e, score_e, game_url in zip(odd_name, odd_score, even_name, even_score, link_game_name):
            game_highlight = ""
            if int(score_o) > int(score_e):
                html = urllib.request.urlopen(f"https://www.youtube.com/results?search_query={game_url}")
                video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
                game_highlight = (f"https://www.youtube.com/watch?v={video_ids[0]}")
                embed.add_field(name=f"**{name_o} : {score_o}**\n~~{name_e} : {score_e}~~",
                                value=f"[More Info]({url_start}{game_url})\n[Highlights]({game_highlight})",
                                inline=True)
            else:
                html = urllib.request.urlopen(f"https://www.youtube.com/results?search_query={game_url}")
                video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
                game_highlight = (f"https://www.youtube.com/watch?v={video_ids[0]}")
                embed.add_field(name=f"~~{name_o} : {score_o}~~\n**{name_e} : {score_e}**",
                                value=f"[More Info]({url_start}{game_url})\n[Highlights]({game_highlight})",
                                inline=True)

        await ctx.send(embed=embed)
        time.sleep(86400) # time in seconds when you want to give you the results again 86400 is 24 hours

client.run(TOKEN)
