import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup

from typing import List

cinnamonBazz = {
    "exam": "しなもんさんのツイートの最大いいね数は？",
    "ans": ['7000', '10000', '25000', '50000']
}


class TicTacToeButton(discord.ui.Button["TicTacToe"]):
    def __init__(self, label: str):
        super().__init__(style=discord.ButtonStyle.secondary, label=label)

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view

        self.style = discord.ButtonStyle.success
        content = 'はずれ'
        if self.label == '50000':
            content = 'せいかい'
            for child in self.view.children:
                child.disabled = True

        await interaction.response.edit_message(content=content, view=view)


class TicTacToe(discord.ui.View):
    children: List[TicTacToeButton]

    def __init__(self):
        super().__init__(timeout=190)

        for v in cinnamonBazz.get('ans'):
            self.add_item(TicTacToeButton(v))


class TicTacToeCog(commands.Cog):

    def __init__(self, bot):
        print('test')
        self.bot = bot

    nb = SlashCommandGroup('hayaoshi', 'test')

    @nb.command(name='test', description='button')
    async def button(self, ctx):
        # レスポンスで定義したボタンを返す
        await ctx.respond(cinnamonBazz['exam'], view=TicTacToe())


def setup(bot):
    bot.add_cog(TicTacToeCog(bot))
