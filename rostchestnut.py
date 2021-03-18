import discord
# import openpyxl as openpyxl
import requests
import asyncio
from json import loads
import os

from discord.ext import commands

app = commands.Bot(command_prefix='!')

@app.event
async def on_ready():
    print(app.user.id)
    print("전 준비됐답니다~~")
    game = discord.Game("내 키는 185cm")
    await app.change_presence(status=discord.Status.dnd, activity=game)

    Twitch = 'gu05179'
    name = '군밤소년'
    twitch_Client_ID = 'z3h5altd9xaau4gmighodebwjjliwd'
    twitch_Client_secret = 'ofisiq4twzfmr2hxh6q4r6z7blw21q'
    channel = app.get_channel(821011605496135770)
    oauth_key = requests.post("https://id.twitch.tv/oauth2/token?client_id=" + twitch_Client_ID + "&client_secret=" + twitch_Client_secret + "&grant_type=client_credentials")
    access_token = loads(oauth_key.text)["access_token"]
    token_type = 'Bearer '
    authorization = token_type + access_token
    print(authorization)
    check = False

    while True:
        print("ready on Notification")

        # 트위치 api에게 방송 정보 요청
        headers = {'client-id': twitch_Client_ID, 'Authorization': authorization}
        response_channel = requests.get('https://api.twitch.tv/helix/streams?user_login=' + Twitch, headers=headers)
        print(response_channel.text)
        # 라이브 상태 체크
        try:
            # 방송 정보에서 'data'에서 'type' 값이 live 이고 체크상태가 false 이면 방송 알림(오프라인이면 방송정보가 공백으로 옴)
            if loads(response_channel.text)['data'][0]['type'] == 'live' and check == False:
                await channel.send("@everyone" + name + " 님이 방송을 시작했다구! 어서들 보러 오라구!")
                print("Online")
                check = True
        except:
            print("Offline")
            check = False

        await asyncio.sleep(20)

@app.command()
async def ping(ctx):
    await ctx.send("pong!")

    # while True:
    #     headers = {'clinet-ID': 'z3h5altd9xaau4gmighodebwjjliwd', 'Authorization': authorization}
    #     response = requests.get(" https://api.twitch.tv/helix/streams?user_login=" + Twitch, headers=headers)
    #     try:
    #         if loads(response.text)[0]['type'] == 'live' and a == False:
    #             await channel.send(name + "님이 방송을 시작하셨습니다")
    #             a = 1
    #
    #     except:
    #         a = 0
    #     await asyncio.sleep(1)

app.run(os.environ['token'])