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
        nickname = loads(response_channel.text)['data'][0]['user_name']
        game_name = loads(response_channel.text)['data'][0]['game_name']
        title = loads(response_channel.text)['data'][0]['title']
        icon = 'https://static-cdn.jtvnw.net/jtv_user_pictures/7d7a3d97-fe35-4622-ae51-da358992947f-profile_image' \
               '-300x300.jpeg '
        stream_start = loads(response_channel.text)['data'][0]['started_at']
        print_time = stream_start[0:4] + '년' + stream_start[5:7] + '월' + stream_start[8:10] + '일 ' + stream_start[11:19]
        # embed
        embed = discord.Embed(title=nickname, description=title, color=0x62c1cc)
        embed.set_author(name=nickname, icon_url=icon)
        embed.add_field(name="게임", value=game_name, inline=True)
        embed.add_field(name="방송 보러가기", value='https://www.twitch.tv/' + Twitch, inline=True)
        embed.set_footer(text='방송 시작 • ' + print_time)
        embed.set_thumbnail(url=icon)
        # 라이브 상태 체크
        try:
            # 방송 정보에서 'data'에서 'type' 값이 live 이고 체크상태가 false 이면 방송 알림(오프라인이면 방송정보가 공백으로 옴)
            if loads(response_channel.text)['data'][0]['type'] == 'live' and check == False:
                await channel.send("@everyone" + nickname + " 님이 방송을 시작했다구! 어서들 보러 오라구!")
                print("Online")
                check = True
        except:
            print("Offline")
            check = False

        await asyncio.sleep(20)

app.run(os.environ['token'])