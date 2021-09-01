import discord
from discord.ext import commands
import discord_slash
from discord_slash import cog_ext, SlashContext

from enum import Enum
from unidecode import unidecode
import json

guildID = [870765414374854736, 882096026775855184]

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
    Lower_Slot = 6

class lookUp(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # REST events
    @commands.Cog.listener("on_ready")
    async def locations(client):
        print(f'{client.bot.user} is connected to this guild:')
        for guild in client.bot.guilds:
            print(f'{guild.name}(id: {guild.id})')

    @commands.Cog.listener("on_reaction_add")
    async def remove(message, reaction, user):
        if reaction.message.author.bot and reaction.emoji == "❌":
            await reaction.message.delete()

    @cog_ext.cog_slash(name="item", description="Search for a particular item.", guild_ids = guildID)
    async def item(self, ctx: discord_slash.SlashContext, name):
        if ctx.author == self.bot.user: return
        if ctx.author.bot: return
        messageName = unidecode(name.lower())
        for items in equipData['BookList']:
            itemName = unidecode(items['name'].lower())
            itemId = str(items['id'])
            if (messageName in itemName or itemId == messageName) or messageName in itemId:
                if items['slot'] == 1:
                    itype = WeaponType(items['typeId']).name
                else:
                    itype = ItemType(items['slot']).name

                #initialize embed
                embed = discord.Embed(title= "[R" + items['rarity'] * "★" + "] "
                                            + "***" + str(items['name']) + "***" + " - "
                                            + itype.replace("_"," ") + ": " + WeaponElement(items['elementAffinity']).name,
                                      color=WeaponElementColor[WeaponElement(items['elementAffinity']).name].value)

                embed.add_field(name = "***Stats***", value =
                                "***LV*** : " + "50-70"+'\n'+
                                "***HP*** : " + str(items['maxStat']['maxHitPoint']) + " - " + str(items['limitBreakMaxStat']['maxHitPoint'])+'\n'
                                "***CRIT*** : " + str(items['maxStat']['critChance'] * 100) + " - " + str(items['limitBreakMaxStat']['critChance'] * 100),
                                inline = True)
                embed.add_field(name = '​', value =
                                "***PATK*** : " + str(items['maxStat']['physicalPower']) + " - " + str(items['limitBreakMaxStat']['physicalPower'])+'\n'+
                                "***MATK*** : " + str(items['maxStat']['spellPower']) + " - " + str(items['limitBreakMaxStat']['spellPower'])+'\n'+
                                "***Accuracy*** : " + str(items['maxStat']['hitRating']) + " - " + str(items['limitBreakMaxStat']['hitRating']),
                                inline = True)
                embed.add_field(name = '​', value =
                                "***PDEF*** : " + str(items['maxStat']['physicalResist']) + " - " + str(items['limitBreakMaxStat']['physicalResist'])+'\n'+
                                "***MDEF*** : " + str(items['maxStat']['spellResist']) + " - " + str(items['limitBreakMaxStat']['spellResist'])+'\n'+
                                "***Evasion*** : " + str(items['maxStat']['evasionRating']) + " - " + str(items['limitBreakMaxStat']['evasionRating']),
                                inline = True)

                for skill in skillData['BookList']:
                    if skill['id'] == items['skillId']:
                        #movement type
                        if skill['rowTypeAfterCast'] == 1:
                            arrow = "ᐅ"
                        elif skill['rowTypeAfterCast'] == 2:
                            arrow = "ᐊ"
                        else:
                            arrow = "X"

                        # eval cooldown formula within the json with level variable
                        level = 1
                        minCooldown = int(eval(skill['cooldown']))
                        minEnhancedCooldown = int(eval(skill['enhancedCooldown']))
                        level = 9
                        maxCooldown = int(eval(skill['cooldown']))
                        maxEnhancedCooldown = int(eval(skill['enhancedCooldown']))

                        embed.add_field(name = "***" + str(skill['name']) + "***"
                                        + "  - " + " Cast: " + str(int(skill['castDuration']) / 10) + 's'
                                        + " CD: " + str(minCooldown / 10) + "-" + str(maxCooldown / 10) + 's'
                                        + " " + arrow ,
                                        value = str(skill['display'] + '\n'),
                                        inline = False)

                        embed.add_field(name = "***Dragon***"
                                        + "  - " + " Cast: " + str(int(skill['enhancedCastDuration']) / 10) + 's'
                                        + " CD: " + str(minEnhancedCooldown / 10) + "-" + str(maxEnhancedCooldown / 10) + 's',
                                        value = str(skill['displayForEnhancement'] + '\n'),
                                        inline = False)

                        embed.add_field(name = "***Enhancement***",
                                        value = str(skill['displayForReinforcement'] + '\n'),
                                        inline = False)

                #item skills are located in a seperate json object requiring a seprate search
                for passive in passiveSkillData['BookList']:
                    if passive['id'] == items['skillId']:
                        embed.add_field(name = "***Skill***", value =
                                        str(passive['display']) + '\n' +
                                        str(passive['displayForReinforcement']),
                                        inline = False)
                        valueString = "​"
                        #synths are in seprate json object and each armor should have one so safe to assume
                        #armorUnit tests this assertion
                        for combinedPassives in items['combinedPassiveSkillIds']:
                            for combined in combinedPassiveSkillData['BookList']:
                                if combined['id'] == combinedPassives:
                                    valueString += "**" + combined['name'] + "**" + '\n' + combined['display'] + '\n'

                        embed.add_field(name = "***Synths***", value =
                                        valueString,
                                        inline = False)

                await ctx.send(embed=embed)
                return
        else:
            response = "```no such weapon (exact match required)```"
            await ctx.send(response, hidden=True)
            return

    @cog_ext.cog_slash(name="search", description="Search for items with a matching name.", guild_ids = guildID)
    async def search(self, ctx: discord_slash.SlashContext, name):
       if ctx.author == self.bot.user: return
       if ctx.author.bot: return

       response = "```"
       for items in equipData['BookList']:
           if name.lower() in unidecode(items['name'].lower()):
               response += items['name'] + ":" + str(items['rarity']) + ":" + str(items['id']) + ", "
       response = response[:-2] + "```"

       if len(response) == 4:
           response = "```No Matches```"
           await ctx.send(response, hidden=True)
       else:
           await ctx.send(response, hidden=True)

    @cog_ext.cog_slash(name="type", description="Search for all items of a ceartin type.  Returns name:rarity:id.", guild_ids = guildID)
    async def type(self, ctx: discord_slash.SlashContext, item_type):
        if ctx.author == self.bot.user: return
        if ctx.author.bot: return
        response = "```"
        for items in equipData['BookList']:
            if items['slot'] == 1:
                itype = WeaponType(items['typeId']).name
            else:
                itype = ItemType(items['slot']).name

            if item_type.lower() in itype.lower().replace("_"," "):
                response += items['name'] + ", "
        response = response[:-2] + "```"

        if len(response) == 4:
            response = "```No Matches```"
            await ctx.send(response, hidden=True)
        else:
            await ctx.send(response, hidden=True)

def setup(bot):
    bot.add_cog(lookUp(bot))
