import random
from urllib import parse

import aiohttp
import discord
import sys
from discord.ext import commands

from .utils import checks
from .utils.dataIO import fileIO
import os
import asyncio
from __main__ import send_cmd_help
import datetime
import operator


class ImRoll:
    def __init__(self, bot):
        self.bot = bot
        self.filters = fileIO("data/rolls/filters.json", "load")
        self.settings = fileIO("data/rolls/settings.json", "load")
        self.active = fileIO("data/rolls/active.json", "load")
        self.counter = fileIO("data/rolls/counter.json", "load")
        self.bans = fileIO("data/rolls/bans.json", "load")
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

    # region Filters
    @commands.group(pass_context=True)
    async def rollfilter(self, ctx):
        """Manages filters for image providers
           Warning: Can (could and will ^^) be used to allow NSFW images

           Filters automatically apply tags to each search"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)
            
    @rollfilter.command(name="import", pass_context=True)
    async def _import_rollfilter(self, ctx):
        server = ctx.message.server
        if server.id not in self.filters:
            self.filters[server.id] = self.filters["default"]
        vals = fileIO("data/loli/filters.json", "load")
        if server.id in vals:
            self.filters[server.id]["loli"] = vals[server.id]
            fileIO("data/rolls/filters.json", "save", self.filters)
            self.filters = fileIO("data/rolls/filters.json", "load")
        else:
            await self.bot.say("Loli filters not found!")
        vals = fileIO("data/kona/filters.json", "load")
        if server.id in vals:
            self.filters[server.id]["kona"] = vals[server.id]
            fileIO("data/rolls/filters.json", "save", self.filters)
            self.filters = fileIO("data/rolls/filters.json", "load")
        else:
            await self.bot.say("Kona filters not found!")
        vals = fileIO("data/gel/filters.json", "load")
        if server.id in vals:
            self.filters[server.id]["gel"] = vals[server.id]
            fileIO("data/rolls/filters.json", "save", self.filters)
            self.filters = fileIO("data/rolls/filters.json", "load")
        else:
            await self.bot.say("Gel filters not found!")
        vals = fileIO("data/dan/filters.json", "load")
        if server.id in vals:
            self.filters[server.id]["dan"] = vals[server.id]
            fileIO("data/rolls/filters.json", "save", self.filters)
            self.filters = fileIO("data/rolls/filters.json", "load")
        else:
            await self.bot.say("Dan filters not found!")

    @rollfilter.command(name="show", pass_context=True)
    async def _filters_show(self, ctx):
        server = ctx.message.server
        if server.id in self.filters:
            list_tags = '\n'.join(sorted(self.filters[server.id]["loli"]))
            await self.bot.say("Loli filter list: ```\n{}```".format(list_tags))
            list_tags = '\n'.join(sorted(self.filters[server.id]["kona"]))
            await self.bot.say("Kona filter list: ```\n{}```".format(list_tags))
            list_tags = '\n'.join(sorted(self.filters[server.id]["gel"]))
            await self.bot.say("Gel filter list: ```\n{}```".format(list_tags))
            list_tags = '\n'.join(sorted(self.filters[server.id]["dan"]))
            await self.bot.say("Dan filter list: ```\n{}```".format(list_tags))
        else:
            await self.bot.say("No custom filters found!")

    @rollfilter.command(name="loli", pass_context=True)
    async def _loli_rollfilter(self, ctx, operation, tag):
        """Manages filters for Lolibooru
           Warning: Can (could and will ^^) be used to allow NSFW images

           Filters automatically apply tags to each search"""
        if "add" in operation:
            await self.filter_add(ctx, "loli", tag)
        elif "del" in operation:
            await self.filter_del(ctx, "loli", tag)
        elif "show" in operation:
            await self.bot.say(self.filters[ctx.message.server.id]["loli"])

    @rollfilter.command(name="dan", pass_context=True)
    async def _dan_rollfilter(self, ctx, operation, tag):
        """Manages filters for Danbooru
           Warning: Can (could and will ^^) be used to allow NSFW images

           Filters automatically apply tags to each search"""
        if "add" in operation:
            await self.filter_add(ctx, "dan", tag)
        elif "del" in operation:
            await self.filter_del(ctx, "dan", tag)
        elif "show" in operation:
            await self.bot.say(self.filters[ctx.message.server.id]["dan"])

    @rollfilter.command(name="gel", pass_context=True)
    async def _gel_rollfilter(self, ctx, operation, tag):
        """Manages filters for Gelbooru
           Warning: Can (could and will ^^) be used to allow NSFW images

           Filters automatically apply tags to each search"""
        if "add" in operation:
            await self.filter_add(ctx, "gel", tag)
        elif "del" in operation:
            await self.filter_del(ctx, "gel", tag)
        elif "show" in operation:
            await self.bot.say(self.filters[ctx.message.server.id]["gel"])

    @rollfilter.command(name="kona", pass_context=True)
    async def _kona_rollfilter(self, ctx, operation, tag):
        """Manages filters for Konachan
           Warning: Can (could and will ^^) be used to allow NSFW images

           Filters automatically apply tags to each search"""
        if "add" in operation:
            await self.filter_add(ctx, "kona", tag)
        elif "del" in operation:
            await self.filter_del(ctx, "kona", tag)
        elif "show" in operation:
            await self.bot.say(self.filters[ctx.message.server.id]["kona"])
    # endregion

    # region Settings
    @commands.command(no_pm=True)
    async def maxfilters(self, mod, maxfilters):
        """Sets the global tag limit for the filter list

           Gives an error when a user tries to add a filter while the server's filter list
           contains a certain amount of tags
           """
        self.settings["maxfilters"][mod] = maxfilters
        fileIO("data/rolls/settings.json", "save", self.settings)
        await self.bot.say("Maximum filters allowed per server for {} set to '{}'.".format(mod, maxfilters))
    # endregion

    # region Counter
    async def check_time(self, date_string, now):
        long_date = "{}.{}.{} {}:{}".format(now.day, now.month, now.year, now.hour, now.minute)
        event_time = datetime.datetime.strptime(date_string, "%d.%m.%Y %H:%M")
        current_time = datetime.datetime.strptime(long_date, "%d.%m.%Y %H:%M")
        return current_time - event_time

    async def log_roll(self, server_id):
        now = datetime.datetime.now()
        time_delta = await self.check_time(self.counter[server_id]["roll_date"], now)
        if time_delta >= datetime.timedelta(days=1):
            self.counter[server_id]["yesterday"] = self.counter[server_id]["today"]
            self.counter[server_id]["today"] = {}
            log_roll_date = "{}.{}.{} {}:{}".format(now.day, now.month, now.year, 5, 0)
            self.counter[server_id]["roll_date"] = log_roll_date
            fileIO("data/rolls/counter.json", "save", self.counter)

    @commands.command(pass_context=True, no_pm=True)
    async def fapcounter(self, ctx, *text):
        server = ctx.message.server
        if server.id not in self.counter:
            await self.bot.say("No statistics for this server. Zone-tan is not pleased ;(")
        else:
            await self.log_roll(server.id)
            ovals = self.counter[server.id]["values"].items()
            vals = []
            for mtuple in ovals:
                vals.append((mtuple[0], int(mtuple[1])))
            names = sorted(vals, key=operator.itemgetter(1), reverse=True)
            list_tags = ""
            for mtuple in names:
                list_tags += "{} - {}\n".format(mtuple[0], mtuple[1])
            await self.bot.say(
                "Since {}, Zone-tan kept track of your faps: ```\n👑{}```".format(self.counter[server.id]["date"],
                                                                                 list_tags))
            ovals = self.counter[server.id]["yesterday"].items()
            vals = []
            for mtuple in ovals:
                vals.append((mtuple[0], int(mtuple[1])))
            names = sorted(vals, key=operator.itemgetter(1), reverse=True)
            list_tags = ""
            for mtuple in names:
                list_tags += "{} - {}\n".format(mtuple[0], mtuple[1])
            await self.bot.say(
                "Yesterday: ```\n👑{}```".format(list_tags))
            ovals = self.counter[server.id]["today"].items()
            vals = []
            for mtuple in ovals:
                vals.append((mtuple[0], int(mtuple[1])))
            names = sorted(vals, key=operator.itemgetter(1), reverse=True)
            list_tags = ""
            for mtuple in names:
                list_tags += "{} - {}\n".format(mtuple[0], mtuple[1])
            await self.bot.say(
                "Today: ```\n👑{}```".format(list_tags))

    async def add_fap(self, ctx):
        server = ctx.message.server
        user = ctx.message.author.name
        now = datetime.datetime.now()
        long_date = "{}.{}.{} {}:{}".format(now.day, now.month, now.year, now.hour, now.minute)
        if server.id not in self.counter:
            date = "{}.{}.{}".format(now.day, now.month, now.year)
            log_roll_date = "{}.{}.{} {}:{}".format(now.day, now.month, now.year, 5, 0)
            self.counter[server.id] = {"date": date, "roll_date": log_roll_date, "values": {}, "yesterday": {}, "today": {}}
            fileIO("data/rolls/counter.json", "save", self.counter)
            self.counter = fileIO("data/rolls/counter.json", "load")
        if user not in self.counter[server.id]["values"]:
            self.counter[server.id]["values"][user] = "1"
            fileIO("data/rolls/counter.json", "save", self.counter)
        else:
            # Trust me, I am engineer ^^
            self.counter[server.id]["values"][user] = str(int(self.counter[server.id]["values"][user])+1)
            fileIO("data/rolls/counter.json", "save", self.counter)
        await self.log_roll(server.id)
        if user not in self.counter[server.id]["today"]:
            self.counter[server.id]["today"][user] = "1"
            fileIO("data/rolls/counter.json", "save", self.counter)
        else:
            # Trust me, I am engineer ^^
            self.counter[server.id]["today"][user] = str(int(self.counter[server.id]["today"][user])+1)
            if int(self.counter[server.id]["today"][user]) > int(self.bans[server.id]["rules"]["daily"]):
                if user not in self.bans[server.id]["whitelist"]:
                    await self.bot.say("You are not allowed to fap for next {} day(s)"
                                       .format(self.bans[server.id]["rules"]["VACation"]))
                else:
                    await self.bot.say("Your reputation lets you avoid banishment.")
            fileIO("data/rolls/counter.json", "save", self.counter)
    # endregion

    # region Group rolls
    @commands.command(pass_context=True, no_pm=True)
    async def imroll(self, ctx, *text):
        server = ctx.message.server
        channel = ctx.message.channel
        self.filters = fileIO("data/rolls/filters.json", "load")
        self.settings = fileIO("data/rolls/settings.json", "load")
        self.active = fileIO("data/rolls/active.json", "load")
        self.counter = fileIO("data/rolls/counter.json", "load")
        await self.add_fap(ctx)

        lock = asyncio.Lock()
        await asyncio.gather(
            self.image_get(ctx, server, channel, "loli", lock) if self.active["current"]["loli"] == "true" else dummy(),
            self.image_get(ctx, server, channel, "dan", lock) if self.active["current"]["dan"] == "true" else dummy(),
            self.image_get(ctx, server, channel, "gel", lock) if self.active["current"]["gel"] == "true" else dummy(),
            self.image_get(ctx, server, channel, "kona", lock) if self.active["current"]["kona"] == "true" else dummy(),
        )

    @commands.command(pass_context=True, no_pm=True)
    async def imrollf(self, ctx, *text):
        server = ctx.message.server
        channel = ctx.message.channel
        self.filters = fileIO("data/rolls/filters.json", "load")
        self.settings = fileIO("data/rolls/settings.json", "load")
        self.active = fileIO("data/rolls/active.json", "load")
        self.counter = fileIO("data/rolls/counter.json", "load")
        await self.add_fap(ctx)

        await asyncio.gather(
            self.image_get(ctx, server, channel, "loli", False, False) if self.active["current"][
                                                                              "loli"] == "true" else dummy(),
            self.image_get(ctx, server, channel, "dan", False, False) if self.active["current"][
                                                                             "dan"] == "true" else dummy(),
            self.image_get(ctx, server, channel, "gel", False, False) if self.active["current"][
                                                                             "gel"] == "true" else dummy(),
            self.image_get(ctx, server, channel, "kona", False, False) if self.active["current"][
                                                                              "kona"] == "true" else dummy(),
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
            await self.bot.say("```{}```".format(self.active["current"]))

    async def toggle_switch(self, mode):
        self.active = fileIO("data/rolls/active.json", "load")
        if self.active["current"][mode] == "true":
            self.active["current"][mode] = "false"
            await self.bot.say(mode + " - disabled!")
        else:
            self.active["current"][mode] = "true"
            await self.bot.say(mode + " - enabled!")
        fileIO("data/rolls/active.json", "save", self.active)

    @configrolls.command(name="loli", pass_context=True, no_pm=True)
    @checks.is_owner()
    async def _loli_switch(self, ctx, *text):
        await self.toggle_switch("loli")

    @configrolls.command(name="kona", pass_context=True, no_pm=True)
    @checks.is_owner()
    async def _kona_switch(self, ctx, *text):
        await self.toggle_switch("kona")

    @configrolls.command(name="dan", pass_context=True, no_pm=True)
    @checks.is_owner()
    async def _dan_switch(self, ctx, *text):
        await self.toggle_switch("dan")

    @configrolls.command(name="gel", pass_context=True, no_pm=True)
    @checks.is_owner()
    async def _gel_switch(self, ctx, *text):
        await self.toggle_switch("gel")

    @commands.command(no_pm=True)
    @checks.is_owner()
    async def killswitch(self):
        if self.active["killed"] != "True":
            self.active["backup"] = self.active["current"]
            self.active["current"] = {"loli": "false", "kona": "false", "gel": "false", "dan": "false"}
            self.active["killed"] = "True"
            fileIO("data/rolls/active.json", "save", self.active)
            await self.bot.say("Disabled")

    @commands.command(no_pm=True)
    @checks.is_owner()
    async def dekillswitch(self):
        if self.active["killed"] == "True":
            self.active["current"] = self.active["backup"]
            self.active["killed"] = "False"
            fileIO("data/rolls/active.json", "save", self.active)
            await self.bot.say("Enabled")
    # endregion

    # region Support functions
    async def filter_add(self, ctx, mod, tag):
        server = ctx.message.server
        if server.id not in self.filters:
            self.filters[server.id] = self.filters["default"]
            fileIO("data/rolls/filters.json", "save", self.filters)
            self.filters = fileIO("data/rolls/filters.json", "load")
        if len(self.filters[server.id][mod]) < int(self.settings["maxfilters"][mod]):
            if tag not in self.filters[server.id][mod]:
                self.filters[server.id][mod].append(tag)
                fileIO("data/rolls/filters.json", "save", self.filters)
                await self.bot.say("Filter '{}' added to the server's {} filter list.".format(tag, mod))
            else:
                await self.bot.say(
                    "Filter '{}' is already in the server's {} filter list.".format(tag, mod))
        else:
            await self.bot.say("This server has exceeded the maximum filters ({}/{})."
                               " https://www.youtube.com/watch?v=1MelZ7xaacs".format(
                                len(self.filters[server.id][mod]), self.settings["maxfilters"][mod]))

    async def filter_del(self, ctx, mod, tag):
        server = ctx.message.server
        if len(tag) > 0:
            if server.id not in self.filters:
                self.filters[server.id] = self.filters["default"]
                fileIO("data/rolls/filters.json", "save", self.filters)
                self.filters = fileIO("data/rolls/filters.json", "load")
            if tag in self.filters[server.id][mod]:
                self.filters[server.id][mod].remove(tag)
                fileIO("data/rolls/filters.json", "save", self.filters)
                await self.bot.say("Filter '{}' deleted from the server's {} filter list.".format(tag, mod))
            else:
                await self.bot.say("Filter '{}' does not exist in the server's {} filter list.".format(tag, mod))
        else:
            if server.id in self.filters:
                del self.filters[server.id][mod]
                fileIO("data/rolls/filters.json", "save", self.filters)
                await self.bot.say("Reverted the server to the default {} filter list.".format(mod))
            else:
                await self.bot.say("Server is already using the default {} filter list.".format(mod))

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
                    await self.bot.edit_message(m1, "As requested by: {}".format(ctx.message.author.name), embed=output)
                    await self.bot.edit_message(m2, "{}: {}".format(ctx.message.author.name, image_url))
                else:
                    await self.bot.edit_message(m1, "Server gave no response.")
            except:
                mtype, obj, tb = sys.exc_info()
                return await self.bot.edit_message(m1, "Error during request processing. Exception raised in line: {}"
                                                       .format(tb.tb_lineno))
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
                                await self.bot.edit_message(m1, "As requested by: {}".format(ctx.message.author.name),
                                                            embed=output)
                                await self.bot.edit_message(m2, "{}: {}".format(ctx.message.author.name, image_url))
                                fuse = 1
                                break
                        if fuse == 0:
                            await self.bot.edit_message(m1, "Cannot find an image that can be viewed by you.")
                    else:
                        # Edits the pending message with an error received by the server
                        await self.bot.edit_message(m1, "{}".format(page["message"]))
                else:
                    await self.bot.edit_message(m1, "Server gave no response.")
            except:
                mtype, obj, tb = sys.exc_info()
                await self.bot.edit_message(m1, "Error during request processing. Exception raised in line: {}"
                                                .format(tb.tb_lineno))
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
                    await self.bot.edit_message(m1, "As requested by: {}".format(ctx.message.author.name), embed=output)
                    await self.bot.edit_message(m2, "{}: {}".format(ctx.message.author.name, image_url))
                else:
                    return await self.bot.edit_message(m1, "Server gave no response.")
            except:
                mtype, obj, tb = sys.exc_info()
                return await self.bot.edit_message(m1, "Error during request processing. Exception raised in line: {}"
                                                       .format(tb.tb_lineno))
            # endregion
    # endregion


async def dummy():
    pass


def check_folder():
    if not os.path.exists("data/rolls"):
        print("Creating data/rolls folder...")
        os.makedirs("data/rolls")


def check_files():
    now = datetime.datetime.now()
    date = "{}.{}.{}".format(now.day, now.month, now.year)
    filters = {"default": {"loli": ["rating:safe"], "gel": ["rating:safe"], "dan": ["rating:safe"],
                           "kona": ["rating:safe"]}}
    settings = {"maxfilters": {"loli": "50", "gel": "10", "dan": "50", "kona": "50"}}
    activity = {"current": {"loli": "true", "kona": "true", "gel": "false", "dan": "true"},
                "backup": {"loli": "true", "kona": "true", "gel": "false", "dan": "true"},
                "killed": "False"}
    counter = {"default": {"date": date}}
    banned = {"ban": {}, "whitelist": [], "rules": {"daily": "50", "VACation": "7"}}

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
    if not fileIO("data/rolls/counter.json", "check"):
        print("Creating default counter.json...")
        fileIO("data/rolls/counter.json", "save", counter)
    if not fileIO("data/rolls/bans.json", "check"):
        print("Creating default bans.json...")
        fileIO("data/rolls/bans.json", "save", counter)
    # endregion


def setup(bot):
    check_folder()
    check_files()
    bot.add_cog(ImRoll(bot))