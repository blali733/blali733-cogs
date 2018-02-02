import discord
from discord.ext import commands

from utils import checks
from .utils.dataIO import fileIO
import os
import asyncio
from . import rolls
from .imSettings import add_filter, del_filter
from __main__ import send_cmd_help


class ImRoll:
    def __init__(self, bot):
        self.bot = bot
        self.loliFilters = fileIO("data/rolls/loli_filters.json", "load")
        self.loliSettings = fileIO("data/rolls/loli_settings.json", "load")
        self.danFilters = fileIO("data/rolls/dan_filters.json", "load")
        self.danSettings = fileIO("data/rolls/dan_settings.json", "load")
        self.gelFilters = fileIO("data/rolls/gel_filters.json", "load")
        self.gelSettings = fileIO("data/rolls/gel_settings.json", "load")
        self.konaFilters = fileIO("data/rolls/kona_filters.json", "load")
        self.konaSettings = fileIO("data/rolls/kona_settings.json", "load")
        self.active = fileIO("data/rolls/active.json", "load")

    @commands.group(pass_context=True)
    async def imlolifilter(self, ctx):
        """Manages loli filters
           Warning: Can be used to allow NSFW images

           Filters automatically apply tags to each search"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @imlolifilter.command(name="add", pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_server=True)
    async def _add_imlolifilter(self, ctx, filtertag: str):
        """Adds a tag to the server's loli filter list

           Example: !lolifilter add rating:s"""
        add_filter(self, ctx, filtertag, "loli")

    @imlolifilter.command(name="del", pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_server=True)
    async def _del_imlolifilter(self, ctx, filtertag: str = ""):
        """Deletes a tag from the server's loli filter list

           Without arguments, reverts to the default loli filter list

           Example: !lolifilter del rating:s"""
        del_filter(self, ctx, filtertag, "loli")

    @commands.group(pass_context=True)
    async def imgelfilter(self, ctx):
        """Manages gel filters
           Warning: Can be used to allow NSFW images

           Filters automatically apply tags to each search"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @imgelfilter.command(name="add", pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_server=True)
    async def _add_imgelfilter(self, ctx, filtertag: str):
        """Adds a tag to the server's gel filter list

           Example: !gelfilter add rating:s"""
        add_filter(self, ctx, filtertag, "gel")

    @imgelfilter.command(name="del", pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_server=True)
    async def _del_imgelfilter(self, ctx, filtertag: str = ""):
        """Deletes a tag from the server's gel filter list

           Without arguments, reverts to the default gel filter list

           Example: !gelfilter del rating:s"""
        del_filter(self, ctx, filtertag, "gel")

    @commands.group(pass_context=True)
    async def imdanfilter(self, ctx):
        """Manages dan filters
           Warning: Can be used to allow NSFW images

           Filters automatically apply tags to each search"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @imdanfilter.command(name="add", pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_server=True)
    async def _add_imdanfilter(self, ctx, filtertag: str):
        """Adds a tag to the server's dan filter list

           Example: !danfilter add rating:s"""
        add_filter(self, ctx, filtertag, "dan")

    @imdanfilter.command(name="del", pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_server=True)
    async def _del_imdanfilter(self, ctx, filtertag: str = ""):
        """Deletes a tag from the server's dan filter list

           Without arguments, reverts to the default dan filter list

           Example: !danfilter del rating:s"""
        del_filter(self, ctx, filtertag, "dan")

    @commands.group(pass_context=True)
    async def imkonafilter(self, ctx):
        """Manages kona filters
           Warning: Can be used to allow NSFW images

           Filters automatically apply tags to each search"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @imkonafilter.command(name="add", pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_server=True)
    async def _add_imkonafilter(self, ctx, filtertag: str):
        """Adds a tag to the server's kona filter list

           Example: !konafilter add rating:s"""
        add_filter(self, ctx, filtertag, "kona")

    @imkonafilter.command(name="del", pass_context=True, no_pm=True)
    @checks.admin_or_permissions(manage_server=True)
    async def _del_imkonafilter(self, ctx, filtertag: str = ""):
        """Deletes a tag from the server's kona filter list

           Without arguments, reverts to the default kona filter list

           Example: !konafilter del rating:s"""
        del_filter(self, ctx, filtertag, "kona")

    @commands.group(pass_context=True)
    @checks.is_owner()
    async def loliset(self, ctx):
        """Manages loli options"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @loliset.command(name="maxfilters")
    async def _maxfilters_loliset(self, maxfilters):
        """Sets the global tag limit for the filter list

           Gives an error when a user tries to add a filter while the server's filter list contains a certain amount of tags"""
        self.settings["maxfilters"] = maxfilters
        fileIO("data/rolls/loli_settings.json", "save", self.settings)
        await self.bot.say("Maximum filters allowed per server for loli set to '{}'.".format(maxfilters))

    @commands.command(pass_context=True, no_pm=True)
    async def imroll(self, ctx, *text):
        server = ctx.message.server
        channel = ctx.message.channel
        self.loliFilters = fileIO("data/rolls/loli_filters.json", "load")
        self.loliSettings = fileIO("data/rolls/loli_settings.json", "load")
        self.danFilters = fileIO("data/rolls/dan_filters.json", "load")
        self.danSettings = fileIO("data/rolls/dan_settings.json", "load")
        self.gelFilters = fileIO("data/rolls/gel_filters.json", "load")
        self.gelSettings = fileIO("data/rolls/gel_settings.json", "load")
        self.konaFilters = fileIO("data/rolls/kona_filters.json", "load")
        self.konaSettings = fileIO("data/rolls/kona_settings.json", "load")
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
        self.loliFilters = fileIO("data/rolls/loli_filters.json", "load")
        self.loliSettings = fileIO("data/rolls/loli_settings.json", "load")
        self.danFilters = fileIO("data/rolls/dan_filters.json", "load")
        self.danSettings = fileIO("data/rolls/dan_settings.json", "load")
        self.gelFilters = fileIO("data/rolls/gel_filters.json", "load")
        self.gelSettings = fileIO("data/rolls/gel_settings.json", "load")
        self.konaFilters = fileIO("data/rolls/kona_filters.json", "load")
        self.konaSettings = fileIO("data/rolls/kona_settings.json", "load")
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
        self.loliFilters = fileIO("data/rolls/loli_filters.json", "load")
        self.loliSettings = fileIO("data/rolls/loli_settings.json", "load")

        lock = asyncio.Lock()
        await rolls.lolibooru_get(self, ctx, server, channel, lock)

    @commands.command(pass_context=True, no_pm=True)
    async def danrs(self, ctx, *text):
        server = ctx.message.server
        channel = ctx.message.channel
        self.danFilters = fileIO("data/rolls/dan_filters.json", "load")
        self.danSettings = fileIO("data/rolls/dan_settings.json", "load")

        lock = asyncio.Lock()
        await rolls.danbooru_get(self, ctx, server, channel, lock)

    @commands.command(pass_context=True, no_pm=True)
    async def gelrs(self, ctx, *text):
        server = ctx.message.server
        channel = ctx.message.channel
        self.gelFilters = fileIO("data/rolls/gel_filters.json", "load")
        self.gelSettings = fileIO("data/rolls/gel_settings.json", "load")

        lock = asyncio.Lock()
        await rolls.gelbooru_get(self, ctx, server, channel, lock)

    @commands.command(pass_context=True, no_pm=True)
    async def konars(self, ctx, *text):
        server = ctx.message.server
        channel = ctx.message.channel
        self.konaFilters = fileIO("data/rolls/kona_filters.json", "load")
        self.konaSettings = fileIO("data/rolls/kona_settings.json", "load")

        lock = asyncio.Lock()
        await rolls.konachan_get(self, ctx, server, channel, lock)


async def dummy():
    pass


def check_folder():
    if not os.path.exists("data/rolls"):
        print("Creating data/rolls folder...")
        os.makedirs("data/rolls")


def set_activity():
    activity = {"loli": "true", "kona": "true", "gel": "true", "dan": "true"}

    if not fileIO("data/rolls/active.json", "check"):
        print("Creating default active.json...")
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

    # TODO make it shorter!

    # region File checking
    if not fileIO("data/rolls/loli_filters.json", "check"):
        print("Creating default loli filters.json...")
        fileIO("data/rolls/loli_filters.json", "save", loliFilters)
    else:
        loliFilterlist = fileIO("data/rolls/loli_filters.json", "load")
        if "default" not in loliFilterlist:
            loliFilterlist["default"] = loliFilters["default"]
            print("Adding default loli filters...")
            fileIO("data/rolls/loli_filters.json", "save", loliFilterlist)
    if not fileIO("data/rolls/loli_settings.json", "check"):
        print("Creating default loli settings.json...")
        fileIO("data/rolls/loli_settings.json", "save", loliSettings)

    if not fileIO("data/rolls/dan_filters.json", "check"):
        print("Creating default dan filters.json...")
        fileIO("data/rolls/dan_filters.json", "save", danFilters)
    else:
        danFilterlist = fileIO("data/rolls/dan_filters.json", "load")
        if "default" not in danFilterlist:
            danFilterlist["default"] = danFilters["default"]
            print("Adding default dan filters...")
            fileIO("data/rolls/dan_filters.json", "save", danFilterlist)
    if not fileIO("data/rolls/dan_settings.json", "check"):
        print("Creating default dan settings.json...")
        fileIO("data/rolls/dan_settings.json", "save", danSettings)

    if not fileIO("data/rolls/gel_filters.json", "check"):
        print("Creating default gel filters.json...")
        fileIO("data/rolls/gel_filters.json", "save", gelFilters)
    else:
        gelFilterlist = fileIO("data/rolls/gel_filters.json", "load")
        if "default" not in gelFilterlist:
            gelFilterlist["default"] = gelFilters["default"]
            print("Adding default gel filters...")
            fileIO("data/rolls/gel_filters.json", "save", gelFilterlist)
    if not fileIO("data/rolls/gel_settings.json", "check"):
        print("Creating default gel settings.json...")
        fileIO("data/rolls/gel_settings.json", "save", gelSettings)

    if not fileIO("data/rolls/kona_filters.json", "check"):
        print("Creating default kona filters.json...")
        fileIO("data/rolls/kona_filters.json", "save", konaFilters)
    else:
        konaFilterlist = fileIO("data/rolls/kona_filters.json", "load")
        if "default" not in konaFilterlist:
            konaFilterlist["default"] = konaFilters["default"]
            print("Adding default kona filters...")
            fileIO("data/rolls/kona_filters.json", "save", konaFilterlist)
    if not fileIO("data/rolls/kona_settings.json", "check"):
        print("Creating default kona settings.json...")
        fileIO("data/rolls/kona_settings.json", "save", konaSettings)
    # endregion


def setup(bot):
    check_folder()
    set_activity()
    check_files()
    bot.add_cog(ImRoll(bot))
