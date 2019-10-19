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
    

   

    # region Group rolls
    @commands.command(pass_context=True, no_pm=True)
    async def imroll(self, ctx, *text):
        """
        Generates set of images in ordered manner.
        """
        server = ctx.message.server
        channel = ctx.message.channel
        user = ctx.message.author.name
        if self.active["killed"] != "True":
            if not self.check_ban(user, server.id):
                self.filters = fileIO("data/rolls/filters.json", "load")
                self.settings = fileIO("data/rolls/settings.json", "load")
                self.active = fileIO("data/rolls/active.json", "load")
                self.counter = fileIO("data/rolls/counter.json", "load")
                await self.add_roll(ctx)

                lock = asyncio.Lock()
                await asyncio.gather(
                    self.image_get(ctx, server, channel, "loli", lock) if self.active["current"]["loli"] == "true" else dummy(),
                    self.image_get(ctx, server, channel, "dan", lock) if self.active["current"]["dan"] == "true" else dummy(),
                    self.image_get(ctx, server, channel, "gel", lock) if self.active["current"]["gel"] == "true" else dummy(),
                    self.image_get(ctx, server, channel, "kona", lock) if self.active["current"]["kona"] == "true" else dummy(),
                )
            else:
                await self.bot.say(self.get_random_string("GTFO").replace("%u", user))
        else:
            await self.bot.say(self.get_random_string("disabled_info"))

    @commands.command(pass_context=True, no_pm=True)
    async def imrollf(self, ctx, *text):
        """
        Generates set of images in unordered manner.
        """
        server = ctx.message.server
        channel = ctx.message.channel
        user = ctx.message.author.name
        if self.active["killed"] != "True":
            if not self.check_ban(user, server.id):
                self.filters = fileIO("data/rolls/filters.json", "load")
                self.settings = fileIO("data/rolls/settings.json", "load")
                self.active = fileIO("data/rolls/active.json", "load")
                self.counter = fileIO("data/rolls/counter.json", "load")
                await self.add_roll(ctx)

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
            else:
                await self.bot.say(self.get_random_string("GTFO").replace("%u", user))
        else:
            await self.bot.say(self.get_random_string("disabled_info"))
    # endregion

    # region Single rolls
    @commands.command(pass_context=True, no_pm=True)
    async def lolirs(self, ctx, *text):
        """
        Generates image form lolibooru.
        """
        server = ctx.message.server
        channel = ctx.message.channel
        user = ctx.message.author.name
        if self.active["killed"] != "True":
            if not self.check_ban(user, server.id):
                self.filters = fileIO("data/rolls/filters.json", "load")
                self.settings = fileIO("data/rolls/settings.json", "load")

                await self.image_get(ctx, server, channel, "loli", False, False)
            else:
                await self.bot.say(self.get_random_string("GTFO").replace("%u", user))
        else:
            await self.bot.say(self.get_random_string("disabled_info"))

    @commands.command(pass_context=True, no_pm=True)
    async def danrs(self, ctx, *text):
        """
        Generates image form danbooru.
        """
        server = ctx.message.server
        channel = ctx.message.channel
        user = ctx.message.author.name
        if self.active["killed"] != "True":
            if not self.check_ban(user, server.id):
                self.filters = fileIO("data/rolls/filters.json", "load")
                self.settings = fileIO("data/rolls/settings.json", "load")

                await self.image_get(ctx, server, channel, "dan", False, False)
            else:
                await self.bot.say(self.get_random_string("GTFO").replace("%u", user))
        else:
            await self.bot.say(self.get_random_string("disabled_info"))

    @commands.command(pass_context=True, no_pm=True)
    async def gelrs(self, ctx, *text):
        """
        Generates image form gelbooru.
        """
        server = ctx.message.server
        channel = ctx.message.channel
        user = ctx.message.author.name
        if self.active["killed"] != "True":
            if not self.check_ban(user, server.id):
                self.filters = fileIO("data/rolls/filters.json", "load")
                self.settings = fileIO("data/rolls/settings.json", "load")

                await self.image_get(ctx, server, channel, "gel", False, False)
            else:
                await self.bot.say(self.get_random_string("GTFO").replace("%u", user))
        else:
            await self.bot.say(self.get_random_string("disabled_info"))

    @commands.command(pass_context=True, no_pm=True)
    async def konars(self, ctx, *text):
        """
        Generates image form konachan.
        """
        server = ctx.message.server
        channel = ctx.message.channel
        user = ctx.message.author.name
        if self.active["killed"] != "True":
            if not self.check_ban(user, server.id):
                self.filters = fileIO("data/rolls/filters.json", "load")
                self.settings = fileIO("data/rolls/settings.json", "load")

                await self.image_get(ctx, server, channel, "kona", False, False)
            else:
                await self.bot.say(self.get_random_string("GTFO").replace("%u", user))
        else:
            await self.bot.say(self.get_random_string("disabled_info"))
    # endregion

    # region Configrolls
    @commands.group(pass_context=True)
    async def configrolls(self, ctx):
        """
        Displays active configuration of enabled servers.
        """
        if ctx.invoked_subcommand is None:
            self.active = fileIO("data/rolls/active.json", "load")
            await self.bot.say("```{}```".format(self.active["current"]))

    async def toggle_switch(self, server):
        """
        Switches state of server.
        """
        self.active = fileIO("data/rolls/active.json", "load")
        if self.active["current"][server] == "true":
            self.active["current"][server] = "false"
            await self.bot.say(self.get_random_string("sth_disabled").format(server))
        else:
            self.active["current"][server] = "true"
            await self.bot.say(self.get_random_string("sth_enabled").format(server))
        fileIO("data/rolls/active.json", "save", self.active)

    @configrolls.command(name="loli", pass_context=True, no_pm=True)
    @checks.is_owner()
    async def _loli_switch(self, ctx, *text):
        """
        Toggles availability of lolibooru.
        """
        await self.toggle_switch("loli")

    @configrolls.command(name="kona", pass_context=True, no_pm=True)
    @checks.is_owner()
    async def _kona_switch(self, ctx, *text):
        """
        Toggles availability of konachan.
        """
        await self.toggle_switch("kona")

    @configrolls.command(name="dan", pass_context=True, no_pm=True)
    @checks.is_owner()
    async def _dan_switch(self, ctx, *text):
        """
        Toggles availability of danbooru.
        """
        await self.toggle_switch("dan")

    @configrolls.command(name="gel", pass_context=True, no_pm=True)
    @checks.is_owner()
    async def _gel_switch(self, ctx, *text):
        """
        Toggles availability of gelbooru.
        """
        await self.toggle_switch("gel")

    @commands.command(no_pm=True)
    @checks.is_owner()
    async def killswitch(self):
        """
        Disables all image generating functions.
        """
        if self.active["killed"] != "True":
            self.active["killed"] = "True"
            fileIO("data/rolls/active.json", "save", self.active)
            await self.bot.say("Disabled")

    @commands.command(no_pm=True)
    @checks.is_owner()
    async def dekillswitch(self):
        """
        Reenables status of image generating functions.
        """
        if self.active["killed"] == "True":
            self.active["killed"] = "False"
            fileIO("data/rolls/active.json", "save", self.active)
            await self.bot.say("Enabled")
    # endregion

   
    def get_details(self, page, iterator, mode):
        """
        Generates embed message for image.
        """
        # Fetches the image ID
        image_id = page[iterator].get('id')

        # Sets the embed title
        embed_title = self.phrases[mode]["title"].format(image_id)

        # Sets the URL to be linked
        embed_link = self.phrases[mode]["embed"].format(image_id)

        # Check for the rating and set an appropriate color
        rating = page[iterator].get('rating')
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
        """
        Fetches image from specified server, and passes result messages to specified server.
        """
        search_phrase = self.phrases[mode]["call"]
        tag_list = ''
        httpclient = aiohttp.ClientSession()

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
                async with httpclient.get(search_phrase, headers={'User-Agent': "blali733-cogs (https://git.io/vpCIl)"}) as r:
                    website = await r.text()

                # Gets the amount of results
                count_start = website.find("count=\"")
                count_end = website.find("\"", count_start + 7)
                count = website[count_start + 7:count_end]

                # Picks a random page and sets the search URL to json
                pid = str(random.randint(0, int(count)))
                search_phrase += "&json=1&pid={}".format(pid)
                # Fetches the json page
                async with httpclient.get(search_phrase,
                                          headers={'User-Agent': "blali733-cogs (https://git.io/vpCIl)"}) as r:
                    page = await r.json()
                if page:
                    # Sets the image URL
                    image_url = "{}".format(website[0]['file_url'])

                    output = self.get_details(page, 0, mode)

                    # Edits the pending message with the results
                    await self.bot.edit_message(m1, self.get_random_string("m1")
                                                .format(ctx.message.author.name), embed=output)
                    await self.bot.edit_message(m2, self.get_random_string("m2")
                                                .format(ctx.message.author.name, image_url))
                else:
                    await self.bot.edit_message(m1, self.get_random_string("no_response"))
            except:
                mtype, obj, tb = sys.exc_info()
                return await self.bot.edit_message(m1, self.get_random_string("request_error").format(tb.tb_lineno))
            # endregion
        elif mode is "dan":
            # region Danbooru
            try:
                async with httpclient.get(search_phrase,
                                          headers={'User-Agent': "blali733-cogs (https://git.io/vpCIl)"}) as d:
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

                                output = self.get_details(page, index, mode)

                                # Edits the pending message with the results
                                await self.bot.edit_message(m1, self.get_random_string("m1")
                                                            .format(ctx.message.author.name), embed=output)
                                await self.bot.edit_message(m2, self.get_random_string("m2")
                                                            .format(ctx.message.author.name, image_url))
                                fuse = 1
                                break
                        if fuse == 0:
                            await self.bot.edit_message(m1, self.get_random_string("no_result"))
                    else:
                        # Edits the pending message with an error received by the server
                        await self.bot.edit_message(m1, "{}".format(page["message"]))
                else:
                    await self.bot.edit_message(m1, self.get_random_string("no_response"))
            except:
                mtype, obj, tb = sys.exc_info()
                await self.bot.edit_message(m1, self.get_random_string("request_error").format(tb.tb_lineno))
            # endregion
        else:
            # region Lolibooru / Konachan
            try:
                async with httpclient.get(search_phrase,
                                          headers={'User-Agent': "blali733-cogs (https://git.io/vpCIl)"}) as r:
                    page = await r.json()
                if page:
                    # Sets the image URL
                    image_url = page[0].get("file_url").replace(' ', '+')

                    output = self.get_details(page, 0, mode)

                    # Edits the pending messages with the results
                    await self.bot.edit_message(m1, self.get_random_string("m1").format(ctx.message.author.name),
                                                embed=output)
                    await self.bot.edit_message(m2, self.get_random_string("m2").format(ctx.message.author.name,
                                                                                        image_url))
                else:
                    return await self.bot.edit_message(m1, self.get_random_string("no_response"))
            except:
                mtype, obj, tb = sys.exc_info()
                return await self.bot.edit_message(m1, self.get_random_string("request_error").format(tb.tb_lineno))
            # endregion
    # endregion


async def dummy():
    """
    Permanently bugless function - does nothing.
    """
    pass
