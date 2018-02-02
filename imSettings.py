from .utils.dataIO import fileIO
import asyncio


async def add_filter(instance, ctx, filtertag: str, name):
    server = ctx.message.server
    if server.id not in instance.filters:
        instance.filters[server.id] = instance.filters["default"]
        fileIO("data/rolls/" + name + "_filters.json", "save", instance.filters)
        instance.filters = fileIO("data/rolls/" + name + "_filters.json", "load")
    if len(instance.filters[server.id]) < int(instance.settings["maxfilters"]):
        if filtertag not in instance.filters[server.id]:
            instance.filters[server.id].append(filtertag)
            fileIO("data/rolls/" + name + "_filters.json", "save", instance.filters)
            await instance.bot.say("Filter '{}' added to the server's " + name + " filter list.".format(filtertag))
        else:
            await instance.bot.say("Filter '{}' is already in the server's " + name + " filter list.".format(filtertag))
    else:
        await instance.bot.say(
            "This server has exceeded the maximum filters ({}/{}). https://www.youtube.com/watch?v=1MelZ7xaacs".format(
                len(instance.filters[server.id]), instance.settings["maxfilters"]))


async def del_filter(instance, ctx, filtertag: str, name):
    server = ctx.message.server
    if len(filtertag) > 0:
        if server.id not in instance.filters:
            instance.filters[server.id] = instance.filters["default"]
            fileIO("data/rolls/" + name + "_filters.json", "save", instance.filters)
            instance.filters = fileIO("data/rolls/" + name + "_filters.json", "load")
        if filtertag in instance.filters[server.id]:
            instance.filters[server.id].remove(filtertag)
            fileIO("data/rolls/" + name + "_filters.json", "save", instance.filters)
            await instance.bot.say("Filter '{}' deleted from the server's " + name + " filter list.".format(filtertag))
        else:
            await instance.bot.say("Filter '{}' does not exist in the server's " + name
                                   + " filter list.".format(filtertag))
    else:
        if server.id in instance.filters:
            del instance.filters[server.id]
            fileIO("data/rolls/" + name + "_filters.json", "save", instance.filters)
            await instance.bot.say("Reverted the server to the default " + name + " filter list.")
        else:
            await instance.bot.say("Server is already using the default " + name + " filter list.")
