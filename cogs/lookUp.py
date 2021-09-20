#download for grequests to fix issues with ssl
#tends to cause some of the rest events to go into inf loops
#grequests used in boss list to request pages for boss enum
from gevent import monkey as curious_george
curious_george.patch_all(thread=False, select=False)
import grequests
import requests

#api stuff
import discord
from discord.ext import commands
#Expirmental wrapper for discord slash commands
#When offical rewrite is out a rewrite might be nesscary
import discord_slash
from discord_slash import cog_ext, SlashContext

#data object stuff
from aenum import Enum, NoAlias, auto
import json

#search stuff
import re
#primarily used in item search for forgien words
#normalizses unicode to let english users search for the french named items
from unidecode import unidecode

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

# this class has partial searches so needs to be managed carefully
class BossEx(Enum):
    Hildegard = auto()
    Matilda_And_Hildegard = auto()
    Matilda_And_Upa_Jellyfish = auto()
    Hiveval = auto()
    Grimwasp = auto()
    Counterattacking_Grimwasp = auto()
    Dark_Knight = auto()
    Shadowlurker_Dark_Knight = auto()
    Mitra_Golem = auto()
    Scape_Ox = auto()
    Equismaton = auto()
    Roaring_Scape_Ox = auto()
    Graenill = auto()
    Almudahd = auto()
    Zarich = auto()
    Zarich_And_Almudahd = auto()
    Xenon = auto()
    Empty_Head = auto()
    Snowlia = auto()
    Sky_Pirate_Head_Of_Obsession = auto()
    Zafosboa = auto()
    Bone_Python = auto()
    Triwhisp = auto()
    Rem_Nawis = auto()
    Ines = auto()
    Grothvarg_Rebirthed = auto()
    Grothvarg = auto()

class BossGb(Enum):
    Pehn = auto()
    Mazandor = auto()
    Malagna = auto()
    Aspidochelone = auto()
    Warlugan = auto()
    Dismurte = auto()
    Ulteriness = auto()
    Furnav_Moth = auto()
    Isvaal = auto()
    Kelkrus = auto()
    Giganturus = auto()
    Anemorabius = auto()
    Feluze = auto()
    Envisoeur = auto()
    Ember_Fox = auto()
    King_Cat_Sith = auto()
    Agunios = auto()
    Venomush = auto()
    Rikelnok = auto()
    Auguste = auto()

class lookUp(commands.Cog):

    guildList = []
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        # load json item data
        # equipment data
        with open('json/equipmentItem') as json_file:
            f = open('json/equipmentItem')
            self.__equipData = json.load(f)
            f.close

        # skill data
        with open('json/commandSkill') as json_file:
            f = open('json/commandSkill')
            self.__skillData = json.load(f)
            f.close

        # synth data
        with open('json/combinedPassiveSkill') as json_file:
            f = open('json/combinedPassiveSkill')
            self.__combinedPassiveSkillData = json.load(f)
            f.close

        # skill data
        with open('json/passiveSkill') as json_file:
            f = open('json/passiveSkill')
            self.__passiveSkillData = json.load(f)
            f.close

    # REST events
    @commands.Cog.listener("on_ready")
    async def locations(self):
        print(f'{self.bot.user} is connected to this guild:')
        for guild in self.bot.guilds:
            print(f'{guild.name}(id: {guild.id})')
            self.guildList.append(guild.id)

    @commands.Cog.listener("on_reaction_add")
    async def remove(message, reaction, user):
        if reaction.message.author.bot and reaction.emoji == "❌":
            await reaction.message.delete()

    @cog_ext.cog_slash(name="item", description="Search for a particular item.", guild_ids = guildList)
    async def item(self, ctx: discord_slash.SlashContext, name):
        if ctx.author.bot: return
        messageName = unidecode(name.lower())
        for items in self.__equipData['BookList']:
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

                for skill in self.__skillData['BookList']:
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
                for passive in self.__passiveSkillData['BookList']:
                    if passive['id'] == items['skillId']:
                        embed.add_field(name = "***Skill***", value =
                                        str(passive['display']) + '\n' +
                                        str(passive['displayForReinforcement']),
                                        inline = False)
                        valueString = "​"
                        #synths are in seprate json object and each armor should have one so safe to assume
                        #armorUnit tests this assertion
                        for self.__combinedPassives in items['combinedPassiveSkillIds']:
                            for combined in self.__combinedPassiveSkillData['BookList']:
                                if combined['id'] == self.__combinedPassives:
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

    @cog_ext.cog_slash(name="search", description="Search for items with a matching name.", guild_ids = guildList)
    async def search(self, ctx: discord_slash.SlashContext, name):
       if ctx.author.bot: return

       response = "```"
       for items in self.__equipData['BookList']:
           if name.lower() in unidecode(items['name'].lower()):
               response += items['name'] + ":" + str(items['rarity']) + ":" + str(items['id']) + ", "
       response = response[:-2] + "```"

       if len(response) == 4:
           response = "```No Matches```"
           await ctx.send(response, hidden=True)
           return
       await ctx.send(response, hidden=True)

    @cog_ext.cog_slash(name="type", description="Search for all items of a ceartin type.  Returns name:rarity:id.", guild_ids = guildList)
    async def type(self, ctx: discord_slash.SlashContext, item_type):
        if ctx.author.bot: return

        response = "```"
        for items in self.__equipData['BookList']:
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
            return

        await ctx.send(response, hidden=True)

    @cog_ext.cog_slash(name="boss", description="Search for a boss guide.", guild_ids = guildList)
    async def boss(self, ctx: discord_slash.SlashContext, boss):
        if ctx.author.bot: return

        # this solution finds first parital match so Boss enum needs to be carfully managed
        bossName = ''
        for bosses in set(BossEx.__members__):
            if boss.lower() in bosses.lower().replace("_"," "):
                bossName = bosses
                break

        if bossName != '':
             response = requests.get("https://altema-mitrasphere.com/" + bossName.replace("_",""))
             if "404-img.png" in str(response.content): #altema doesn't return right code so look for their 404 img
                 await ctx.send("```BossEx not found on altema```", hidden=True)
             else:
                 await ctx.send("https://altema-mitrasphere.com/" + bossName.replace("_","").replace("And",""))
        else:
            bossName = ''
            for bosses in set(BossGb.__members__):
                if boss.lower() in bosses.lower().replace("_"," "):
                    bossName = bosses
                    break

            if bossName != '':
                 response = requests.get("https://altema-mitrasphere.com/" + bossName.replace("_",""))
                 if "404-img.png" in str(response.content): #altema doesn't return right code so look for their 404 img
                     await ctx.send("```BossGb not found on altema```", hidden=True)
                 else:
                     await ctx.send("https://altema-mitrasphere.com/" + bossName.replace("_","").replace("And",""))
            else:
                await ctx.send("```BossEx not found in database```", hidden=True)

    @cog_ext.cog_slash(name="EX", description="Get a list of all possible EX bosses.", guild_ids = guildList)
    async def EX(self, ctx: discord_slash.SlashContext):
        if ctx.author.bot: return

        urls = []
        for bosses in BossEx.__members__: #find a solid alternative to __members__
            urls.append("https://altema-mitrasphere.com/" + bosses.replace("_","").replace("And",""))
        rs = (grequests.get(u) for u in urls)
        responses = grequests.map(rs)

        lst = ""
        for x in range(len(responses)):
            target = re.compile("404-img.png")
            if target.search(str(responses[x].content)): #altema doesn't return the right code so look for the 404 img
                lst += BossEx(x + 1).name.replace("_"," ") + '\n'
            else:
                lst += '[' + BossEx(x + 1).name.replace("_", " ") + ']' + "(https://altema-mitrasphere.com/" + BossEx(x + 1).name.replace("_","").replace("And","") + ')' + '\n'

        embed = discord.Embed(description=lst)
        await ctx.send(embed=embed, hidden=True)

    @cog_ext.cog_slash(name="GB", description="Get a list of all possible GB bosses.", guild_ids = guildList)
    async def GB(self, ctx: discord_slash.SlashContext):
        if ctx.author.bot: return

        urls = []
        for bosses in BossGb.__members__: #find a solid alternative to __members__
            urls.append("https://altema-mitrasphere.com/" + bosses.replace("_","").replace("And",""))
        rs = (grequests.get(u) for u in urls)
        responses = grequests.map(rs)

        lst = ""
        for x in range(len(responses)):
            target = re.compile("404-img.png")
            if target.search(str(responses[x].content)): #altema doesn't return the right code so look for the 404 img
                lst += BossGb(x + 1).name.replace("_"," ") + '\n'
            else:
                lst += '[' + BossGb(x + 1).name.replace("_", " ") + ']' + "(https://altema-mitrasphere.com/" + BossGb(x + 1).name.replace("_","").replace("And","") + ')' + '\n'

        embed = discord.Embed(description=lst)
        await ctx.send(embed=embed, hidden=True)
def setup(bot):
    bot.add_cog(lookUp(bot))
