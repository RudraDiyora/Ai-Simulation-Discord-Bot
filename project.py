import discord
from discord.ext import commands
import random
import asyncio


client = commands.Bot(command_prefix = 't?')
#the bot will to a dm with a dm

damage_over_time = False
blinding = False
user_HP = 10
thunder_HP = 10
effects = [damage_over_time, blinding]

#cards
class Kit:
    Class = "Fighter"
    Name = "Kit"
    Ability = "Cat With Magical Blades"
    Power = 2
    Heal = 0
    Defence = 1
    class Effect_class:
        damage_over_time = True
        blinding = False

    def Attack(self):
        if turn == user:
            pass   
class Cotton_dog:
    Class = "Healer"
    Name = "Cotton Doge"
    Ability = "Heals 1 Health-Point, by removing this card"
    Power = 0
    Heal = 1
    Defence = 0
    class Effect_class:
        damage_over_time = False
        blinding = False
class Sunglasses:
    Class = "Special"
    Name = "Mr.Sunglasses"
    Ability = "When Mr.Sunglasses gets played, the opponet is forced to draw a card at random."
    Power = 1
    Heal = 0
    Defence = 1
    class Effect_class:
        damage_over_time = False
        blinding = True
class Boomer:
    Class = "Defence"
    Name = "BoOmEr"
    Ability = "If you take 1 damage, that damage is nulled and boomer heals you for 1 HP point when destroyed."
    Power = 1
    Heal = 0
    Defence = 3
    class Effect_class:
        damage_over_time = False
        blinding = False

kit = Kit()
cotton_dog = Cotton_dog()
sunglasses = Sunglasses()
boomer = Boomer()
#spiceal effects
characters = [kit, cotton_dog, sunglasses, boomer]

#Makes a function that summons a card from the ThunderHead
def thunder_move():
    cardToSummon = random.choice(characters)
    thunder_hand.append(cardToSummon)
    thunder_field.append(cardToSummon.Name)

#view command       
@client.command()
async def view(ctx, card):
    card = str(card)
    for character in characters:
        if card == character.Name:
            item = character     
            loading = await ctx.send("Loading.")

            for i in range(3):
                await loading.edit(content = "Loading.")
                await asyncio.sleep(.5)
                await loading.edit(content = "Loading..")
                await asyncio.sleep(.5)
                await loading.edit(content = "Loading...")
                await asyncio.sleep(.5)
            await loading.delete()

            em = discord.Embed(title = item.Name, color = discord.Color.gold())
            em.add_field(name = "Power", value = f"{item.Power}")
            em.add_field(name = "Heal", value = f"{item.Heal}")
            em.add_field(name = "Defence", value = f"{item.Defence}")
            if item.Effect_class.damage_over_time == True:
                em.add_field(name = "Effect(s)", value = "Damage Over Time")
            elif item.Effect_class.blinding == True:
                em.add_field(name = "Effect(s)", value = "Blinding")
            
            await ctx.send(embed = em)
            return
        else:
            await ctx.send("There was an error in proscing your viewing request. Make sure the name of the character is excat i.e. caps and all.")
            return
        break

@client.group(invoke_without_command = True)
async def takedown(ctx, extra = None):
    if extra != None:
        return
    global hand, user, turn, turn_value, oppenet


    class Oppenet:
        Name = client
        disaffects_active = False
        class disaffects:
            damage_over_time = False
            blinding = False
    oppenet = Oppenet()

    user = ctx.author
    turn_value = random.randint(1, 2)
    turn = ''
    if turn_value == 1:
        turn = f"{user}"
        await ctx.send(f"{user.name} goes first!")
    elif turn_value == 2:
        turn = f"{client}"
        await ctx.send("Thunderhead goes first!")

    hand = []
    #Sets a varibale that holds 1 card from the Defence, Fighter, Special, and Healer classes
    for character in characters:
        print(character.Name)
        if character.Class == "Fighter":
            fighter_card = character.Name
            hand.append(fighter_card)
        if character.Class == "Defence":
            defense_card = character.Name
            hand.append(defense_card)
        if character.Class == "Special":
            speical_card = character.Name
            hand.append(speical_card)
        if character.Class == "Healer":
            healer_card = character.Name
            hand.append(healer_card)
    
    await user.send(hand)
@takedown.command()
async def use(ctx,*, card):
    global thunder_hand, user_field, thunder_field
    #sets the Users field
    user_field = []

    #sets the AI hand
    thunder_hand = []
    for character in characters:
        if character.Class == "Fighter":
            thunder_fighter_card = character.Name
            thunder_hand.append(thunder_fighter_card)

    for character in characters:
        if character.Name == card:
            card = character.Name

    thunder_field = []
    thunder_field.append(thunder_fighter_card)

    user = ctx.author
    if turn_value == 1:
        #checks if user has the card
        if card not in hand:
            await ctx.send("YOU DON'T HAVE THIS CARD!")
            return None

        await draw(user)

        #intiats code if the user has the card and it is the user's turn
        if card in hand:
            #adds the card to the field
            user_field.append(card)
            #takes the card out of the user's hand, and sends a dm to the user with the new hand.
            hand.remove(card)
            await user.send(hand)

            #sends the field in form of an embed
            em = discord.Embed(title = "TAKDOWN!", color = discord.Color.dark_purple())
            em.add_field(name = user, value = user_field)
            em.add_field(name = "Thunderhead", value = thunder_field)
            field_update = await ctx.send(embed = em)
             
            #switches turn to Thunderhead 
            turn = client 

    if turn == client:

        if oppenet.disaffects_active == True:
            pass
        await ctx.send("WAIT FOR YOUR TURN!!!!")

        em = discord.Embed(title = "TAKDOWN!", color = discord.Color.dark_purple())
        em.add_field(name = user, value = user_field)
        em.add_field(name = "Thunderhead", value = thunder_field)
        field_update = await ctx.send(embed = em)

        thunder_move()
        #switches turn to user
        turn = user
        return

#Fight Command -- 1 Way
@client.command()
async def fight(ctx, card):
    card = str(card)
    user = ctx.author
    if card not in user_field:
        await ctx.send(f"{card.upper} IS NOT ON YOUR FIELD!")
        return
    elif card in user_field:
        #Checks if the opponets field is empty
        if len(thunder_field) == 0:
            #Checks if the card the user placed is a valid card
            for char in characters:
                if char.Name == card.upper or char.Name == card.lower:
                    card = char


            effect_characters = [kit, sunglasses]
            for card in effect_characters:
                if card.Effect_class.blinding == True:
                    #Do blinding effect
                    pass
                elif card.Effect_class.damage_over_time == True:
                    thunder_HP -= card.Effect_class.damage_over_time
                    pass

                else:
                    pass
                    #Damage calculation
                    thunder_HP -= card.Power


    await ctx.send(f"{user} had a succeful hit using {card}! Thunderhead has {thunder_HP_left}!")

async def draw(player):
    player_hand = ""
    #checks who the 'player' is that draws a card
    if player == user:
        player = user
        player_hand = hand
    else:
        player = client
        player_hand = thunder_hand

    #radomizes a class that the card will be drawn from 
    character_classes = ["Fighter", "Defence", "Healer", "Special"]
    draw_card_class = random.choice(character_classes)
    for character in characters:
        if character.Class == draw_card_class:
            player_hand.append(character.Name)



client.run('Nzg2NzQ1MDA3MDY2NzEwMDE3.X9K3Yg.g0K91cFM9g-BA13mAp2K7aUGJiU')