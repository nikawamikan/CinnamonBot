# This example requires the 'message_content' privileged intent for prefixed commands.
import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup

from typing import List


# Defines a custom button that contains the logic of the game.
# The ['Hayaoshi'] bit is for type hinting purposes to tell your IDE or linter
# what the type of `self.view` is. It is not required.
class HayaoshiButton(discord.ui.Button["Hayaoshi"]):
    def __init__(self, x: int, y: int):
        # A label is required, but we don't need one so a zero-width space is used.
        # The row parameter tells the View which row to place the button under.
        # A View can only contain up to 5 rows -- each row can only have 5 buttons.
        # Since a Tic Tac Toe grid is 3x3 that means we have 3 rows and 3 columns.
        super().__init__(style=discord.ButtonStyle.secondary, label="\u200b", row=5)
        self.x = x
        self.y = y

    # This function is called whenever this particular button is pressed.
    # This is part of the "meat" of the game logic.
    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: Hayaoshi = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            self.style = discord.ButtonStyle.danger
            self.label = "X"
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = "It is now O's turn"
        else:
            self.style = discord.ButtonStyle.success
            self.label = "O"
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = "It is now X's turn"

        self.disabled = True
        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = "X won!"
            elif winner == view.O:
                content = "O won!"
            else:
                content = "It's a tie!"

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)


# This is our actual board View.
class Hayaoshi(discord.ui.View):
    # This tells the IDE or linter that all our children will be HayaoshiButtons.
    # This is not required.
    children: List[HayaoshiButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        # Our board is made up of 3 by 3 HayaoshiButtons.
        # The HayaoshiButton maintains the callbacks and helps steer
        # the actual game.
        for x in range(3):
            for y in range(3):
                self.add_item(HayaoshiButton(x, y))

    # This method checks for the board winner and is used by the HayaoshiButton.
    def check_board_winner(self):
        # Check horizontal
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check vertical
        for line in range(3):
            value = self.board[0][line] + \
                self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check diagonals
        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == -3:
            return self.X
        elif diag == 3:
            return self.O

        # If we're here, we need to check if a tie has been reached.
        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None


class HayaoshiCog(commands.Cog):

    def __init__(self, bot):
        print('test')
        self.bot = bot

    nb = SlashCommandGroup('hayaoshi', 'test')

    @nb.command(name='test', description='button')
    async def button(self, ctx):
        # レスポンスで定義したボタンを返す
        await ctx.respond("Tic Tac Toe: X goes first", view=Hayaoshi())


def setup(bot):
    bot.add_cog(HayaoshiCog(bot))
