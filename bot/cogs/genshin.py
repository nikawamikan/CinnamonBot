import discord
from discord.ui import Select,View
from discord.ext import commands
from discord.commands import Option,SlashCommandGroup
import aiohttp
from lib.yamlutil import yaml

uidListYaml = yaml(path='uid.yaml')
uidList = uidListYaml.load_yaml()
icon = "https://images-ext-2.discordapp.net/external/2FdKTBe_yKt6m5hYRdiTAkO0i0HVPkGDOF7lkxN6nO8/%3Fsize%3D128%26overlay/https/crafatar.com/avatars/5d3e654c29bb4ae59e3a5df78372597b.png"
l: list[discord.SelectOption] = []

class uidselectView(View):
    @discord.ui.select(
            placeholder="表示するUIDを指定してね",
            options=l
        )
    async def select_callback(self, select:discord.ui.Select, interaction):
        embed = await GenshinCog.getApi(self,uid=select.values[0])
        await interaction.response.edit_message(content=None,embed=embed[0],view=self)

class GenshinCog(commands.Cog):

    def __init__(self, bot):
        print('genshin初期化')
        self.bot = bot

    async def getApi(self,uid):
        url = f"https://enka.network/u/{uid}/__data.json"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                resp = await response.json()
        try:
            embed = discord.Embed( 
                                title="あなたの原神ステータスだよ",
                                color=0x1e90ff, 
                                description="多分リアルタイムだよ", 
                                url=url 
                                )
            embed.add_field(inline=False,name="ユーザーネーム",value=resp['playerInfo']['nickname'])
            embed.add_field(inline=False,name="ステータスメッセージ",value=resp['playerInfo']['signature'])
            embed.add_field(inline=False,name="レベル",value=resp['playerInfo']['level'])
            embed.add_field(inline=False,name="世界ランク",value=resp['playerInfo']['worldLevel'])
            embed.add_field(inline=False,name="深境螺旋",value=f"{resp['playerInfo']['towerFloorIndex']}-{resp['playerInfo']['towerLevelIndex']}")
            embed.set_footer(text="made by CinnamonSea2073", icon_url=icon)
            return embed, resp['playerInfo']['nickname']
        except:
            embed = discord.Embed( 
                    title=f"エラーが発生しました。APIを確認してからもう一度お試しください。\n{url}",
                    color=0x1e90ff, 
                    url=url 
                    )
            return embed
    
    genshin = SlashCommandGroup('genshin', 'test')

    @genshin.command(name="get", description="UUIDからキャラ情報を取得します")
    async def genshin_get(
            self,
            ctx: discord.ApplicationContext,
    ):
        await ctx.respond("読み込み中")
        global l
        for uid, v in uidList.items():
            print(v['uid'])
            print(v['user'])
            l.append(discord.SelectOption(label=str(uid), description=v['user']))
        view = uidselectView()
        await ctx.send(view=view)

    @genshin.command(name="set", description="あなたのUIDを設定します")
    async def genshin_set(
            self,
            ctx: discord.ApplicationContext,
            uid: Option(int, required=True, description="UIDを指定しやがれってんだ!!!（？）", )
    ):
        await ctx.respond("読み込み中")
        print(uid)
        user = await self.getApi(uid)
        print(user[1])
        uidList[str(uid)] = {"uid": uid, "name": ctx.author.name, "user": user[1]}
        uidListYaml.save_yaml(uidList)
        await ctx.send(f"<@{ctx.author.id}>\nUID多分設定できたで\nuid : **{uid}**\nusername : **{user[1]}**")

def setup(bot):
    bot.add_cog(GenshinCog(bot))