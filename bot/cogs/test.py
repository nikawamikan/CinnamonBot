from cogs.shogi import *
import discord
from discord.ext import commands
from discord import Option, SlashCommandGroup

ROOM_NAMES = ["Norma", "Morris", "Jimmy", "Baranov",
              "Sebastian", "Rooke", "Lynsey", "Collingwood"]


class RecruitmentView(discord.ui.View):

    def __init__(self, auther, n):
        super().__init__(timeout=190)
        self.members = [auther]
        self.auther = auther
        self.n = n
    MEMBER_LABEL = "{}人集まってるよ"

    @discord.ui.button(label=MEMBER_LABEL.format(1), row=0, style=discord.ButtonStyle.primary)
    async def member_button(self, button: discord.Button, interaction: discord.Interaction):
        if interaction.user.id in self.members:
            await interaction.response.send_message(
                content="既に登録してるよ", ephemeral=True)
        else:
            self.members.append(interaction.user.id)

            members: str = ""
            for v in self.members:
                members += f"<@!{v}>\n"
            num_people = len(self.members)
            button.label = RecruitmentView.MEMBER_LABEL.format(
                len(self.members))
            if num_people >= 2:
                for child in self.children:
                    child.disabled = False
            await interaction.response.edit_message(
                content=f"{members} が集まってくれてるよ！", view=self)

    @discord.ui.button(label="はじめる", row=1, style=discord.ButtonStyle.success, disabled=True)
    async def begin_button(self, _: discord.Button, interaction: discord.Interaction):
        await interaction.response.edit_message(content="スレッドを開始します", view=None)
        thread = await interaction.channel.create_thread(name=f"{ROOM_NAMES[self.n]}", auto_archive_duration=60, type=discord.ChannelType.public_thread)
        self.n = (self.n + 1) % len(ROOM_NAMES)

        async def countdown(ctx: discord.Message, n: int, message="{}"):
            await asyncio.sleep(1)
            for i in range(n):
                await ctx.edit(content=message.format(str(n-i)))
                await asyncio.sleep(1)
        message = await thread.send(content="10秒後に開始します")
        await countdown(ctx=message, n=9, message="あと {} 秒")
        key: list = random_key_list()
        count = 9
        await message.edit(content=minhaya[key[count]]["exam"], view=HayaoshiView(prize_money=30000, count=count, key=key, thread=thread))


class Hoge(commands.Cog):
    def __init__(self, bot):
        print('test init')
        self.bot = bot
        self.n = 0

    command = SlashCommandGroup('t', 'hoge')

    @command.command(name='e', description='???')
    async def set(
        self,
        ctx: discord.ApplicationContext,
    ):
        await ctx.respond(content="メンバーの募集を開始するよ", view=RecruitmentView(auther=ctx.author.id, n=self.n))
        self.n = (self.n + 1) % len(ROOM_NAMES)


def setup(bot):
    bot.add_cog(Hoge(bot))
