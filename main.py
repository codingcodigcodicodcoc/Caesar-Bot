import os
import random
import discord
import music
import time
from discord.ext import commands
from discord.ext.commands import has_permissions
from keep_alive import keep_alive

my_secret = os.environ['TOKEN']

cogs = [music]

bot = commands.Bot(command_prefix="lv.", intents=discord.Intents.all())


@bot.event
async def on_ready():
  print('Here comes {0.user}'.format(bot))
  global bal
  global mem
  bal = []
  mem = []

for i in range(len(cogs)):
  cogs[i].setup(bot)

@bot.command()
async def bal(ctx):
  x = mem.index(ctx.author)
  await ctx.send(f'{ctx.author.name}\'s profile')
  await ctx.send(f'>>> Purse Money : {bal[x]}')

@bot.command()
async def color(ctx):
  def check(y):
    return y.author == ctx.author and y.channel == ctx.channel
  rand = random.randrange(0,7)
  if rand == 0:
    str = ':red_square:'
    await ctx.send(str)
  if rand == 1:
    str = ':orange_square:'
    await ctx.send(str)
  if rand == 2:
    str = ':yellow_square:'
    await ctx.send(str)
  if rand == 3:
    str = ':green_square:'
    await ctx.send(str)
  if rand == 4:
    str =':blue_square:'
    await ctx.send(str)
  if rand == 5:
    str = ':purple_square:'
    await ctx.send(str)
  if rand == 6:
    str = ':black_large_square:'
    await ctx.send(str)
  await ctx.send("What is the color of this square?")
  x = str.index("_")
  print(str[1:x])
  y = await bot.wait_for("message", check=check)
  print(y.content.lower())
  if (str[1:x]) == y.content.lower() or (str[1:2]) == y.content.lower():
    await ctx.send('win')
  else:
    await ctx.send('lose')

@bot.command()
async def coin(ctx, arg, val):
  val = valcheck(val, ctx.author)
  num = random.randrange(0, 2)
  if arg == "tails" or arg == "heads" or arg == "tail" or arg == "head":
    if num == 0 and (arg == "heads" or arg == "head"):
      addMoney(val, ctx.author)
      await ctx.send(f'Heads, you guessed correct! You have won {val}')
    elif num == 0 and (arg != "heads" or arg != "head"):
      removeMoney(val, ctx.author)
      await ctx.send(f'Heads, you are wrong! You have lost {val}')
    if num == 1 and (arg == "tails" or arg == "tail"):
      addMoney(val, ctx.author)
      await ctx.send(f'Tails, you guessed correct! You have won {val}')
    elif num == 1 and (arg != "tails" or arg != "tail"):
      removeMoney(val, ctx.author)
      await ctx.send(f'Tails, you are wrong! You have lost {val}')
  else:
    await ctx.send("You need to pick heads or tails")

@bot.command()
async def list(ctx):
  for x in mem:
    y = mem.index(x)
    await ctx.send(f'>>> {x} has a balance of {bal[y]}')

@bot.command()
async def add(ctx, user: discord.Member):
  check = 0
  for x in mem:
    if x == user:
      await ctx.send('This user has already been added')
      check = 1
      return
  if check != 1:
    mem.append(user)
    bal.append(500)
    await ctx.send(f'Added {user.mention}')

@bot.command()
async def blackjack(ctx, arg):
  gameNotLost = True
  def check(response):
    return response.author == ctx.author and response.channel == ctx.channel
  def convertCard(num):
    if num == 2:
      return "<:2c:984228235426533426>"
    if num == 3:
      return "<:3c:984228236571594792>"
    if num == 4:
      return "<:4c:984228237511106560>"
    if num == 5:
      return "<:5c:984228238618398800>"
    if num == 6:
      return "<:6c:984228239595667476>"
    if num == 7:
      return "<:7c:984228240539394108>"
    if num == 8:
      return "<:8c:984228241642512404>"
    if num == 9:
      return "<:9c:984228242770759690>"
    if num == 10:
      return "<:10c:984228244142301244>"
    if num == "J":
      return "<:Jc:984228246650495017>"
    if num == "Q":
      return "<:Qc:984228249179656212>"
    if num == "K":
      return "<:Kc:984228248131108864>"
    if num == "A":
      return "<:Ac:984228245383835649>"
  def addTotal(arr):
    val = 0
    for i in arr:
      arrval = arr[i]
      exc = arrval[2:3]
      if exc == "J" or exc == "Q" or exc == "K":
        exc = 10
      if exc == "A":
        exc = 11
      val = val + exc
      if val <= 21:
        return True
      if val > 21:
        return False
  count = 0
  card = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, "J", "J", "J", "J", "Q", "Q", "Q", "Q", "K", "K", "K", "K", "A", "A", "A", "A"]
  used = []
  dealerhand = []
  playerhand = []
  for i in range(52):
    used.append(0)
  await ctx.send("Dealer hand:")
  while count < 2:
    cont = False
    draw = random.randrange(0,52)
    if used[draw] == 0:
      dealerhand.append(convertCard(card[draw]))
      used.insert(draw, 1)
      count = count+1
      cont = True
    if count == 1 and cont == True:
      d = await ctx.send(f'>>> {dealerhand[0]}')
    elif count == 2 and cont == True:
      await d.edit(content=f'>>> {dealerhand[0]} <:hidden:984230599621476363>')
  count = 0
  await ctx.send("Your hand:")
  while count < 2:
    cont = False
    draw = random.randrange(0,52)
    if used[draw] == 0:
      playerhand.append(convertCard(card[draw]))
      used.insert(draw,1)
      count = count+1
      cont = True
    if count == 1 and cont == True:
      startHand = await ctx.send(f'>>> {playerhand[0]}')
    elif count == 2 and cont == True:
      await startHand.edit(content = f'>>> {playerhand[0]} {playerhand[1]}')
  times = 1
  while gameNotLost == True:
    curHand = startHand.content.lower()
    await ctx.send("Hit or Stay?")
    response = await bot.wait_for("message", check=check)
    if response.content.lower() == "Hit" or response.content.lower() == "hit" or response.content.lower() == "h":
      draw = random.randrange(0,52)
      if used[draw] == 0:
        times = times + 1
        playerhand.append(convertCard(card[draw]))
        used.insert(draw,1)
        await startHand.edit(content = f'{curHand} {playerhand[times]}')
        gameNotLost = addTotal(playerhand)
  print(arg)

@bot.command()
async def dadjoke(ctx):
    num = random.randrange(0, 10)
    if num == 0:
        await ctx.send(
            'There was once a man that had never eaten a hotdog with toppings before, but now when he eats his hotdogs he knows to relish it.'
        )
    if num == 1:
        await ctx.send(
            'There was once a man with very dry lips, every hour or so he must apply vaseline to his lips to keep it from bleeding. Before he left his house, he applied his vaseline, and headed out to meet with his girlfriend and her family. When he arrived, the first thing he noticed was a monstrous pile of dirty dishes in the kitchen sink. When he inquired about it, the father of his girlfriend stated,"Whoever speaks first at the dinnertable must wash those dishes." With an awkward exchange of glances, he, his girlfriend, and her parents agreed. After 2 minutes of silence, the man has an idea. He suddenly goes to his girlfriend and starts railing her, like no filter, raw shit. The mother and father looked horrified, yet did not utter a word. The man then did the same to his girlfriends mother, this time his girlfriend and her father were furious, yet silent still. But just then, after around an hour, he felt is lips cracking. He quickly pulled out his vaseline to which the father replied,"WHOA WHOA, ALRIGHT, I WILL DO THE DISHES" '
        )
    if num == 2:
        await ctx.send(
            'A man was on a relatively hot streak at his bowling game, and started whooping and hollering his achievments to all who would hear. Unfortunately, the boss of the joint was a rather sensitive dude who was intolerant to arrogance and profane language. So when the man said,"God fucking damn it, the last pin is still up." The boss picked him up and threw him down the lane, knocking down the last pin. Afterwards, the man stayed quiet at his bowling game, knowing he could have been killed, but he was spared.'
        )
    if num == 3:
        await ctx.send(
            'The mafia boss acknowledged my achievements and sent me on an overnight fishing trip free of charge, the only hiccup was that there was no lodging anywhere so I had to sleep on my boat in the water. I was sent to sleep with the fish.'
        )
    if num == 4:
        await ctx.send(
            'If Dwayne Johnson forces you onto a fully erect pornstar, is this considered being stuck between a Rock and a hard place?'
        )
    if num == 5:
        await ctx.send(
            'A man had recently been caught embezzling money and was being chased after by the cops and their dogs. He hated the fact that all this easy money was going to waste, with each tep he took away from his register. He was almost out of breath when he reached the train junction and leaped onto a car carrying Thanksgiving food items, losing the guards. He was on the gravy train.'
        )
    if num == 6:
        await ctx.send(
            'A laboratory offered $1,000,000 to any volunteer who would test their product. A man eagerly said yes and headed to their facilities to take what he thought to be easy money. Unfortunately, this laboratory specialized in prosthetics for destroyed limbs, and the volunteer money ended up costing him an arm and a leg.'
        )
    if num == 7:
        await ctx.send(
            'There is actually a historical misconception about the death of Julius Caesar. Brutus had already told Caesar of the plans for his murder and recommended that he escape, but he did not tell him when it would happen. He thought he had the entire day to make preparations but by then it was too late. When the time came and the knives were drawn, a surprised Caesar looked at his clock and asked,"At two, Brutus?"'
        )
    if num == 8:
        await ctx.send(
            'A pair of Siamese twins that were joined by the shoulder enlisted to become soldiers in WW2. They endured countless troubles in the trials of war, but still they remained resilient as they were brothers in arms.'
        )
    if num == 9:
        await ctx.send(
            'An arsonist, a rapist, a sadist, and a masochist met in a park. the arsonist spots a cat and suggest they burn it. The rapist stops him and says,"Fuck it, first!" The sadist then offers,"How about we do all of that and insult its parents while we do it!" The masochist says, "meow"'
        )


@bot.command()
async def hitonme(ctx):
    num = random.randrange(0, 15)
    if num == 0:
        await ctx.send('I am going to turn your dairy farm into a creamery.')
    if num == 1:
        await ctx.send(
            'I hope you like bilinguals because I will speak french in between your legs'
        )
    if num == 2:
        await ctx.send('Are you a tumor? Because you are growing on me')
    if num == 3:
        await ctx.send(
            'Are you a fire alarm? Because you are really fucking loud and annoying'
        )
    if num == 4:
        await ctx.send('If you ever need a place to sit call me')
    if num == 5:
        await ctx.send('i am in your home')
    if num == 6:
        await ctx.send(
            'Do you ride horses backwards? because you seem like the reverse cowgirl type.'
        )
    if num == 7:
        await ctx.send(
            'I am kind of like Indiana Jones, if you let me into your cave I would raid it like a lost ark.'
        )
    if num == 8:
        await ctx.send(
            'When I meet up with a professor, I expect to get mind blown. But when I am with you, the expectation is the same, but my mind is out of the picture.'
        )
    if num == 9:
        await ctx.send(
            'Something about you reminds me of Christian Bale, because when I see you, my Dark Knight Rises'
        )
    if num == 10:
        await ctx.send(
            'If you are my job, I would not mind working overtime, all the time.')
    if num == 11:
        await ctx.send(
            'Maybe it is because you are a christian girl, but you sure do know how to turn the other cheek.'
        )
    if num == 12:
        await ctx.send(
            'So you are agnostic, huh? Then, if you let me, I will do something to you to convince you that God does not exist'
        )
    if num == 13:
        await ctx.send(
            'Are you a fan of wrestling? Because I can show you an amazing chokehold technique.'
        )
    if num == 14:
        await ctx.send(
            'ẅ̴̩̹̲̟̺͕̬̦́̔͜͜ͅh̴̖̱̩͖̹̤̖̰͍͍̻̾̓ö̶̼̘͓͕̠̖́̈̿̀̈́͗͘ͅm̸̮͎̈́́͐̚̕̚͝͝ ̸̡̛̼̹̣͔̮͔̏̾͊̃̌̉̅͆ä̸̞̝͖́m̸̳̗̬̭̝̲̞̣̼̽̃̀̅̈́̀̈̇͛͒͑̄͛̚͝ő̸͓͇͈̥͓́̈̔̑̾̍̓́͌͝͝͝ń̷̡̧̜̱͔̳̗̟̯̳̟̼͗͐́̂̾̋̋g̶̨̻͇̰̲͈͊̓̾̐̂̋́̔̎͠͠ś̶̡̞̣͎̦͕̖̥̰̯̮̃͒̍̎̑͒͊͛̋̈́̕͜t̸̼͉̯̼̬͕͔̻͎̀͌͋́͝͝͝͠ ̴̨̛̱̫̻̜̘̲̱͎̳͑̌̀̊͗̾̆̋ỳ̶̡̥͓̖̹̪̟̹̝͙̰̙̤ͅơ̶̞̖̱̦̥̈́͗̋̀͆̊̍̕u̴̠̲͓͑̑̇̽̓ ̸̛̬̰̭̗̘̜͕̲͉͎̮̈́̔̌̓̑m̴̡̢̧̧̢͔̯̣͚͍̼̼̫͉̐̈́é̴͎̥̱͙͚͖̰̲̜̣̯̥̓̅̎̓̄͊̑ͅr̷͔̟̟̪̩͈̎̍̈̇́̆͒̊̓̉̊ȩ̴̦̪̳̝̲̲͖̞̗̦̥̏̔͗͒̃̀̍́̄͛̚ ̴͔̞̫͔͖̀̐͂̇̈́͋̃̍̈́̓̇̒͜͠m̴̡͈̪̳̲͇̤̮̺̅̀͛̈̈́́̉͒̈́͋͂̓͘͝͝o̴̙̠͔͙̻͚̗͍̫̠̮̗̙̠̐̉̾͂̀̀̚ͅr̶̥͓̤̼͉̟̔t̸̨̗̤͕̥̰̦̬̗̻̰̐̏̓̋̎͋̓̈́̋̑ä̴̧̛̛̬̥̫͉́̀̌̓͌̓̊̅̃̾͆́l̸̫̟͎̃͑̄̌͌̈̓̃̈́̂͜͝͝s̶̢̥̥̙̠͔̪̹̝̻̗͂̎͒̊̿̈́̎̄̈̂̽̕͠ ̸̛̲̻̫͕̰́̿̉́͆̇̄̿͗̇̇́͘d̵̫̈́̈͜į̸̻̮̦͂̐̎͌͗s̷̛̯͙͎͙̱̓̏͒t̶̗͛̃̈̎͘ų̴̃̎̆̾́̽̈́̀́͊́͑͘͝ṟ̵̡̣̖̟̤̘̬̝͊ͅb̵͔̹̮̫̥̥͖͓̬̬̘̯̝͊͘͜s̷̛̫͓̋̆̿̿̂͛̔̉̑̆͌̕͝ ̵̡̺͈̤̜̼̭̼͖̱̈́̿̌͒̔̆́͜m̷̬̖͉̣͉̦͖̬̻̲͓̥̒̈̂̆͜͝͝ͅͅy̶̛̯̭̮͐̈́̾̒̌̔́ ̶̡̛̳̭̱͈͍̝̪̻s̵̠̈́̃͗͌̎͆͒̚͝͝l̵̡̡̛͔͉̰̳͕͍̖̻̽̋͊̏̀͆͂̊̐̎ͅữ̸̡̦͇̦̠̤̘̖̜͌̿͒̐̓͆̈́̒̓̚͜ͅͅͅṃ̸̳̓̉̐̅̅͐́̚͠͝b̷̢̨̋͂̋̐̋͘ͅe̸͓̻͒̈́̋̽̇̚ŗ̵̭͉̐̄'
        )

def addMoney(val, user):
  x = mem.index(user)
  bal[x] = bal[x] + int(val)

def removeMoney(val, user):
  x = mem.index(user)
  bal[x] = bal[x] - int(val)

def valcheck(val, user):
  x = mem.index(user)
  if val == "all":
    val = bal[x]
  if val == "half":
    val = bal[x] // 2
  return val

@bot.command()
@has_permissions(administrator=True)
async def addmoney(ctx, user: discord.Member, val):
  x = mem.index(user)
  bal[x] = bal[x]+int(val)
  await ctx.send(f'Added {val} to {user.mention}\'s account')

@bot.command()
@has_permissions(administrator=True)
async def setmoney(ctx, user: discord.Member, val):
  x = mem.index(user)
  bal[x] = int(val)
  await ctx.send(f'Set {user.mention}\'s purse money to {val}')

keep_alive()
bot.run(my_secret)
