##INCLUDES
import discord
from discord.ext import commands

import random
import json
import asyncio

import slm

##SETTINGS
TOKEN = None
with open("token.txt", "r") as fd:
    TOKEN = (str)(fd.read())
if TOKEN == None:
    print("Failed to load the token. Check  token.txt .")
    exit


with open("default_settings.json", "r+") as fd:
    settings = json.load(fd)

print(f"Settings: {settings}")


bot_slm = slm.SLM(
    custom_dict={},
    words_range = [settings["min_words"], settings["max_words"]],
    sentences_range = [settings["min_sentences"], settings["max_sentences"]],
    forbidden_words = settings["forbidden_list"]
)

##Bot init

bot = commands.Bot(command_prefix="....!", self_bot=False)

##Commands
##Slash commands

@bot.command()
async def ping(ctx: discord.Message):
    await ctx.reply("Pong!")

## MODS
@bot.command()
async def dice_mod(ctx: discord.Message, mode):
    settings["dice_mod"] = string_to_bool(mode)
    await ctx.reply("Бог не играет в кости")    

@bot.command()
async def ignore_dm_mod(ctx: discord.Message, mode):
    settings["ignore_dm_mod"] = string_to_bool(mode)
    await ctx.reply("ДЕФКОН 1, ДЕФКОН 1, НАМ ПИЗДЕЦ!!!!")

@bot.command()
async def silent_mod(ctx: discord.Message, mode):
    settings["silent_mod"] = string_to_bool(mode)
    await ctx.reply("На грани тьми и тени  скользит воин ниндзя, лазутчик и убийца исполняющий любое повеление господина!")


@bot.command()
async def delay_mod(ctx: discord.Message, mode):
    settings["delay"] = string_to_bool(mode)
    await ctx.reply("Тепреь я не бот, теперь я просто психически болен!!!")

#Limit commands
@bot.command()
async def set_chance(ctx: discord.Message, chance):
    try:
        settings["chance"] = int(chance)
    except:
        await ctx.reply("Check args. SINGLE argument must be INTEGER")
        return
    
    await ctx.reply(f"New chance: {settings['chance']}")

@bot.command()
async def set_min_max_delay(ctx: discord.Message, min, max):
    try:
        settings["delay_min_ms"] = int(min)
        settings["delay_max_ms"] = int(max)
    except:
        await ctx.reply("Check args. Both TWO of them must be INTEGERS")
        return
    
    await ctx.reply(f"New min and max: {settings['min_words']}, {settings['max_words']}")

@bot.command()
async def set_min_max_words(ctx: discord.Message, min, max):
    try:
        settings["min_words"] = int(min)
        settings["max_words"] = int(max)
    except:
        await ctx.reply("Check args. Both TWO of them must be INTEGERS")
        return
    
    await ctx.reply(f"New min and max: {settings['min_words']}, {settings['max_words']}")

@bot.command()
async def set_min_max_sentences(ctx: discord.Message, min, max):
    try:
        settings["min_sentences"] = int(min)
        settings["max_sentences"] = int(max)
    except:
        await ctx.reply("Check args. Both TWO of them must be INTEGERS")
        return
    
    await ctx.reply(f"New min and max: {settings['min_sentences']}, {settings['max_sentences']}")

#save/load word dictionary
@bot.command()
async def save_dict(ctx: discord.Message):
    with open("dict_save.json", "w") as file:
        json.dump(bot_slm.dict_get(), file)
    await ctx.reply("Dict was saved successfuly")

@bot.command()
async def load_dict(ctx: discord.Message):
    with open("dict_save.json", "r") as file:
        bot_slm.dict_set(json.load(file))
    await ctx.reply("Dictionary was loaded successfuly")

#Events
@bot.event
async def on_ready():
    print("BOT: I am ready\n")

@bot.event
async def on_message(message: discord.Message):

    print(f"[{message.created_at}] {message.author}: {message.content}")
    if message.author.id in settings['commands_whitelist']:
        await bot.process_commands(message)
    
    if settings['ignore_dm_mod']&(message.guild == None) :
        return

    if settings['ignore_me']&(message.author == bot.user):
        return
    
    if settings['ignore_bots']&(message.author.bot):
        return 

    bot_slm.learn(message.content)
    print(f"Dict lenght: {len(list(bot_slm.dict_get().keys()))} \n")
    print(f"Dict: {bot_slm.dict_get()}")

    last_word = message.content.split()[-1]

    dice = random.randint(1, settings['chance'])
    print("DICE: ", dice)
    if (settings['dice_mod'] & (dice!=1)):
        return

    # checks for silent mod
    if (settings['silent_mod'] != True):
        
        #continue mod
        if settings['continue_sentence']:
            random_text = bot_slm.generate_text(root=last_word)
        else:
            random_text = bot_slm.generate_text(root=None)
        
        #delay
        if settings['delay']:
            async with message.channel.typing():
                await asyncio.sleep((random.randint(settings['delay_min_ms'], settings['delay_max_ms'])/1000))
            await message.channel.send(random_text)
        else:
            await message.channel.send(random_text)

## Useful functions
#checks if sequance of chars of target are contained in object
def containts_target(object, target):

    target_lenght = len(target)
    i = 0
    for char in object:
        if char == target[i]:
            i += 1
            if i >= target_lenght:
                return True
        else:
            i = 0

#converts symbols which are triditionaly represent True or False as bool
def string_to_bool(string):
    if string in ('yes', 'y', 'True', 't', '1', 'enable', 'on'):
        return True
    elif string in ('no', 'n', 'False', 'f', '0', 'disable', 'off'):
        return False

bot.run(TOKEN)