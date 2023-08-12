import discord
from discord.ext import commands
import random

player1 = ""
player2 = ""
turn = ""
game_over = True
#Sets a board array
board = []

client = commands.Bot(command_prefix='t?')

W_Conditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

#Creates a New Tic-Tac-Toe Board
@client.command(aliases = ['ttt'])
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global player1
    global player2
    global turn
    global game_over
    global count

    if game_over:
        global board
        #Board itself
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        game_over = False
        count = 0

        player1 = p1
        player2 = p2
        #Print the board
        line = ""
        for i in range(len(board)):
            if i == 2 or i == 5 or i == 8:
                line += " " + board[i]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[i]
        #Decide who goes first: Player1 or Player2
        number = random.randint(1, 2)
        if number == 1:
            turn = player1
            await ctx.send(f"{player1.mention} goes first")
            return
        elif number == 2:
            turn = player2
            await ctx.send(f"{player2.mention} goes first")
            return
    else: 
        await ctx.send("Your already in a Tic-Tac-Toe game! Finish your game and then start a new one!")

@client.command()
async def move(ctx, position: int):
    global turn
    global player1
    global player2
    global board
    global count 
    

    if not game_over:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < position < 10 and board[position - 1] == ":white_large_square:":
                board[position - 1] = mark
                count += 1 

                #Print board(again)
                line = ""
                for i in range(len(board)):
                    if i == 2 or i == 5 or i == 8:
                        line += " " + board[i]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[i]

                check_winner(W_Conditions, mark)
                if game_over:
                    await ctx.send(mark + " WON!")
                elif count >= 9:
                    await ctx.send("IT'S A TIE!")
                
                #Switch Turns to other player
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1

            else:
                await ctx.send("Make sure you choose a valid position on the board by choosing a number between 1 and 9. The number you choose will represent the position you will mark.") 
        else:
            await ctx.send("Wait for your turn!")
    else: 
        await ctx.send("Please start your own game first!")

def check_winner(W_Conditions, mark):
    global game_over
    for condition in W_Conditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            game_over = True

@tictactoe.error
async def tictactoe_error_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please @'mention two valid discord members in the current server for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players.")

@move.error
async def move_error_handler(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please eneter a VALID position that you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer position")

# Run the client/bot
client.run('Nzg2NzQ1MDA3MDY2NzEwMDE3.X9K3Yg.g0K91cFM9g-BA13mAp2K7aUGJiU')