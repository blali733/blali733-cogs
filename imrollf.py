import discord
from discord.ext import commands
from .utils.dataIO import fileIO
from urllib import parse
import os
import aiohttp
import asyncio
import random

class ImRollPE:
	def __init__(self, bot):
		self.bot = bot
		self.loliFilters = fileIO("data/loli/filters.json", "load")
		self.loliSettings = fileIO("data/loli/settings.json", "load")
		self.danFilters = fileIO("data/dan/filters.json","load")
		self.danSettings = fileIO("data/dan/settings.json","load")
		self.gelFilters = fileIO("data/gel/filters.json", "load")
		self.gelSettings = fileIO("data/gel/settings.json", "load")
		self.konaFilters = fileIO("data/kona/filters.json","load")
		self.konaSettings = fileIO("data/kona/settings.json","load")

	@commands.command(pass_context=True,no_pm=True)
	async def imrollf(self, ctx, *text):
		server = ctx.message.server
		channel = ctx.message.channel
		self.loliFilters = fileIO("data/loli/filters.json", "load")
		self.loliSettings = fileIO("data/loli/settings.json", "load")
		self.danFilters = fileIO("data/dan/filters.json","load")
		self.danSettings = fileIO("data/dan/settings.json","load")
		self.gelFilters = fileIO("data/gel/filters.json", "load")
		self.gelSettings = fileIO("data/gel/settings.json", "load")
		self.konaFilters = fileIO("data/kona/filters.json","load")
		self.konaSettings = fileIO("data/kona/settings.json","load")

		await asyncio.gather(
			lolibooru_get(self, ctx, server, channel),
			danbooru_get(self, ctx, server, channel),
			gelbooru_get(self, ctx, server, channel),
			konachan_get(self, ctx, server, channel),
		)
		
async def lolibooru_get(self, ctx, server, channel):
	loliEmbedLink   = ""
	loliEmbedTitle  = ""
	loliImageId     = ""
	loliOutput      = None
	loliRating      = ""
	loliRatingColor = "FFFFFF"
	loliRatingWord  = "unknown"
	loliSearch  = "https://lolibooru.moe/post/index.json?limit=1&tags="
	loliTagSearch   = ""
	
	# Assign tags to URL
	if server.id in self.loliFilters:
		loliTagSearch += " ".join(self.loliFilters[server.id])
	else:
		loliTagSearch += " ".join(self.loliFilters["default"])

	# Randomize results
	loliTagSearch += " order:random"
	loliSearch += parse.quote_plus(loliTagSearch)
	
	lolim1 = await self.bot.send_message(channel, "Fetching loli image...")
	lolim2 = await self.bot.send_message(channel, "loli preview ^^")

	# Fetch and display the image or an error
	try:
		async with aiohttp.get(loliSearch) as r:
			lolibooru = await r.json()
		if lolibooru != []:
			# Sets the image URL
			imageURL = lolibooru[0].get("file_url").replace(' ', '+')

			# Fetches the image ID
			loliImageId = lolibooru[0].get('id')

			# Sets the embed title
			loliEmbedTitle = "Lolibooru Image #{}".format(loliImageId)

			# Sets the URL to be linked
			loliEmbedLink = "https://lolibooru.moe/post/show/{}".format(loliImageId)

			# Check for the loliRating and set an appropriate color
			loliRating = lolibooru[0].get('rating')
			if loliRating == "s":
				loliRatingColor = "00FF00"
				loliRatingWord = "safe"
			elif loliRating == "q":
				loliRatingColor = "FF9900"
				loliRatingWord = "questionable"
			elif loliRating == "e":
				loliRatingColor = "FF0000"
				loliRatingWord = "explicit"

			# Initialize verbose embed
			loliOutput = discord.Embed(title=loliEmbedTitle, url=loliEmbedLink, colour=discord.Colour(value=int(loliRatingColor, 16)))

			# Edits the pending lolim1 with the results
			await self.bot.edit_message(lolim1, "Image found.", embed=loliOutput)
			return await self.bot.edit_message(lolim2, imageURL)
		else:
			return await self.bot.edit_message(lolim1, "Your search terms gave no results.")
	except:
		return await self.bot.edit_message(lolim1, "Connection timed out.")

async def danbooru_get(self, ctx, server, channel):
	#Danbooru
	danEmbedLink   = ""
	danEmbedTitle  = ""
	danImageId     = ""
	danOutput      = None
	danRating      = ""
	danRatingColor = "FFFFFF"
	danRatingWord  = "unknown"
	danSearch  = "http://danbooru.donmai.us/posts.json?tags="
	danTagSearch   = ""
	
		# Assign tags to URL
	if server.id in self.danFilters:
		danTagSearch += " ".join(self.danFilters[server.id])
	else:
		danTagSearch += " ".join(self.danFilters["default"])
	danSearch += parse.quote_plus(danTagSearch)

	# Randomize results
	danSearch += "&random=y"
	
	danm1 = await self.bot.send_message(channel, "Fetching dan image...")
	danm2 = await self.bot.send_message(channel, "dan preview")
	
	# Fetch and display the image or an error
	try:
		async with aiohttp.get(danSearch) as d:
			danbooru = await d.json()
		if danbooru != []:
			if "success" not in danbooru:
				fuse = 0
				for index in range(len(danbooru)): # Goes through each result until it finds one that works
					if "file_url" in danbooru[index]:
						# Sets the image URL
						danImageURL = "https://danbooru.donmai.us{}".format(danbooru[index].get('file_url'))
						# Fetches the image ID
						danImageId = danbooru[index].get('id')

						# Sets the embed title
						danEmbedTitle = "Danbooru Image #{}".format(danImageId)

						# Sets the URL to be linked
						danEmbedLink = "https://danbooru.donmai.us/posts/{}".format(danImageId)
						
						# Checks for the rating and sets an appropriate color
						danRating = danbooru[index].get('rating')
						if danRating == "s":
							danRatingColor = "00FF00"
							danRatingWord = "safe"
						elif danRating == "q":
							danRatingColor = "FF9900"
							danRatingWord = "questionable"
						elif danRating == "e":
							danRatingColor = "FF0000"
							danRatingWord = "explicit"

						# Initialize verbose embed
						danOutput = discord.Embed(title=danEmbedTitle, url=danEmbedLink, colour=discord.Colour(value=int(danRatingColor, 16)))

						# Edits the pending message with the results
						await self.bot.edit_message(danm1, "Image found.", embed=danOutput)
						await self.bot.edit_message(danm2, danImageURL)
						fuse = 1
						break
				if fuse == 0:
					await self.bot.edit_message(danm1, "Cannot find an image that can be viewed by you.")
			else:
				# Edits the pending message with an error received by the server
				await self.bot.edit_message(danm1, "{}".format(danbooru["message"]))
		else:
			await self.bot.edit_message(danm1, "Your search terms gave no results.")
	except:
		await self.bot.edit_message(danm1, "Connection timed out.")
		
async def gelbooru_get(self, ctx, server, channel):
	gelEmbedLink   = ""
	gelEmbedTitle  = ""
	gelImageId     = ""
	gelOutput      = None
	gelRating      = ""
	gelRatingColor = "FFFFFF"
	gelRatingWord  = "unknown"
	gelSearch  = "http://gelbooru.com/index.php?page=dapi&s=post&limit=1&q=index&tags="
	gelTagSearch   = ""
	# Apply tags to URL
	if server.id in self.gelFilters:
		gelTagSearch += " ".join(self.gelFilters[server.id])
	else:
		gelTagSearch += " ".join(self.gelFilters["default"])
	gelSearch += parse.quote_plus(gelTagSearch)
	
	gelm1 = await self.bot.send_message(channel, "Fetching gel image...")
	gelm2 = await self.bot.send_message(channel, "gel preview")
	
	# Fetch and display the image or an error
	try:
		# Fetch the xml page to randomize the results
		async with aiohttp.get(gelSearch) as r:
			website = await r.text()

		# Gets the amount of results
		countStart = website.find("count=\"")
		countEnd = website.find("\"", countStart+7)
		count = website[countStart+7:countEnd]

		# Picks a random page and sets the search URL to json
		pid = str(random.randint(0, int(count)))
		gelSearch += "&json=1&pid={}".format(pid)
		# Fetches the json page
		async with aiohttp.get(gelSearch) as r:
			website = await r.json()
		if website:
			# Sets the image URL
			gelImageURL = "{}".format(website[0]['file_url'])
			# Fetches the image ID
			gelImageId = website[0].get('id')

			# Sets the embed title
			gelEmbedTitle = "Gelbooru Image #{}".format(gelImageId)

			# Sets the URL to be linked
			gelEmbedLink = "https://gelbooru.com/index.php?page=post&s=view&id={}".format(gelImageId)

			# Check for the rating and set an appropriate color
			gelRating = website[0].get('rating')
			if gelRating == "s":
				gelRatingColor = "00FF00"
				gelRatingWord = "safe"
			elif gelRating == "q":
				gelRatingColor = "FF9900"
				gelRatingWord = "questionable"
			elif gelRating == "e":
				gelRatingColor = "FF0000"
				gelRatingWord = "explicit"

			# Initialize verbose embed
			gelOutput = discord.Embed(title=gelEmbedTitle, url=gelEmbedLink, colour=discord.Colour(value=int(gelRatingColor, 16)))

			# Edits the pending message with the results
			await self.bot.edit_message(gelm1, "Image details", embed=gelOutput)
			await self.bot.edit_message(gelm2, gelImageURL)
		else:
			await self.bot.edit_message(gelm1, "Your search terms gave no results.")
	except:
		await self.bot.edit_message(gelm1, "Connection timed out.")

async def konachan_get(self, ctx, server, channel):
	konaEmbedLink   = ""
	konaEmbedTitle  = ""
	konaImageId     = ""
	konaOutput      = None
	konaRating      = ""
	konaRatingColor = "FFFFFF"
	konaRatingWord  = "unknown"
	konaSearch  = "https://konachan.com/post.json?limit=1&tags="
	konaTagSearch   = ""
	# Apply tags to URL
	if server.id in self.konaFilters:
		konaTagSearch += " ".join(self.konaFilters[server.id])
	else:
		konaTagSearch += " ".join(self.konaFilters["default"])

	# Randomize results
	konaTagSearch += " order:random"
	konaSearch += parse.quote_plus(konaTagSearch)
	
	konam1 = await self.bot.send_message(channel, "Fetching kona image...")
	konam2 = await self.bot.send_message(channel, "Kona(ta) preview")
	
	# Fetch and display the image or an error
	try:
		async with aiohttp.get(konaSearch) as r:
			website = await r.json()
		if website != []:
			# Sets the image URL
			konaImageURL = "https:{}".format(website[0].get("file_url")).replace(' ', '+')
			# Fetches the image ID
			konaImageId = website[0].get('id')

			# Sets the embed title
			konaEmbedTitle = "Konachan Image #{}".format(konaImageId)

			# Sets the URL to be linked
			konaEmbedLink = "https://konachan.com/post/show/{}".format(konaImageId)
			
			# Checks for the rating and set an appropriate color
			konaRating = website[0].get('rating')
			if konaRating == "s":
				konaRatingColor = "00FF00"
				konaRatingWord = "safe"
			elif konaRating == "q":
				konaRatingColor = "FF9900"
				konaRatingWord = "questionable"
			elif konaRating == "e":
				konaRatingColor = "FF0000"
				konaRatingWord = "explicit"

			# Initialize verbose embed
			konaOutput = discord.Embed(title=konaEmbedTitle, url=konaEmbedLink, colour=discord.Colour(value=int(konaRatingColor, 16)))

			# Edits the pending message with the results
			await self.bot.edit_message(konam1, "Image found.", embed=konaOutput)
			await self.bot.edit_message(konam2, konaImageURL)
		else:
			await self.bot.edit_message(konam1, "Your search terms gave no results.")
	except:
		await self.bot.edit_message(konam2, "connection timed out.")

def check_folder():
	if not os.path.exists("data/loli"):
		print ("Creating data/loli folder...")
		os.makedirs("data/loli")
	if not os.path.exists("data/dan"):
		print ("Creating data/dan folder...")
		os.makedirs("data/dan")
	if not os.path.exists("data/gel"):
		print("Creating data/gel folder...")
		os.makedirs("data/gel")
	if not os.path.exists("data/kona"):
		print ("Creating data/kona folder...")
		os.makedirs("data/kona")

def check_files():
	loliFilters = {"default":["rating:safe"]}
	loliSettings = {"maxfilters":"50"}
	danFilters = {"default":["rating:safe"]}
	danSettings = {"username":"", "api_key":"", "maxfilters":"10"}
	gelFilters = {"default":["rating:safe"]}
	gelSettings = {"maxfilters":"50"}
	konaFilters = {"default":["rating:safe"]}
	konaSettings = {"username":"", "api_key":"", "maxfilters":"10"}

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
		print ("Creating default dan filters.json...")
		fileIO("data/dan/filters.json", "save", danFilters)
	else:
		danFilterlist = fileIO("data/dan/filters.json", "load")
		if "default" not in danFilterlist:
			danFilterlist["default"] = danFilters["default"]
			print ("Adding default dan filters...")
			fileIO("data/dan/filters.json", "save", danFilterlist)
	if not fileIO("data/dan/settings.json", "check"):
		print ("Creating default dan settings.json...")
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
		print ("Creating default kona filters.json...")
		fileIO("data/kona/filters.json", "save", konaFilters)
	else:
		konaFilterlist = fileIO("data/kona/filters.json", "load")
		if "default" not in konaFilterlist:
			konaFilterlist["default"] = konaFilters["default"]
			print ("Adding default kona filters...")
			fileIO("data/kona/filters.json", "save", konaFilterlist)
	if not fileIO("data/kona/settings.json", "check"):
		print ("Creating default kona settings.json...")
		fileIO("data/kona/settings.json", "save", konaSettings)

def setup(bot):
	check_folder()
	check_files()
	bot.add_cog(ImRollPE(bot))
