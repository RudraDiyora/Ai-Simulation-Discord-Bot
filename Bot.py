# Import Discord Packages
import discord
from discord.ext import commands
import json 
import os 
import asyncio
import random
from uno import my_hand_var


os.chdir("/Users/abc/Desktop/Code")

# Client (the bot)
client = commands.Bot(command_prefix='t?')
general_channel = client.get_channel(755855737497977073)
print(general_channel)

# Proof that Thunderhead has turned on + basic information about Thunderhead
@client.event
async def on_ready():
    # Commands and Basic Functionality
    general_channel = client.get_channel(755855737497977073)
    await general_channel.send('I am online!')

#REACTION-COMMANDS START HERE

#MODDERATION STARTS HERE
#BLACKLISTING
@client.event
async def on_message(message):
    global msg_true
    msg_true = False
    if message.content.startswith('t?'):
        msg_true = True
    if msg_true == False:
        if message.author == client.user.id:
            return
        elif "hi" in message.content.lower():
            await message.channel.send("WHY???!?!?!")
            return
        else:
            return

    await client.process_commands(message)

# YT-FIGHT ------- WORK IN PROGRESS
@client.command(aliases = ['ytf'])
async def fight(ctx, yt1, yt2, yt3, yt4):
    global yt1_, yt2_, yt3_, yt4_
    yt1_ = str(yt1)
    yt2_ = str(yt2)
    yt3_ = str(yt3)
    yt4_ = str(yt4)

    class ytf_1:
        Power = random.randrange(1, 50)
        HP = random.randrange(1, 100)
    class ytf_2:
        Power = random.randrange(1, 50)
        HP = random.randrange(1, 100)
    class ytf_3:
        Power = random.randrange(1, 50)
        HP = random.randrange(1, 100)
    class ytf_4:
        Power = random.randrange(1, 50)
        HP = random.randrange(1, 100)

    bracket_em = discord.Embed(title = "FIGHT!", color = discord.Color.dark_teal())
    bracket_em.add_field(name = "R-1", value = f"{yt1_} VS. {yt4_}")
    bracket_em.add_field(name = "R-2", value = f"{yt2_} VS. {yt3_}")
    bracket = await ctx.send(embed = bracket_em)

    winner_round_one = ""
    if ytf_1.Power > ytf_4.Power:
        await asyncio.sleep(1)
        winner_round_one = yt1_
        bracket_new_em = discord.Embed(title = "FIGHT!", color = discord.Color.dark_teal())
        bracket_new_em.add_field(name = "R-1-W", value = F"{winner_round_one}")
        await bracket.edit(embed = bracket_new_em)
    elif ytf_1.Power < ytf_4.Power:
        await asyncio.sleep(1)
        winner_round_one = yt4_
        bracket_new_em = discord.Embed(title = "FIGHT!", color = discord.Color.dark_teal())
        bracket_new_em.add_field(name = "R-1-W", value = f"{winner_round_one}")
        await bracket.edit(embed = bracket_new_em)
    
    winner_round_two = ""
    if ytf_2.Power > ytf_3.Power:
        await asyncio.sleep(1)
        winner_round_one = yt2_
        bracket_new_em = discord.Embed(title = "FIGHT!", color = discord.Color.dark_teal())
        bracket_new_em.add_field(name = "R-2-W", value = f"{winner_round_two}")
        await bracket.edit(embed = bracket_new_em)
    elif ytf_2.Power < ytf_3.Power:
        await asyncio.sleep(1)
        winner_round_one = yt3_
        bracket_new_em = discord.Embed(title = "FIGHT!", color = discord.Color.dark_teal())
        bracket_new_em.add_field(name = "R-2-W", value = f"{winner_round_two}")
        await bracket.edit(embed = bracket_new_em)

    if winner_round_one > winner_round_two:
        await asyncio.sleep(1)
        winner = winner_round_one
        braket_new_em = discord.Embed(title = "FIGHT!", color = discord.Color.green())
        braket_new_em.add_field(name = "WINNER!", value = f"{winner_round_one}")
        await bracket.edit(embed = braket_new_em)
    elif winner_round_one < winner_round_two:
        await asyncio.sleep(1)
        winner = winner_round_two
        braket_new_em = discord.Embed(title = "FIGHT!", color = discord.Color.green())
        braket_new_em.add_field(name = "WINNER!", value = f"{winner_round_two}")
        await bracket.edit(embed = braket_new_em)

# Economy System
# Balance Command
@client.command()
async def balance(ctx):
    await open_account(ctx.author)
    user =  ctx.author
    users = await get_bank_data()

    Wallet_amt = users[str(user.id)]["Wallet"]
    Bank_amt = users[str(user.id)]["Bank"]

    em = discord.Embed(title = f"{ctx.author.name}'s Balance", color = discord.Color.red())
    em.add_field(name = "Wallet balance", value = Wallet_amt)
    em.add_field(name = "Bank balance", value = Bank_amt)
    await ctx.send(embed = em)

# Beg Command
@client.command()
@commands.cooldown(1, 90, commands.BucketType.user)

async def beg(ctx):
    await open_account(ctx.author)

    users = await get_bank_data()
    
    user =  ctx.author

    earnings = random.randrange(100)
    
    await ctx.send(f"A generous soul gave you {earnings} coins!!!")  
    users[str(user.id)]["Wallet"] += earnings
    
    
    with open("Bot_Bank.json", "w") as f:
        json.dump(users,f)  

# Withdraw command. Bank --> Wallet
@client.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def withdraw(ctx,amount = None):
    await open_account(ctx.author)

    if amount == None:
        await ctx.send("Please enter the amount")
        return      

    balance = await update_wallet(ctx.author)  

    amount = int(amount)

    if amount>balance[1]:
        await ctx.send("You don't a lot of coins!")
        return
    if amount<0:
        await ctx.send("You can't withdraw a negitve amount of coins!")
        return
        
    await update_wallet(ctx.author,amount)    
    await update_wallet(ctx.author,-1*amount,"Bank")
    await ctx.send(f"You withdrew {amount} coins!")
   
# Deposit Command. Wallet --> Bank
@client.command(aliases = ["dep"])
@commands.cooldown(1, 60, commands.BucketType.user)

async def deposit(ctx,amount = None):
    await open_account(ctx.author)

    if amount == None:
        await ctx.send("Please enter the amount")   
        return

    balance = await update_wallet(ctx.author)

    if amount == "all":
        amount = balance[0]

    amount = int(amount)
    if amount>balance[0]:
        await ctx.send("You don't a lot of coins!")
        return
    if amount<0:
        await ctx.send("You can't withdraw a negitve amount of coins!")
        return
        
    await update_wallet(ctx.author,-1*amount,"Bank")
    await update_wallet(ctx.author,amount,"Wallet")
    await ctx.send(f"You deposited {amount} coins!")

# Send Money Command
@client.command()
@commands.cooldown(1, 180, commands.BucketType.user)

async def send(ctx,member:discord.Member,amount = None):
    await open_account(ctx.author)
    await open_account(member)

    if amount == None:
        await ctx.send("Please enter the amount")
        return

    balance = await update_wallet(ctx.author)

    amount = int(amount)
    if amount>balance[1]:
        await ctx.send("You don't a lot of coins!")
        return
    if amount<0:
        await ctx.send("You can't withdraw a negitve amount of coins!")
        return
        
    await update_wallet(ctx.author,-1*amount,"Bank")
    await update_wallet(member,amount,"Bank")
    await ctx.send(f"{ctx.author.mention} gave {amount} coins to {member.mention}")

# Rob/Steal Command
@client.command()
@commands.cooldown(1, 180, commands.BucketType.user)
async def steal(ctx,member:discord.Member):
    await open_account(ctx.author)
    await open_account(member)

    balance = await update_wallet(member)

    if balance[0]<100:
        await ctx.send("Leave the poor soul alone This person dosen't have a lot of coins!")
        return

    steal_amt = random.randrange(0, balance[0])

        
    await update_wallet(ctx.author,steal_amt)
    await update_wallet(member,-1*steal_amt)
    await ctx.send(f"{ctx.author.mention} stole {steal_amt} coins from {member.mention}! {member.mention} is probally mad!😡")

# Slots Command
@client.command()
@commands.cooldown(1, 30, commands.BucketType.user)
async def slots(ctx,amount = None):
    await open_account(ctx.author)

    if amount == None:
        await ctx.send("Please enter the amount")
        return

    balance = await update_wallet(ctx.author)

    amount = int(amount)
    if amount>balance[0]:
        await ctx.send(f"You don't have {amount} coins! Don't try to cheat the system! :angry: ")
        return
    if amount<0:
        await ctx.send("You can't bet a negitve amount of coins!")
        return
    
    final = []
    for i in range(3):
        a = random.choice(['🎄','🎁 ','🔔','🏔'])

        final.append(a)

    await ctx.send(str(final))
    
    if final[0] == final[1] and final[1] == final[2] and final[0] == final[2] and final[2] == final[3] and final[0] == final[3]: 
        await update_wallet(ctx.author,2*amount)
        await ctx.send(f"{ctx.author.mention} Won!")
    else:
        await update_wallet(ctx.author,-1 *amount)
        await ctx.send(f"{ctx.author.mention} Lost!")

# Economy System Store
mainshop =[{"Name": "Watch", "Price": 50, "Description": "Flex this amazing watch that includes a basic design, but still retains an adequate lookz!"},
           {"Name": "Keyboard", "Price": 150, "Description": "Small and high-quality keyboard that keeps your hands comfortable!"},
           {"Name": "Yeeter", "Price": 500, "Description": "This Yetter gives you full authority to call yourself a Yeeter!"},
           {"Name": "BFA", "Price": 100, "Description": "A basic fishing rod for new fishers!"}]

# Shop Command
@client.command()
async def shop(ctx):
    em = discord.Embed(title = "Shop")

    for item in mainshop:
        name = item["Name"]
        price = item["Price"]
        description = item["Description"]
        em.add_field(name = name, value = f"${price} | {description}")

    await ctx.send(embed = em)

# Buy Command
@client.command()
async def buy(ctx, item, amount = 1):
    await open_account(ctx.author)

    res = await buy_this(ctx.author, item, amount)

    if not res[0]:
        if res[1] == 1:
            await ctx.send("Ya I don't think I sell that!")
            return
        if res[1] == 2:
            return

    await ctx.send(f"{ctx.author.mention} just bought {amount} {item}!")

# Shelf Command
@client.command()
async def shelf(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["bag"]
    except:
        bag = []


    em = discord.Embed(title = f"{ctx.author.name}'s Bag")
    for item in bag:
        name = item["item"]
        amount = item["amount"]

        em.add_field(name = name, value = amount)    

    await ctx.send(embed = em) 

# buy_this helper function
async def buy_this(user,item_name,amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["Name"].lower()
        if name == item_name:
            name_ = name
            price = item["Price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_wallet(user)

    if bal[0]<cost:
        return [False,2]


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            obj = {"item":item_name , "amount" : amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item" : item_name , "amount" : amount}
        users[str(user.id)]["bag"] = [obj]        

    with open("Bot_Bank.json","w") as f:
        json.dump(users,f)

    await update_wallet(user,cost*-1,"Wallet")

    return [True,"Worked"]

# Sell Command you get 90% of the coins that the orginal item cost
@client.command()
async def sell(ctx,item,amount = 1):
    await open_account(ctx.author)

    res = await sell_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("You can't sell something you don't have!")
            return
        if res[1]==2:
            await ctx.send(f"You don't have {amount} {item} in your shelf.")
            return
        if res[1]==3:
            await ctx.send(f"You don't have {item} in your shelf.")
            return

    await ctx.send(f"You just sold {amount} {item}.")

# Sell_this helper function
async def sell_this(user,item_name,amount,price = None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["Name"].lower()
        if name == item_name:
            name_ = name
            if price==None:
                price = 0.9 * item["Price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_wallet(user)


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False,2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            return [False,3]
    except:
        return [False,3]    

    with open("Bot_Bank.json","w") as f:
        json.dump(users,f)

    await update_wallet(user,cost,"Wallet")

    return [True,"Worked"]

# Status command
@client.command(aliases = ["c"])
async def coins(ctx,x = 3):
    users = await get_bank_data()
    leader_board = {}
    total = []
    for user in users:
        name = int(user)
        total_amount = users[user]["Wallet"] + users[user]["Bank"]
        leader_board[total_amount] = name
        total.append(total_amount)

    total = sorted(total,reverse=True)    

    em = discord.Embed(title = f"Top {x} Richest People" , description = "This is decided on the amount of coins in your wallet and your bank.",color = discord.Color(0xfa43ee))
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        member = client.get_user(id_)
        name = member
        em.add_field(name = f"{index}. {name}" , value = f"{amt}",  inline = False)
        if index == x:
            break
        else:
            index += 1

    await ctx.send(embed = em)

# Black Jack Command
# User Generation   
@client.command(aliases = ['bj'])
async def blackjack(ctx, amount = None):
    await open_account(ctx.author)
    
    if amount == None:
        await ctx.send("Please enter an amount!")
        return

    balance = await update_wallet(ctx.author)

    amount = int(amount)
    if amount>balance[0]:
        await ctx.send(f"You don't have {amount} coins! Don't try to cheat the system! :angry: ")
        return
    if amount<0:
        await ctx.send("You can't bet a negitve amount of coins!")
        return  

# Card Symbols
    h = "♡"
    s = "♤"
    c = "♧"
    d = "♢"
    final = []
    for i in range(2):
        Ace = int(11)
        a = random.choice([2,3,4,5,6,7,8,9,10,Ace, 2,3,4,5,6,7,8,9,10,Ace, 2,3,4,5,6,7,8,9,10,Ace, 2,3,4,5,6,7,8,9,10,Ace])

        final.append(a)
    
# Card Symbol Random Generation
    for i in range(4):
        sign = random.choice([h, s, c, d])
    for i in range(4):
        sign2 = random.choice([h, s, c, d])
    for i in range(4):
        sign3 = random.choice([h, s, c, d])
    for i in range(4):
        sign4 = random.choice([h, s, c, d])


    user_amt = final
    U_A_amt = user_amt[0]
    U_B_amt = user_amt[1]
    await ctx.send(f"{ctx.author.name} = {sign}{user_amt[0]} {sign2}{user_amt[1]}")
# Bot Generation Amount
    final = []
    for i in range(2):
        Ace = int(11)
        a = random.choice([2,3,4,5,6,7,8,9,10,Ace, 2,3,4,5,6,7,8,9,10,Ace, 2,3,4,5,6,7,8,9,10,Ace, 2,3,4,5,6,7,8,9,10,Ace])

        final.append(a)

    bot_amt = final
    B_A_amt = bot_amt[0]
    B_B_amt = bot_amt[1]
    await ctx.send(f"Thunerhead = {sign3}{bot_amt[0]} {sign4}{bot_amt[1]}")

    user_total_amt = int(U_A_amt) + int(U_B_amt)
    bot_total_amt = int(B_A_amt) + int(B_B_amt)

    if user_total_amt>21:
        await ctx.send(f"{ctx.author.mention}, you had a bust! If you have been living under a rock, that means your numbers are greater than 21 in total. Thunderhead wins by default!")
        await update_wallet(ctx.author,-1*amount)        
    if bot_total_amt>21:
        await ctx.send("Thunderhead had a bust. If you have been living under a rock, that means your numbers are greater than 21 in total. Thunderhead wins by default!")
        await update_wallet(ctx.author,2*amount)
    if user_total_amt>21 and bot_total_amt>21:
        await ctx.send(f"{ctx.author.mention} had a bust and so did Thunderhead!")

    if user_total_amt>bot_total_amt: 
        await update_wallet(ctx.author,2*amount)
        await ctx.send(f"{ctx.author.mention} Won!")

    if user_total_amt == bot_total_amt:
        await ctx.send(f"{ctx.author.mention} it's a tie!")

    if user_total_amt<bot_total_amt:
        await update_wallet(ctx.author,-1*amount)
        await ctx.send(f"{ctx.author.mention} Lost! Better luck next time!")

# Lottery Information Command
@client.command(aliases = ['li'])
async def lottery_info(ctx):
    await ctx.send("If you win a lottery, you an get up to 1000 coins! However, if you don't win the lottery, you will lose up to 500 coins! The number range of the lottery is from 0 - 50.")

# Lottery_enter Command 
@client.command(aliases = ['le'])
async def lottery(ctx, number = None):
    await open_account(ctx.author)

    if number == None: 
        await ctx.send(f"{ctx.author.name} YOU. CAN'T. ENTER. A. LOTTERY. IF. YOU. DON'T. GIVE. A. LOTTERY. N-U-M-B-E-R!")
        return

    for i in range(1):
        lose_amt = random.choice([50,100,150,200,250,300,350,400,450,500])
    for i in range(1):
        win_amt = random.choice([100,200,300,400,500,600,700,800,900,1000])

    balance = await update_wallet(ctx.author)

    if balance[0]<lose_amt:
        await ctx.send(f"{ctx.author.mention} this is a very risky play. I will prevent you from entering THIS lottery. Gain so more money and enter another lottery.")
        return

    number = int(number)
    if number != int(number):
        await ctx.send(f"DUDE! {number} is not a number. Please enter a valid integer!")   
        return
    if number>50:
        await ctx.send(f"{number} is not a number that is greater than 50. Use t?help lottery for more information!")
        return
    if number<0:
        await ctx.send(f"{number} is not a number that is less than 0. Use t?help lottery for more information!")
        return

    for i in range(1):
        lottery_num = random.choice([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50])


    if lottery_num == number:
        await update_bank(ctx.author,win_amt)
        await ctx.send(f"{ctx.author.mention} WON THE LOTTERY! OMG! {ctx.author.mention} WON {win_amt} COINS!")

    if lottery_num != number:
        await update_wallet(ctx.author,-1*lose_amt)
        await ctx.send(f"{ctx.author.mention} LOST THE LOTTERY! YIKES! {ctx.author.mention} LOST {lose_amt} COINS! The lottery number was {lottery_num}!")

# Football Command ---- On_Hold/Work_In_Progress
@client.command(aliases = ['fb'])
async def football(ctx):
    em = discord.Embed(title = "FootBall Teams", color = discord.Color.green())
    # NFC
    em.add_field(name = "NFC-West", value = "S.Seahawks \nLA.Rams \nA.Cardinals \nSF.49ers")
    em.add_field(name = "NFC-South", value = "NO.Saints \nTB.Buccaneers \nC.Panthers \nA.Falcons")
    em.add_field(name = "NFC-East", value = "W.Football Team \nD.Cowboys \nNY.Giants \nP.Eagles")
    em.add_field(name = "NFC-North", value = "GB.Packers \nC.Bears \nM.Vikings \nD.Lions")
    # AFC
    em.add_field(name = "AFC-West", value = "KC.Chiefs \nLV.Raiders \nLA.Chargers \nD.Broncos")
    em.add_field(name = "AFC-South", value = "T.Titans \nI.Colts \nH.Texans \nJ.Jaguars")
    em.add_field(name = "AFC-East", value = "B.Bills \nM.Dolphins \nNE.Patriots \nNY.Jets")
    em.add_field(name = "AFC-North", value = "P.Steelers \nB.Ravens \nC.Browns \nC.Bengals")

    await ctx.send("Welcome to the football game! You will have to select a football team from the 32 NFL teams!")
    await ctx.send(embed = em)

#Thunderhead Command
@client.command()
async def Thunderhead(ctx):
    global power_difference

    for i in range(1):
        Thunderhead_power = random.randrange(1,500)
    for i in range(1):
        User_power = random.randrange(1,500)

    msg = await ctx.send("You wouldn't dare!!")

    power_difference = Thunderhead_power - User_power
    
    if power_difference<0:
        power_difference = User_power - Thunderhead_power

    await asyncio.sleep(2)

    if Thunderhead_power>User_power:
        await msg.edit(content = f"You are pathetic. You only have the power of {User_power} whereas I have the power of {Thunderhead_power}!")
        await asyncio.sleep(1)
        await msg.edit(content = "HEHE I AM STRONGER!!")
        await asyncio.sleep(1)
        await msg.edit(content = "TRY ME!!")
        await asyncio.sleep(2)
        await msg.delete()
    if Thunderhead_power<User_power:
        await msg.edit(content = f"You were lucky! IT WAS A GLITCH!")
        await asyncio.sleep(1)
        await msg.edit(content = "UGH!")
        await asyncio.sleep(1)
        await msg.edit(content = "GLITCH!")
        await asyncio.sleep(2)
        await msg.delete()
        await asyncio.sleep(3)
        await open_account(ctx.author)
        await update_wallet(ctx.author,-1/2*Thunderhead_power)

        user =  ctx.author
        users = await get_bank_data()

        Wallet_amt = users[str(user.id)]["Wallet"]
        # Bank_amt = users[str(user.id)]["Bank"]

        em = discord.Embed(title = f"{ctx.author.name}'s Balance", color = discord.Color.magenta())
        em.add_field(name = "Wallet balance", value = Wallet_amt)
        await ctx.send(embed = em)
        await asyncio.sleep(2)
        await msg.delete()
        
#Uno
@client.group(invoke_without_command=True)
async def uno(ctx, oppenet):
    global my_hand, your_hand, card_1, card_2, card_3, card_4, card_5, card_6, card_7, start_em, start_off
    if oppenet == None:
        await ctx.send("Who ya tryin' play uno with?")
        return
    
    # Randomly chooses 7 cards for me(user)
    for i in range(1):
        card_1 = random.choice(my_hand_var)
        card_2 = random.choice(my_hand_var)
        card_3 = random.choice(my_hand_var)
        card_4 = random.choice(my_hand_var)
        card_5 = random.choice(my_hand_var)
        card_6 = random.choice(my_hand_var)
        card_7 = random.choice(my_hand_var)
        my_hand = [card_1, card_2, card_3, card_4, card_5, card_6, card_7]

    # Randomly chooses 7 cards for oppenet
    # for i in range(1):
    #     card_1 = random.choice(my_hand_var)
    #     card_2 = random.choice(my_hand_var)
    #     card_3 = random.choice(my_hand_var)
    #     card_4 = random.choice(my_hand_var)
    #     card_5 = random.choice(my_hand_var)
    #     card_6 = random.choice(my_hand_var)
    #     card_7 = random.choice(my_hand_var)
    #     your_hand = [card_1, card_2, card_3, card_4, card_5, card_6, card_7]

    # Random Start-Off Var
    start_off = random.choice(my_hand_var)
    em = discord.Embed(title = "UNO!", color = discord.Color.dark_teal())
    em.add_field(name = "START-OFF", value = f"{start_off}")

    # DM's cards to user, and oppenet
    await ctx.author.send(my_hand)
    # await oppenet.send(your_hand)
    start_em = await ctx.send(embed = em)
@uno.command()
async def play(ctx, *, card_play):
    global current_card_holder_var, new_em, newer_em

    card = str(card_play)

    if card == None:
        await ctx.send("YOU HAVE TO CHOOSE A CARD TO PLAY!")
        return
    if card not in my_hand:
        await ctx.send("You don't have that card in your hand. Check you dm's.")
        return 

# Checks if the card is in my-hand
    elif card in my_hand:
        current_card = f"{card}"

# Sets up a check system for the uno logic
        current_card_holder_var = ""
        if card_play[:3] == "Red":
            current_card_holder_var = "0 " + card_play
        elif card_play[:4] == "Blue":
            current_card_holder_var = "3 " + card_play
        elif card_play[:5] == "Green":
            current_card_holder_var = "7 " + card_play
        elif card_play[:6] == "Yellow":
            current_card_holder_var = "27 " + card_play


# Checks if the color is the same as the start-off card or the current-card
        # card_check = card[:3] == current_card[:3]
        # print(card)
        # print(card_check)
        # print(current_card_holder_var)
        if card[1] == current_card_holder_var[2] or card[1] == current_card_holder_var[2] or card[1] == current_card_holder_var[2] or card[1] == current_card_holder_var[3]:
            my_hand.remove(card)
            await ctx.author.send(my_hand)
            new_em = discord.Embed(title = "UNO!", color = discord.Color.dark_teal())
            new_em.add_field(name = "CURRENT-CARD", value = current_card)
            await start_em.edit(embed = new_em)
        else: #if card[1] != current_card_holder_var[2] or card[1] != current_card_holder_var[2] or card[1] != current_card_holder_var[2] or card[1] != current_card_holder_var[3]:
            await ctx.send(F"DOES {card}'S COLOR WITHT HE CURRENT CARD'S NUMBER COLOR??? NO!!!!")

        if len(my_hand) < 1:
            newer_em = discord.Embed(title = "UNO!", color = discord.Color.dark_teal())
            newer_em.add_field(name = "CURRENT-CARD", value = f"{card}")
            newer_em.add_field(name = "UNO!", value = f"{ctx.author}")
            await start_em.edit(embed = newer_em)
        if len(my_hand) == None:
            await new_em.delete()
            await newer_em.delete()
            em = discord.Embed(title = "UNO!", color = discord.Color.dark_orange())
            em.add_field(name = "WINNER!", value = f"{ctx.author}")

#MY-CARD-GAME COMMAND

    

# open_account helper function
async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else: 
        users[str(user.id)] = {}        
        users[str(user.id)]["Wallet"] = 0   
        users[str(user.id)]["Bank"] = 0

    with open("Bot_Bank.json", "w") as f:
        json.dump(users,f)
    return True


async def get_bank_data():
    with open("Bot_Bank.json", "r") as f:
        users = json.load(f)

    return users 

# Update user bank and/or wallet information
async def update_wallet(user,change = 0,mode = "Wallet"):
    users = await get_bank_data()
    users[str(user.id)][mode] += change
    with open("Bot_Bank.json", "w") as f:
        json.dump(users,f)
    
    balance = [users[str(user.id)]["Wallet"],users[str(user.id)]["Bank"]]
    return balance

async def update_bank(user,change = 0,mode = "Bank"):
    users = await get_bank_data()
    users[str(user.id)][mode] += change
    with open("Bot_Bank.json", "w") as f:
        json.dump(users,f)
    
    balance = [users[str(user.id)]["Wallet"],users[str(user.id)]["Bank"]]
    return balance

# Runs the client/bot
client.run('Nzg2NzQ1MDA3MDY2NzEwMDE3.X9K3Yg.g0K91cFM9g-BA13mAp2K7aUGJiU')