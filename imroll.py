import discord
from discord.ext import commands
from .utils.dataIO import fileIO
import os
import asyncio
from . import rolls


class ImRoll:
    def __init__(self, bot):
        self.bot = bot
        self.loliFilters = fileIO("data/loli/filters.json", "load")
        self.loliSettings = fileIO("data/loli/settings.json", "load")
        self.danFilters = fileIO("data/dan/filters.json", "load")
        self.danSettings = fileIO("data/dan/settings.json", "load")
        self.gelFilters = fileIO("data/gel/filters.json", "load")
        self.gelSettings = fileIO("data/gel/settings.json", "load")
        self.konaFilters = fileIO("data/kona/filters.json", "load")
        self.konaSettings = fileIO("data/kona/settings.json", "load")
        self.active = fileIO("data/rolls/active.json", "load")

    @commands.command(pass_context=True, no_pm=True)
    async def imroll(self, ctx, *text):
        server = ctx.message.server
        channel = ctx.message.channel
        self.loliFilters = fileIO("data/loli/filters.json", "load")
        self.loliSettings = fileIO("data/loli/settings.json", "load")
        self.danFilters = fileIO("data/dan/filters.json", "load")
        self.danSettings = fileIO("data/dan/settings.json", "load")
        self.gelFilters = fileIO("data/gel/filters.json", "load")
        self.gelSettings = fileIO("data/gel/settings.json", "load")
        self.konaFilters = fileIO("data/kona/filters.json", "load")
        self.konaSettings = fileIO("data/kona/settings.json", "load")
        self.active = fileIO("data/rolls/active.json", "load")

        lock = asyncio.Lock()
        await asyncio.gather(
            rolls.lolibooru_get(self, ctx, server, channel, lock) if self.active["loli"] == "true" else dummy(),
            rolls.danbooru_get(self, ctx, server, channel, lock) if self.active["dan"] == "true" else dummy(),
            rolls.gelbooru_get(self, ctx, server, channel, lock) if self.active["gel"] == "true" else dummy(),
            rolls.konachan_get(self, ctx, server, channel, lock) if self.active["kona"] == "true" else dummy(),
        )

    @commands.command(pass_context=True, no_pm=True)
    async def imrollf(self, ctx, *text):
        server = ctx.message.server
        channel = ctx.message.channel
        self.loliFilters = fileIO("data/loli/filters.json", "load")
        self.loliSettings = fileIO("data/loli/settings.json", "load")
        self.danFilters = fileIO("data/dan/filters.json", "load")
        self.danSettings = fileIO("data/dan/settings.json", "load")
        self.gelFilters = fileIO("data/gel/filters.json", "load")
        self.gelSettings = fileIO("data/gel/settings.json", "load")
        self.konaFilters = fileIO("data/kona/filters.json", "load")
        self.konaSettings = fileIO("data/kona/settings.json", "load")
        self.active = fileIO("data/rolls/active.json", "load")

        l1 = asyncio.Lock()
        l2 = asyncio.Lock()
        l3 = asyncio.Lock()
        l4 = asyncio.Lock()
        await asyncio.gather(
            rolls.lolibooru_get(self, ctx, server, channel, l1) if self.active["loli"] == "true" else dummy(),
            rolls.danbooru_get(self, ctx, server, channel, l2) if self.active["dan"] == "true" else dummy(),
            rolls.gelbooru_get(self, ctx, server, channel, l3) if self.active["gel"] == "true" else dummy(),
            rolls.konachan_get(self, ctx, server, channel, l4) if self.active["kona"] == "true" else dummy(),
        )

    @commands.command(pass_context=True, no_pm=True)
    async def getSwitch(self, ctx, *text):
        self.active = fileIO("data/rolls/active.json", "load")
        await self.bot.say(self.active)

    @commands.command(pass_context=True, no_pm=True)
    async def loliSwitch(self, ctx, *text):
        self.active = fileIO("data/rolls/active.json", "load")
        if self.active["loli"] == "true":
            self.active["loli"] = "false"
            await self.bot.say("Loli disabled!")
        else:
            self.active["loli"] = "true"
            await self.bot.say("Loli enabled!")
        fileIO("data/rolls/active.json", "save", self.active)

    @commands.command(pass_context=True, no_pm=True)
    async def konaSwitch(self, ctx, *text):
        self.active = fileIO("data/rolls/active.json", "load")
        if self.active["kona"] == "true":
            self.active["kona"] = "false"
            await self.bot.say("Kona(ta) disabled!")
        else:
            self.active["kona"] = "true"
            await self.bot.say("Kona(ta) enabled!")
        fileIO("data/rolls/active.json", "save", self.active)

    @commands.command(pass_context=True, no_pm=True)
    async def danSwitch(self, ctx, *text):
        self.active = fileIO("data/rolls/active.json", "load")
        if self.active["dan"] == "true":
            self.active["dan"] = "false"
            await self.bot.say("Dan disabled!")
        else:
            self.active["dan"] = "true"
            await self.bot.say("Dan enabled!")
        fileIO("data/rolls/active.json", "save", self.active)

    @commands.command(pass_context=True, no_pm=True)
    async def gelSwitch(self, ctx, *text):
        self.active = fileIO("data/rolls/active.json", "load")
        if self.active["gel"] == "true":
            self.active["gel"] = "false"
            await self.bot.say("Gel disabled!")
        else:
            self.active["gel"] = "true"
            await self.bot.say("Gel enabled!")
        fileIO("data/rolls/active.json", "save", self.active)

    @commands.command(pass_context=True, no_pm=True)
    async def lolirs(self, ctx, *text):
        server = ctx.message.server
        channel = ctx.message.channel
        self.loliFilters = fileIO("data/loli/filters.json", "load")
        self.loliSettings = fileIO("data/loli/settings.json", "load")

        lock = asyncio.Lock()
        await rolls.lolibooru_get(self, ctx, server, channel, lock)

    @commands.command(pass_context=True, no_pm=True)
    async def danrs(self, ctx, *text):
        server = ctx.message.server
        channel = ctx.message.channel
        self.danFilters = fileIO("data/dan/filters.json", "load")
        self.danSettings = fileIO("data/dan/settings.json", "load")

        lock = asyncio.Lock()
        await rolls.danbooru_get(self, ctx, server, channel, lock)

    @commands.command(pass_context=True, no_pm=True)
    async def gelrs(self, ctx, *text):
        server = ctx.message.server
        channel = ctx.message.channel
        self.gelFilters = fileIO("data/gel/filters.json", "load")
        self.gelSettings = fileIO("data/gel/settings.json", "load")

        lock = asyncio.Lock()
        await rolls.gelbooru_get(self, ctx, server, channel, lock)

    @commands.command(pass_context=True, no_pm=True)
    async def konars(self, ctx, *text):
        server = ctx.message.server
        channel = ctx.message.channel
        self.konaFilters = fileIO("data/kona/filters.json", "load")
        self.konaSettings = fileIO("data/kona/settings.json", "load")

        lock = asyncio.Lock()
        await rolls.konachan_get(self, ctx, server, channel, lock)


async def dummy():
    pass


def check_folder():
    if not os.path.exists("data/loli"):
        print("Creating data/loli folder...")
        os.makedirs("data/loli")
    if not os.path.exists("data/dan"):
        print("Creating data/dan folder...")
        os.makedirs("data/dan")
    if not os.path.exists("data/gel"):
        print("Creating data/gel folder...")
        os.makedirs("data/gel")
    if not os.path.exists("data/kona"):
        print("Creating data/kona folder...")
        os.makedirs("data/kona")
    if not os.path.exists("data/rolls"):
        print("Creating data/rolls folder...")
        os.makedirs("data/rolls")


def set_activity():
    activity = {"loli": "true", "kona": "true", "gel": "true", "dan": "true"}

    if not fileIO("data/rolls/active.json", "check"):
        print("Creating default loli filters.json...")
        fileIO("data/rolls/active.json", "save", activity)


def check_files():
    loliFilters = {"default": ["rating:safe"]}
    loliSettings = {"maxfilters": "50"}
    danFilters = {"default": ["rating:safe"]}
    danSettings = {"username": "", "api_key": "", "maxfilters": "10"}
    gelFilters = {"default": ["rating:safe"]}
    gelSettings = {"maxfilters": "50"}
    konaFilters = {"default": ["rating:safe"]}
    konaSettings = {"username": "", "api_key": "", "maxfilters": "10"}

    if not fileIO("data/loli/filters.json", "check"):
        print("Creating default loli filters.json...")
        fileIO("data/loli/filters.json", "save", loliFilters)
    else:
        loliFilterlist = fileIO("data/loli/filters.json", "load")
        if "default" not in loliFilterlist:
            loliFilterlist["default"] = loliFilters["default"]
            print("Adding default loli filters...")
            fileIO("data/loli/filters.json", "save", loliFilterlist)
    if not fileIO("data/loli/settings.json", "check"):
        print("Creating default loli settings.json...")
        fileIO("data/loli/settings.json", "save", loliSettings)

    if not fileIO("data/dan/filters.json", "check"):
        print("Creating default dan filters.json...")
        fileIO("data/dan/filters.json", "save", danFilters)
    else:
        danFilterlist = fileIO("data/dan/filters.json", "load")
        if "default" not in danFilterlist:
            danFilterlist["default"] = danFilters["default"]
            print("Adding default dan filters...")
            fileIO("data/dan/filters.json", "save", danFilterlist)
    if not fileIO("data/dan/settings.json", "check"):
        print("Creating default dan settings.json...")
        fileIO("data/dan/settings.json", "save", danSettings)

    if not fileIO("data/gel/filters.json", "check"):
        print("Creating default gel filters.json...")
        fileIO("data/gel/filters.json", "save", gelFilters)
    else:
        gelFilterlist = fileIO("data/gel/filters.json", "load")
        if "default" not in gelFilterlist:
            gelFilterlist["default"] = gelFilters["default"]
            print("Adding default gel filters...")
            fileIO("data/gel/filters.json", "save", gelFilterlist)
    if not fileIO("data/gel/settings.json", "check"):
        print("Creating default gel settings.json...")
        fileIO("data/gel/settings.json", "save", gelSettings)

    if not fileIO("data/kona/filters.json", "check"):
        print("Creating default kona filters.json...")
        fileIO("data/kona/filters.json", "save", konaFilters)
    else:
        konaFilterlist = fileIO("data/kona/filters.json", "load")
        if "default" not in konaFilterlist:
            konaFilterlist["default"] = konaFilters["default"]
            print("Adding default kona filters...")
            fileIO("data/kona/filters.json", "save", konaFilterlist)
    if not fileIO("data/kona/settings.json", "check"):
        print("Creating default kona settings.json...")
        fileIO("data/kona/settings.json", "save", konaSettings)


def setup(bot):
    check_folder()
    set_activity()
    check_files()
    bot.add_cog(ImRoll(bot))
