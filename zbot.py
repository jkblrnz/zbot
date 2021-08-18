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

# connect
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

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


# REST events
@client.event
async def on_ready():
    print(f'{client.user} is connected to this guild:')
    for guild in client.guilds:
        print(f'{guild.name}(id: {guild.id})')

@client.event
async def on_reaction_add(reaction, user):
    if reaction.message.author.bot:
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
                        if items['typeId'] == 1:
                            itype = "Sword"
                        elif items['typeId'] == 2:
                            itype = "Sword & Shield"
                        elif items['typeId'] == 3:
                            itype = "Mace"
                        elif items['typeId'] == 4:
                            itype = "Bow"
                        elif items['typeId'] == 5:
                            itype = "Staff"
                        elif items['typeId'] == 7:
                            itype = "Magic Device"
                        elif items['typeId'] == 8:
                            itype = "Twin Blades"
                        elif items['typeId'] == 9:
                            itype = "Scythe"
                        elif items['typeId'] == 10:
                            itype = "Spear"
                        elif items['typeId'] == 11:
                            itype = "Cannon"
                        elif items['typeId'] == 12:
                            itype = "Axe"
                    elif items['slot'] == 2:
                        itype = "Head Slot"
                    elif items['slot'] == 3:
                        itype = "Top"
                    elif items['slot'] == 4:
                        itype = "Bottom"
                    elif items['slot'] == 5:
                        itype = "Upper Slot"
                    elif items['slot'] == 6:
                        itype = "Lowwer Slot"

                    #initialize embed
                    embed = discord.Embed(title="***" + items['name'] + "***" + "\n"
                                                + str(items['rarity']) + "★" + " - "
                                                + WeaponElement(items['elementAffinity']).name + " - "
                                                + itype,
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
            if items['slot'] == 1 and items['rarity'] == 4:
                if items['typeId'] == 1:
                    itype = "Sword"
                elif items['typeId'] == 2:
                    itype = "Sword & Shield"
                elif items['typeId'] == 3:
                    itype = "Mace"
                elif items['typeId'] == 4:
                    itype = "Bow"
                elif items['typeId'] == 5:
                    itype = "Staff"
                elif items['typeId'] == 7:
                    itype = "Magic Device"
                elif items['typeId'] == 8:
                    itype = "Twin Blades"
                elif items['typeId'] == 9:
                    itype = "Scythe"
                elif items['typeId'] == 10:
                    itype = "Spear"
                elif items['typeId'] == 11:
                    itype = "Cannon"
                elif items['typeId'] == 12:
                    itype = "Axe"
            elif items['slot'] == 2:
                itype = "Head Slot"
            elif items['slot'] == 3:
                itype = "Top"
            elif items['slot'] == 4:
                itype = "Bottom"
            elif items['slot'] == 5:
                itype = "Upper Slot"
            elif items['slot'] == 6:
                itype = "Lowwer Slot"
            if message.content.lower()[3:] in itype.lower():
                response += items['name'] + ", "
        response = response[:-2]

        if len(response) == 1:
            response += "``No Matches"

        response += "```"

        await message.channel.send(response)


client.run(TOKEN)
