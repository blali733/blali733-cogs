import random
from urllib import parse

import aiohttp
import discord
import sys
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
        self.filters = fileIO("data/rolls/filters.json", "load")
        self.settings = fileIO("data/rolls/settings.json", "load")
        self.active = fileIO("data/rolls/active.json", "load")
        self.phrases = {
            "loli": {"random": "+order%3Arandom",
                     "call": "https://lolibooru.moe/post/index.json?limit=1&tags=",
                     "embed": "https://lolibooru.moe/post/show/{}",
                     "m1": "Fetching loli image...",
                     "m2": "loli preview ^^",
                     "title": "Lolibooru Image #{}"},
            "gel": {"random": "",
                    "call": "http://gelbooru.com/index.php?page=dapi&s=post&limit=1&q=index&tags=",
                    "embed": "https://gelbooru.com/index.php?page=post&s=view&id={}",
                    "m1": "Fetching gel image...",
                    "m2": "gel preview",
                    "title": "Gelbooru Image #{}"},
            "dan": {"random": "&random=y",
                    "call": "http://danbooru.donmai.us/posts.json?tags=",
                    "embed": "https://danbooru.donmai.us/posts/{}",
                    "m1": "Fetching dan image...",
                    "m2": "dan preview",
                    "title": "Danbooru Image #{}"},
            "kona": {"random": "+order%3Arandom",
                     "call": "https://konachan.com/post.json?limit=1&tags=",
                     "embed": "https://konachan.com/post/show/{}",
                     "m1": "Fetching kona image...",
                     "m2": "Kona(ta) preview",
                     "title": "Konachan Image #{}"}
        }

    # TODO fix this region:
    # region Filters and settings
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
    # endregion

    # region Group rolls
    @commands.command(pass_context=True, no_pm=True)
    async def imroll(self, ctx, *text):
        server = ctx.message.server
        channel = ctx.message.channel
        self.filters = fileIO("data/rolls/filters.json", "load")
        self.settings = fileIO("data/rolls/settings.json", "load")
        self.active = fileIO("data/rolls/active.json", "load")

        lock = asyncio.Lock()
        await asyncio.gather(
            self.image_get(ctx, server, channel, "loli", lock) if self.active["loli"] == "true" else dummy(),
            self.image_get(ctx, server, channel, "dan", lock) if self.active["dan"] == "true" else dummy(),
            self.image_get(ctx, server, channel, "gel", lock) if self.active["gel"] == "true" else dummy(),
            self.image_get(ctx, server, channel, "kona", lock) if self.active["kona"] == "true" else dummy(),
        )

    @commands.command(pass_context=True, no_pm=True)
    async def imrollf(self, ctx, *text):
        server = ctx.message.server
        channel = ctx.message.channel
        self.filters = fileIO("data/rolls/filters.json", "load")
        self.settings = fileIO("data/rolls/settings.json", "load")
        self.active = fileIO("data/rolls/active.json", "load")

        await asyncio.gather(
            self.image_get(ctx, server, channel, "loli", False, False) if self.active["loli"] == "true" else dummy(),
            self.image_get(ctx, server, channel, "dan", False, False) if self.active["dan"] == "true" else dummy(),
            self.image_get(ctx, server, channel, "gel", False, False) if self.active["gel"] == "true" else dummy(),
            self.image_get(ctx, server, channel, "kona", False, False) if self.active["kona"] == "true" else dummy(),
        )
    # endregion

    # region Single rolls
    @commands.command(pass_context=True, no_pm=True)
    async def lolirs(self, ctx, *text):
        server = ctx.message.server
        channel = ctx.message.channel
        self.filters = fileIO("data/rolls/filters.json", "load")
        self.settings = fileIO("data/rolls/settings.json", "load")

        await self.image_get(ctx, server, channel, "loli", False, False)

    @commands.command(pass_context=True, no_pm=True)
    async def danrs(self, ctx, *text):
        server = ctx.message.server
        channel = ctx.message.channel
        self.filters = fileIO("data/rolls/filters.json", "load")
        self.settings = fileIO("data/rolls/settings.json", "load")

        await self.image_get(ctx, server, channel, "dan", False, False)

    @commands.command(pass_context=True, no_pm=True)
    async def gelrs(self, ctx, *text):
        server = ctx.message.server
        channel = ctx.message.channel
        self.filters = fileIO("data/rolls/filters.json", "load")
        self.settings = fileIO("data/rolls/settings.json", "load")

        await self.image_get(ctx, server, channel, "gel", False, False)

    @commands.command(pass_context=True, no_pm=True)
    async def konars(self, ctx, *text):
        server = ctx.message.server
        channel = ctx.message.channel
        self.filters = fileIO("data/rolls/filters.json", "load")
        self.settings = fileIO("data/rolls/settings.json", "load")

        await self.image_get(ctx, server, channel, "kona", False, False)
    # endregion

    # region Configrolls
    @commands.group(pass_context=True)
    async def configrolls(self, ctx):
        if ctx.invoked_subcommand is None:
            self.active = fileIO("data/rolls/active.json", "load")
            await self.bot.say(self.active)

    async def toggle_switch(self, mode):
        self.active = fileIO("data/rolls/active.json", "load")
        if self.active[mode] == "true":
            self.active[mode] = "false"
            await self.bot.say(mode + " - disabled!")
        else:
            self.active[mode] = "true"
            await self.bot.say(mode + " - enabled!")
        fileIO("data/rolls/active.json", "save", self.active)

    @configrolls.command(name="loli", pass_context=True, no_pm=True)
    async def _loli_switch(self, ctx, *text):
        self.toggle_switch("loli")

    @configrolls.command(pass_context=True, no_pm=True)
    async def _kona_switch(self, ctx, *text):
        self.toggle_switch("kona")

    @configrolls.command(pass_context=True, no_pm=True)
    async def _dan_switch(self, ctx, *text):
        self.toggle_switch("dan")

    @configrolls.command(pass_context=True, no_pm=True)
    async def _gel_switch(self, ctx, *text):
        self.toggle_switch("gel")
    # endregion

    # region Support functions
    async def get_details(self, page, ident, mode):
        # Fetches the image ID
        image_id = page[ident].get('id')

        # Sets the embed title
        embed_title = self.phrases[mode]["title"].format(image_id)

        # Sets the URL to be linked
        embed_link = self.phrases[mode]["embed"].format(image_id)

        # Check for the rating and set an appropriate color
        rating = page[ident].get('rating')
        if rating == "s":
            rating_color = "00FF00"
            # rating_word = "safe"
        elif rating == "q":
            rating_color = "FF9900"
            # rating_word = "questionable"
        elif rating == "e":
            rating_color = "FF0000"
            # rating_word = "explicit"
        else:
            rating_color = "000000"

        # Initialize verbose embed
        return discord.Embed(title=embed_title, url=embed_link,
                             colour=discord.Colour(value=int(rating_color, 16)))

    async def image_get(self, ctx, server, channel, mode, lock, sync=True):
        search_phrase = self.phrases[mode]["call"]
        tag_list = ''

        # Assign tags to URL
        if server.id in self.filters:
            tag_list += " ".join(self.filters[server.id][mode])
        else:
            tag_list += " ".join(self.filters["default"][mode])
        search_phrase += parse.quote_plus(tag_list)

        if mode is not "gel":
            search_phrase += self.phrases[mode]["random"]

        if sync:
            await lock.acquire()
            m1 = await self.bot.send_message(channel, self.phrases[mode]["m1"])
            m2 = await self.bot.send_message(channel, self.phrases[mode]["m2"])
            lock.release()
        else:
            m1 = await self.bot.send_message(channel, self.phrases[mode]["m1"])
            m2 = await self.bot.send_message(channel, self.phrases[mode]["m2"])

        if mode is "gel":
            # region Gelbooru
            try:
                # Fetch the xml page to randomize the results
                async with aiohttp.get(search_phrase) as r:
                    website = await r.text()

                # Gets the amount of results
                count_start = website.find("count=\"")
                count_end = website.find("\"", count_start + 7)
                count = website[count_start + 7:count_end]

                # Picks a random page and sets the search URL to json
                pid = str(random.randint(0, int(count)))
                search_phrase += "&json=1&pid={}".format(pid)
                # Fetches the json page
                async with aiohttp.get(search_phrase) as r:
                    page = await r.json()
                if page:
                    # Sets the image URL
                    image_url = "{}".format(website[0]['file_url'])

                    output = await self.get_details(page, 0, mode)

                    # Edits the pending message with the results
                    await self.bot.edit_message(m1, "Image details", embed=output)
                    await self.bot.edit_message(m2, image_url)
                else:
                    await self.bot.edit_message(m1, "Your search terms gave no results.")
            except:
                mtype, obj, tb = sys.exc_info()
                return await self.bot.edit_message(m1, "Connection timed out. {}".join(tb.tb_lineno))
            # endregion
        elif mode is "dan":
            # region Danbooru
            try:
                async with aiohttp.get(search_phrase) as d:
                    page = await d.json()
                if page:
                    if "success" not in page:
                        fuse = 0
                        for index in range(len(page)):  # Goes through each result until it finds one that works
                            if "file_url" in page[index]:
                                # Sets the image URL
                                url = page[index].get('file_url')
                                # Hack around two different versions of image link.
                                if url[0] is 'h':
                                    image_url = url
                                else:
                                    image_url = "https://danbooru.donmai.us{}".format(url)

                                output = await self.get_details(page, index, mode)

                                # Edits the pending message with the results
                                await self.bot.edit_message(m1, "Image found.", embed=output)
                                await self.bot.edit_message(m2, image_url)
                                fuse = 1
                                break
                        if fuse == 0:
                            await self.bot.edit_message(m1, "Cannot find an image that can be viewed by you.")
                    else:
                        # Edits the pending message with an error received by the server
                        await self.bot.edit_message(m1, "{}".format(page["message"]))
                else:
                    await self.bot.edit_message(m1, "Your search terms gave no results.")
            except:
                mtype, obj, tb = sys.exc_info()
                await self.bot.edit_message(m1, "Connection timed out. {}".join(tb.tb_lineno))
            # endregion
        else:
            # region Lolibooru / Konachan
            try:
                async with aiohttp.get(search_phrase) as r:
                    page = await r.json()
                if page:
                    # Sets the image URL
                    image_url = page[0].get("file_url").replace(' ', '+')

                    output = await self.get_details(page, 0, mode)

                    # Edits the pending messages with the results
                    await self.bot.edit_message(m1, "Image found.", embed=output)
                    return await self.bot.edit_message(m2, image_url)
                else:
                    return await self.bot.edit_message(m1, "Your search terms gave no results.")
            except:
                mtype, obj, tb = sys.exc_info()
                return await self.bot.edit_message(m1, "Connection timed out. {}".join(tb.tb_lineno))
            # endregion
    # endregion


async def dummy():
    pass


def check_folder():
    if not os.path.exists("data/rolls"):
        print("Creating data/rolls folder...")
        os.makedirs("data/rolls")


def check_files():
    filters = {"default": {"loli": ["rating:safe"], "gel": ["rating:safe"], "dan": ["rating:safe"],
                           "kona": ["rating:safe"]}}
    settings = {"maxfilters": {"loli": "50", "gel": "10", "dan": "50", "kona": "50"}}
    activity = {"loli": "true", "kona": "true", "gel": "true", "dan": "true"}

    # region File checking
    if not fileIO("data/rolls/filters.json", "check"):
        print("Creating default filters.json...")
        fileIO("data/rolls/filters.json", "save", filters)
    else:
        filterlist = fileIO("data/rolls/filters.json", "load")
        if "default" not in filterlist:
            filterlist["default"] = filters["default"]
            print("Adding default filters...")
            fileIO("data/rolls/filters.json", "save", filterlist)
    if not fileIO("data/rolls/settings.json", "check"):
        print("Creating default settings.json...")
        fileIO("data/rolls/settings.json", "save", settings)
    if not fileIO("data/rolls/active.json", "check"):
        print("Creating default active.json...")
        fileIO("data/rolls/active.json", "save", activity)
    # endregion


def setup(bot):
    check_folder()
    check_files()
    bot.add_cog(ImRoll(bot))
