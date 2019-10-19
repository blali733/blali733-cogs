import random
from redbot.core import commands
from redbot.core import Config
from __main__ import send_cmd_help
from .defaultProvider import DefaultProvider


class ImRoll(commands.Cog):

    def __init__(self):
        self.conf = Config.get_conf(self, identifier=666123666)

        provider = DefaultProvider()

        default_guild = {
            'filters': provider.get_filters(),
            'settings': provider.get_settings(),
            'active': provider.get_active(),
            'counter': provider.get_counter(),
            'bans': provider.get_bans(),
            'strings': provider.get_strings(),
        }

        self.conf.register_guild(**default_guild)

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

    # region Strings
    def get_random_string(self, string_type):
        return await self.conf.get_raw('strings', string_type, random.randint(0, len(await self.conf.get_raw('strings', string_type))-1))

    def get_string(self, string_type, iterator):
        return await self.conf.get_raw('strings', string_type, iterator)
    # endregion

    # region Filters
    @commands.group()
    async def rollfilter(self, ctx):
        """
        Manages filters for image providers
        Warning: Can (could and will ^^) be used to allow NSFW images

        Filters automatically apply tags to each search
        """
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @rollfilter.command(name="show")
    async def _filters_show(self, ctx):
        """
        Shows list of filters for each image provider.
        """
        guild = ctx.message.guild
        if guild.id in self.filters:
            order = ["loli", "dan", "kona", "gel"]
            for mod in order:
                list_tags = '\n'.join(sorted(await self.conf.get_raw('filters', guild.id, mod))
                await self.ctx.send(self.get_random_string("filter_list").format(mod.title(), list_tags))
        else:
            await self.ctx.send(self.get_random_string("filter_no_custom"))

    @rollfilter.command(name="loli")
    async def _loli_rollfilter(self, ctx, operation, tag):
        """Manages filters for Lolibooru
           Warning: Can (could and will ^^) be used to allow NSFW images

           Filters automatically apply tags to each search"""
        if "add" in operation:
            await self.filter_add(ctx, "loli", tag)
        elif "del" in operation:
            await self.filter_del(ctx, "loli", tag)
        elif "show" in operation:
            await self.ctx.send(await self.conf.get_raw('filters', ctx.message.guild.id, 'loli'))

    @rollfilter.command(name="dan")
    async def _dan_rollfilter(self, ctx, operation, tag):
        """Manages filters for Danbooru
           Warning: Can (could and will ^^) be used to allow NSFW images

           Filters automatically apply tags to each search"""
        if "add" in operation:
            await self.filter_add(ctx, "dan", tag)
        elif "del" in operation:
            await self.filter_del(ctx, "dan", tag)
        elif "show" in operation:
            await self.ctx.send(await self.conf.get_raw('filters', ctx.message.guild.id, 'dan'))

    @rollfilter.command(name="gel")
    async def _gel_rollfilter(self, ctx, operation, tag):
        """Manages filters for Gelbooru
           Warning: Can (could and will ^^) be used to allow NSFW images

           Filters automatically apply tags to each search"""
        if "add" in operation:
            await self.filter_add(ctx, "gel", tag)
        elif "del" in operation:
            await self.filter_del(ctx, "gel", tag)
        elif "show" in operation:
            await self.ctx.send(await self.conf.get_raw('filters', ctx.message.guild.id, 'gel'))

    @rollfilter.command(name="kona")
    async def _kona_rollfilter(self, ctx, operation, tag):
        """Manages filters for Konachan
           Warning: Can (could and will ^^) be used to allow NSFW images

           Filters automatically apply tags to each search"""
        if "add" in operation:
            await self.filter_add(ctx, "kona", tag)
        elif "del" in operation:
            await self.filter_del(ctx, "kona", tag)
        elif "show" in operation:
            await self.ctx.send(await self.conf.get_raw('filters', ctx.message.guild.id, 'kona'))
    # endregion

    # region Support functions
    async def filter_add(self, ctx, mod, tag):
        """
        Adds tag to list of active tags of server.
        """
        guild=ctx.message.guild
        if guild.id not in await self.conf.get_raw('filters'):
            await self.conf.set_raw('filters', guild.id, value=await self.conf.get_raw('filters', 'default')
        if len(await self.conf.get_raw('filters', guild.id, mod)) < int(await self.conf.get_raw('settings', 'maxfilters', mod)):
            if tag not in await self.conf.get_raw('filters', guild.id, mod):
                await self.conf.set_raw('filters', guild.id, mod, value=await self.conf.get_raw(
                    'filters', guild.id, mod).append(tag))
                await self.ctx.send(self.get_random_string("filter_add").format(tag, mod))
            else:
                await self.ctx.send(self.get_random_string("filter_exists").format(tag, mod))
        else:
            await self.ctx.send(self.get_random_string("filter_max").format(
                                len(await self.conf.get_raw('filters', guild.id, mod)), await self.conf.get_raw('settings', 'maxfilters', mod))

    async def filter_del(self, ctx, mod, tag):
        """
        Deletes tag from list of selected server. Reverts to default when no tag is given.
        """
        guild=ctx.message.guild
        if len(tag) > 0:
            if guild.id not in await self.conf.get_raw('filters'):
                 await self.conf.set_raw('filters', guild.id, value=await self.conf.get_raw('filters', 'default')
            if tag in await self.conf.get_raw('filters', guild.id, mod):
                await self.conf.set_raw('filters', guild.id, mod, value=await self.conf.get_raw(
                    'filters', guild.id, mod).remove(tag))
                await self.ctx.send(self.get_random_string("filter_del").format(tag, mod))
            else:
                await self.ctx.send(self.get_random_string("filter_not_existing").format(tag, mod))
        else:
            if guild.id in await self.conf.get_raw('filters'):
                await self.conf.set_raw('filters', guild.id, value=await self.conf.get_raw(
                    'filters', guild.id).remove(mod))
                await self.ctx.send(self.get_random_string("filter_revert").format(mod))
            else:
                await self.ctx.send(self.get_random_string("filter_default").format(mod))

    # region Settings
    @commands.command(no_pm=True)
    async def maxfilters(self, mod, maxfilters):
        """
        Sets the global tag limit for the filter list

        Gives an error when a user tries to add a filter while the server's filter list
        contains a certain amount of tags
        """
        # TODO - rework this solution
         await self.conf.set_raw('settings', 'maxfilters', mod, value=maxfilters)
        await self.ctx.send("Maximum filters allowed per server for {} set to '{}'.".format(mod, maxfilters))
    # endregion

    # region Counter
    def check_time(self, date_string, now):
        """
        Returns timedelta between date_string and now.
        """
        long_date="{}.{}.{} {}:{}".format(
            now.day, now.month, now.year, now.hour, now.minute)
        event_time=datetime.datetime.strptime(date_string, "%d.%m.%Y %H:%M")
        current_time=datetime.datetime.strptime(long_date, "%d.%m.%Y %H:%M")
        return current_time - event_time

    def check_ban(self, user, guild_id):
        """
        Checks if user is banned or not.

        Returns True for active ban, and False for clean users.
        """
        now=datetime.datetime.now()
        if user not in await self.conf.get_raw('bans', guild_id, 'ban'):
            return False
        else:
            time_delta=self.check_time(await self.conf.get_raw(
                'bans', guild_id, 'ban', user), now)
            if time_delta >= datetime.timedelta(days=int(await self.conf.get_raw('bans', guild_id, 'rules', 'VACation'))):
                await self.conf.set_raw('bans', guild_id, 'ban', value=await self.conf.get_raw(
                    'bans', guild_id, 'ban').remove(user))
                return False
            else:
                return True

    async def log_roll(self, guild_id):
        """
        Checks if day passed since last change of log roll, and performs it if necessary.
        """
        now=datetime.datetime.now()
        time_delta=self.check_time(await self.conf.get_raw('counter', guild_id, 'roll_date', now))
        if time_delta >= datetime.timedelta(days=1):
            await self.conf.set_raw('counter', guild_id, 'yesterday', value=await self.conf.get_raw('counter', guild_id, 'today'))
            await self.conf.set_raw('counter', guild_id, 'today', value={}})
            log_roll_date="{}.{}.{} {}:{}".format(
                now.day, now.month, now.year, 5, 0)
            await self.conf.set_raw('counter', guild_id, 'roll_date', value=log_roll_date)

    @commands.command(no_pm=True)
    async def roll_counter(self, ctx, *text):
        """
        Displays statistics of imroll command usage (or it's abuse).
        """
        guild=ctx.message.guild
        if guild.id not in await self.conf.get_raw('counter'):
            await self.ctx.send(self.get_random_string("stats_empty"))
        else:
            await self.log_roll(guild.id)
            order=["values", "yesterday", "today"]
            for mode in order:
                ovals=await self.conf.get_raw('counter', guild.id, mode).items()
                vals=[]
                for mtuple in ovals:
                    vals.append((mtuple[0], int(mtuple[1])))
                names=sorted(vals, key=operator.itemgetter(1), reverse=True)
                list_tags=""
                for mtuple in names:
                    list_tags += "{} - {}\n".format(mtuple[0], mtuple[1])
                if mode is "values":
                    await self.ctx.send(self.get_random_string("stats_overall")
                                       .format(await self.conf.get_raw('counter', guild.id, 'date'), list_tags))
                else:
                    await self.ctx.send(self.get_random_string("stats_daily").format(mode.title(), list_tags))

    async def add_roll(self, ctx):
        """
        Adds performed roll to log.
        """
        # TODO - remove code repetitions
        guild=ctx.message.guild
        if guild.id not in await self.conf.get_raw('bans'):
            self.conf.set_raw('bans', guild.id,
                              value=await self.conf.get_raw('bans', 'default'))
        user=ctx.message.author.name
        now=datetime.datetime.now()
        if guild.id not in await self.conf.get_raw('counter'):
            date="{}.{}.{}".format(now.day, now.month, now.year)
            log_roll_date="{}.{}.{} {}:{}".format(
                now.day, now.month, now.year, 5, 0)
            await self.conf.set_raw('counter', guild.id, value={"date": date, "roll_date": log_roll_date, "values": {
                }, "yesterday": {}, "today": {}})
        if user not in await self.conf.get_raw('counter', guild.id, 'values'):
            await self.conf.set_raw('counter', guild.id, 'values', user, value="1")
        else:
            # Trust me, I am engineer ^^
            await self.conf.set_raw('counter', guild.id, 'values', user, value=str(
                int(await self.conf.get_raw('counter', guild.id, 'values', user))+1))
        await self.log_roll(guild.id)
        if user not in await self.conf.get_raw('counter', guild.id, 'today'):
            await self.conf.set_raw('counter', guild.id, 'today', user, value="1")
        else:
            # Trust me, I am engineer ^^
            await self.conf.set_raw('counter', guild.id, 'today', user, value=str(
                int(await self.conf.get_raw('counter', guild.id, 'today', user))+1))
            if int(await self.conf.get_raw('counter', guild.id, 'today', user)) > int(await self.conf.get_raw('bans', guild.id, 'rules', 'daily')):
                if user not in await self.conf.get_raw('bans', guild.id, 'whitelist'):
                    await self.ctx.send(await self.get_random_string("ban_given")
                                       .format(await self.conf.get_raw('bans', guild.id,"rules","VACation")))
                    self.conf.set_raw('bans', guild.id,"ban",user,value="{}.{}.{} {}:{}".format(
                        now.day, now.month, now.year, 5, 0)
                else:
                    await self.ctx.send(self.get_random_string("ban_evaded"))
    # endregion
