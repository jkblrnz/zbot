import os
import unidecode
import json
import discord
from dotenv import load_dotenv
from enum import Enum

class WeaponElement(Enum):
    Dark = 6
    Light = 5
    Earth = 4
    Wind = 3
    Water = 2
    Fire = 1

class WeaponElementColor(Enum):
    Dark = discord.Color.purple()
    Light = discord.Color.gold()
    Earth = discord.Color.dark_orange()
    Wind = discord.Color.green()
    Water = discord.Color.blue()
    Fire = discord.Color.red()

class WeaponType(Enum):
    Sword = 1
    Sword_And_Shield = 2
    Mace = 3
    Bow = 4
    Staff = 5
    Magic_Device = 7
    Twin_Blades = 8
    Scythe = 9
    Spear = 10
    Cannon = 11
    Axe = 12
    Bones = 100
    Unknown = 101

class ItemType(Enum):
    Weapon = 1
    Head_Slot = 2
    Top = 3
    Bottom = 4
    Upper_Slot = 5
    Lowwer_Slot = 6

# open and load relevant json files
with open('json/equipmentItem') as json_file:
    f = open('json/equipmentItem')
    equipData = json.load(f)
    f.close

with open('json/commandSkill') as json_file:
    f = open('json/commandSkill')
    skillData = json.load(f)
    f.close

with open('json/combinedPassiveSkill') as json_file:
    f = open('json/combinedPassiveSkill')
    combinedPassiveSkillData = json.load(f)
    f.close

with open('json/passiveSkill') as json_file:
    f = open('json/passiveSkill')
    passiveSkillData = json.load(f)
    f.close

# connect
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

# REST events
@client.event
async def on_ready():
    print(f'{client.user} is connected to this guild:')
    for guild in client.guilds:
        print(f'{guild.name}(id: {guild.id})')

@client.event
async def on_reaction_add(reaction, user):
    if reaction.message.author.bot and reaction.emoji == "❌":
        await reaction.message.delete()
    return

@client.event
async def on_message(message):
    if message.author.bot: return
    if message.author == client.user: return

    if '.i' in message.content or '.I' in message.content:
            for items in equipData['BookList']:
                if unidecode.unidecode(items['name'].lower()) in unidecode.unidecode(message.content.lower()) and unidecode.unidecode(message.content.lower()[3:]) == unidecode.unidecode(items['name'].lower()):

                    if items['slot'] == 1:
                        itype = WeaponType(items['typeId']).name
                    else:
                        itype = ItemType(items['slot']).name

                    #initialize embed
                    embed = discord.Embed(title="***" + items['name'] + "***" + "\n"
                                                + str(items['rarity']) + "★" + " - "
                                                + WeaponElement(items['elementAffinity']).name + " - "
                                                + itype.replace("_"," "),
                                          color=WeaponElementColor[WeaponElement(items['elementAffinity']).name].value)

                    embed.add_field(name = "***Stats Lvl 50-70***", value =
                                    "HP: " + str(items['maxStat']['maxHitPoint']) + " - " + str(items['limitBreakMaxStat']['maxHitPoint']) + '\n' +
                                    "MATK: " + str(items['maxStat']['spellPower']) + " - " + str(items['limitBreakMaxStat']['spellPower']) + '\n' +
                                    "PATK: " + str(items['maxStat']['physicalPower']) + " - " + str(items['limitBreakMaxStat']['physicalPower']) + '\n' +
                                    "MDEF: " + str(items['maxStat']['spellResist']) + " - " + str(items['limitBreakMaxStat']['spellResist']) + '\n' +
                                    "PDEF: " + str(items['maxStat']['physicalResist']) + " - " + str(items['limitBreakMaxStat']['physicalResist']),
                                    inline = True)

                    for skill in skillData['BookList']:
                        if skill['id'] == items['skillId']:

                            if skill['rowTypeAfterCast'] == 1:
                                arrow = "ᐅ"
                            elif skill['rowTypeAfterCast'] == 2:
                                arrow = "ᐊ"
                            else:
                                arrow = "X"

                            # eval cooldown formula within the json with level variable
                            level = 1
                            minCooldown = eval(skill['cooldown'])
                            minEnhancedCooldown = eval(skill['enhancedCooldown'])

                            level = 9
                            maxCooldown = eval(skill['cooldown'])
                            maxEnhancedCooldown = eval(skill['enhancedCooldown'])

                            embed.add_field(name = "***" + str(skill['name']) + "***"
                                            + " Cast: " + str(int(skill['castDuration']) / 10)
                                            + " CD: " + str(minCooldown / 10) + " - " + str(maxCooldown / 10)
                                            + " " + arrow ,
                                            value = str(skill['display'] + '\n'),
                                            inline = True)

                            embed.add_field(name = "***Dragon***"
                                            + " Cast: " + str(int(skill['enhancedCastDuration']) / 10)
                                            + " CD: " + str(minEnhancedCooldown / 10) + " - " + str(maxEnhancedCooldown / 10),
                                            value = str(skill['displayForEnhancement'] + '\n'),
                                            inline = True)

                            embed.add_field(name = "***Enhancement***",
                                            value = str(skill['displayForReinforcement'] + '\n'),
                                            inline = True)

                    for passive in passiveSkillData['BookList']:
                        if passive['id'] == items['skillId']:
                            embed.add_field(name = "***Skill***", value =
                                            str(passive['display']) + '\n' +
                                            str(passive['displayForReinforcement']),
                                            inline = True)
                            valueString = ""
                            for combinedPassives in items['combinedPassiveSkillIds']:
                                for combined in combinedPassiveSkillData['BookList']:
                                    if combined['id'] == combinedPassives:
                                        valueString += "**" + combined['name'] + "**" + '\n' + combined['display'] + '\n'

                            embed.add_field(name = "***Synths***", value =
                                            valueString,
                                            inline = True)

                    await message.channel.send(embed=embed)
                    return
            else:
                response = '```no such weapon (exact match required)```'
                await message.channel.send(response)
                return

    elif '.s' in message.content or '.S' in  message.content:

        response = "```"

        for items in equipData['BookList']:
            if message.content.lower()[3:] in unidecode.unidecode(items['name'].lower()):
                response += items['name'] + ", "
        response = response[:-2]

        if len(response) == 1:
            response += "``No Matches"

        response += "```"

        await message.channel.send(response)

    elif '.t' in message.content or '.T' in message.content:

        response = "```"

        for items in equipData['BookList']:
            itype = ""
            if items['slot'] == 1:
                itype = WeaponType(items['typeId']).name
            else:
                itype = ItemType(items['slot']).name
            if message.content.lower()[3:] in itype.lower().replace("_"," "):
                response += items['name'] + ", "
        response = response[:-2]

        if len(response) == 1:
            response += "``No Matches"

        response += "```"

        await message.channel.send(response)


client.run(TOKEN)
