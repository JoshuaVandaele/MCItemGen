from random import randint
import re

def getUUID():
	UUID = [
		randint(-999999999,999999999),
		randint(-999999999,999999999),
		randint(-999999999,999999999),
		randint(-999999999,999999999),
	]
	UUID.sort(reverse=True)
	return str(UUID).replace("[","[I;")

tags = {
	"EntityTag":{
		"CustomName":[], #json text
		"CustomNameVisible":False,
		"Glowing":False,
		"Invulnerable":False,
		"NoGravity":False,
		"OnGround":False,
		"Silent":False,
	},

	"potions":{
		"CustomPotionEffects":[], #todo
		"CustomPotionColor":0,
		"Potion":"Potion name",
	},


	"blockentities":{
		"BlockEntityTag":{}, #Not going into this rabbit hole
		"BlockStateTag":{},
		"CanPlaceOn":[], #namespaced IDs
	},

	"crossbows":{
		"ChargedProjectiles":[], # tipped arrow in this format: {id: "tipped_arrow", Count: 64b, tag: {}},
		"Charged":False
	},
	
	"books":{
		"pages":[] #Json text
	},

	"writtenbooks":{
		"title":"Title",
		"author":"Folfy_Blue",
		"generation":0, #0 = original, 1 = copy, 2 = copy of a copy, 3 = tattered
		"resolved":False, #Has been opened before or not
	},
	
	"playerheads":{
		"SkullOwner":{
			"UUID":getUUID(),
			"Name":"Folfy_Blue",
			"Properties": {
				"textures":[
					{
					"Value":"", #Base64 JSON object, too complicated for me to go down the rabbit hole rn
					"Signature":"Folfy_Blue"
					}
				]
			}
		}
	},

	"fireworks":{
		"Fireworks":{
			"Explosions":[
				{
					"Colors":[],
					"FadeColors":[],
					"Flicker":False,
					"Trail":False,
					"Type":0, #0 = Small Ball, 1 = Large Ball, 2 = Star-shaped, 3 = Creeper-shaped, 4 = Burst.
				}
			]
		},
		"Flight":1, #Flight duration from -128 to 127
	},

	"fireworkstars":{
		"Explosion":{
			"Colors":[],
			"FadeColors":[],
			"Flicker":False,
			"Trail":False,
			"Type":0, #0 = Small Ball, 1 = Large Ball, 2 = Star-shaped, 3 = Creeper-shaped, 4 = Burst.
		},
	},

	"maps":{
		"map":0, #map numb
		"map_scale_direction":1, #Not documented
		"Decorations":[
			{
				"id":"", #unique string to identify the decoration
				"type":0, #0-26 for all decorations
				"x":0,
				"z":0,
				"rot":0 #rotation
			}
		],
	},

	"susstews":{
		"Effects": [
			{"EffectId":23,"EffectDuration":1000000} #lets go
		]
	},

	"compass":{
		"LodestoneTracked":False,
		"LodestoneDimension":"overworld",
		"LodestonePos":{
			"x":0,
			"y":0,
			"z":0,
		}
	}
}

cmd = {
	"target":"@p",
	"item":"stone",
	"targetSelectors": {
		"distance":False,
		#Closest to coords x,y,z or distance from x,y,z
		"x":False,
		"y":False,
		"z":False,
		#Volume in box selection
		"dx":False,
		"dy":False,
		"dz":False,

		"scores":{}, #{objective1=value1, ...}
		"team":False, #Only give to players of team X # ! is valid

		#How many people will get the item, and which people
		"limit":False,
		"sort":False, #nearest, furthest, random, arbitrary

		"level":False,
		"gamemode":False, # ! is valid

		"x_rotation":False,
		"y_rotation":False,

		#If player has given nbt or nbt tag...
		"tag":"",
		"nbt":"{}",

		"advancements":{}, #{namespaced ID = bool}
		"predicate":False
	},
	"nbt": {
		"display":{
			"Lore":[], #["",{"text":"test","bold":false,"italic":false,"strikethrough":false,"underlined":false,"obfuscated":false,"color":"black"}]
			"Name":"", #{"text":"test","bold":false,"italic":false,"strikethrough":false,"underlined":false,"obfuscated":false,"color":"black"}
		},
		"AttributeModifiers":[], #addAttrModif()
		"Enchantments":[], #addEnch()
		
		"Damage":0,
		"Unbreakable":0,
		"RepairCost":0,
		
		"CanDestroy":[], #namespaced IDs

		"HideFlags":0
	}
}

AttributeModifiers = {
	1:"generic.armor",
	2:"generic.armor_thoughness",
	3:"generic.attack_damage",
	4:"generic.attack_speed",
	5:"generic.attack_knockback",
	6:"generic.max_health",
	7:"generic.knockback_resistance",
	8:"generic.movement_speed",
	9:"generic.jump_strength",
	10:"generic.luck",
	11:"generic.follow_range",
	12:"generic.flying_speed",
	13:"generic.spawn_reinforcements"
}

slots = {
	0:False,
	1:"mainhand",
	2:"offhand",
	3:"feet",
	4:"legs",
	5:"chest",
	6:"head"
}

Enchantments = {
	1:"aqua_affinity",
	2:"bane_of_arthropods",
	3:"binding_curse",
	4:"blast_protection",
	5:"channeling",
	6:"depth_strider",
	7:"efficiency",
	8:"feather_falling",
	9:"fire_aspect",
	10:"fire_protection",
	11:"flame",
	12:"fortune",
	13:"frost_walker",
	14:"impaling",
	15:"infinity",
	16:"knockback",
	17:"looting",
	18:"loyalty",
	19:"luck_of_the_sea",
	20:"lure",
	21:"mending",
	22:"multishot",
	23:"piercing",
	24:"power",
	25:"projectile_protection",
	26:"protection",
	27:"punch",
	28:"quick_charge",
	29:"respiration",
	30:"riptide",
	31:"sharpness",
	32:"silk_touch",
	33:"smite",
	34:"soul_speed",
	35:"sweeping",
	36:"thorns",
	37:"unbreaking",
	38:"vanishing_curse",
}

subItemTypes = {
	"Potions":
	[
		"potion",
		"splash_potion",
		"lingering_potion",
		"tipped_arrow"
	],
	"Block_Entities":[],
	"Crossbows": ["crossbow"]
}

blockentities = {
		"Beehives":["beehive","bee_nest"],
		"Signs":["oak_sign","spruce_sign","birch_sign","jungle_sign","acacia_sign","dark_oak_sign","crimson_sign","warped_sign"],
		"Banners":["white_banner","orange_banner","magenta_banner","light_blue_banner","yellow_banner","lime_banner","pink_banner","gray_banner","light_gray_banner","cyan_banner","purple_banner","blue_banner","brown_banner","green_banner","red_banner","black_banner"],
		"Containers":["chest","trapped_chest","dispenser","furnace","brewing_stand","hopper","dropper","barrel","smoker","blast_furnace","campfire","soul_campfire","lectern","white_shulker_box","orange_shulker_box","magenta_shulker_box","light_blue_shulker_box","yellow_shulker_box","lime_shulker_box","pink_shulker_box","gray_shulker_box","light_gray_shulker_box","cyan_shulker_box","purple_shulker_box","blue_shulker_box","brown_shulker_box","green_shulker_box","red_shulker_box","black_shulker_box"],
		"Beacon":["beacon"],
		"Spawner":["mob_spawner"],
		"Command_Blocks":["command_block","chain_command_block","repeating_command_block"],
}

for blockList in blockentities.values():
	subItemTypes["Block_Entities"] += blockList


def remValFromDict(dict,val):
	newDict = {}
	for key,value in dict.items():
		if value != val:
			newDict[key] = value
	return newDict

def remValsFromDict(dict,vals):
	newDict = dict
	for val in vals:
		newDict = remValFromDict(newDict,val)
	return newDict

def askYN(str):
	print(str + " [Y/N]")
	return input()[0:1].upper() == "Y"

def Block_Entities():
	print("Block entities aren't supported yet.")
	pass

def Crossbows():
	cmd["nbt"] |= tags["crossbows"]

	def addArrow():
		arrow = {}
		arrow["id"] = "minecraft:tipped_arrow"
		arrow["Count"] = 127
		arrow["tag"] = "REMOVEPREV"+input("Paste the raw NBT of the (tipped) arrow.").replace("\\","BACKSLASH")+"REMOVENEXT"

		cmd["nbt"]["ChargedProjectiles"].append(arrow)

	while askYN("Add an arrow loaded in the bow?"):
		addArrow()
		cmd["nbt"]["Charged"] = True

def Potions():
	cmd["nbt"] |= tags["potions"]

	def addPot():
		effect = {}
		effect["Id"] = int(input("What is the potion ID?\n"))
		effect["Amplifier"] = int(input("What Amplifier?\n"))
		effect["Duration"] = int(input("What is the Duration?\n"))
		effect["Ambient"] = askYN("Ambient effect?")
		effect["ShowParticles"] = askYN("Show Particles?")
		effect["ShowIcon"] = askYN("Show Icon?")

		for i in range(0,int(input("How many times do you want this effect to be on the potion?\n"))):
			cmd["nbt"]["CustomPotionEffects"].append(effect)

	while askYN("Add a potion effect?"):
		addPot()
	print("Potion color in format Red<<16 + Green<<8 + Blue")
	cmd["nbt"]["CustomPotionColor"] = int(input())

def addAttrModif():
	attrib = {
		"UUID": getUUID()
	}

	print("What is the attribute you want to use?")

	for i,name in AttributeModifiers.items(): #Display a list of attributes
		print(str(i)+" - "+name)
	modif = int(input())

	attrib["AttributeName"] = "minecraft:"+AttributeModifiers[modif]
	attrib["Name"] = AttributeModifiers[modif]

	print("What will be the amount of this modifier?")
	attrib["Amount"] = int(input())

	print("Do you want it to be:\n0 - Additive\n1 - Multiplicative of the base value\n2 - Multiplicative of the total value")
	attrib["Operation"] = int(input())

	print("Which slot do you want it to work in? (0 for all)")

	for i,name in slots.items(): #Display a list of attributes
		print(str(i)+" - "+str(name))
	slot = int(input())
	attrib["Slot"] = str(slots[slot])

	for i in range(0,int(input("How many times do you want this attribute to be on the item?\n"))):
		cmd["nbt"]["AttributeModifiers"].append(attrib)

def addEnch():
	enchant = {}

	print("What is the enchant you want to add?")
	for i,name in Enchantments.items(): #Display a list of enchants
		print(str(i)+" - "+name)
	enchant["id"] = Enchantments[int(input())]

	print("Which level do you want it to have?")
	enchant["lvl"] = int(input())


	for i in range(0,int(input("How many times do you want this enchant to be on the item?\n"))):
		cmd["nbt"]["Enchantments"].append(enchant)

def swap(str,a,b):
	str = str.replace(b,"$")
	str = str.replace(a,b)
	str = str.replace("$",a)
	return str

def makeJsonText():
	line = []
	done = False
	while not done: #["",{"text":"test","bold":false,"italic":false,"strikethrough":false,"underlined":false,"obfuscated":false,"color":"black"}]
		text = {}
		print("What text do you want to add onto this line?")
		text["text"] = input()
		text["color"] = input("What color do you want this to be?\n")
		text["bold"] = askYN("Is it bold?")
		text["italic"] = askYN("Is it italic?")
		text["strikethrough"] = askYN("Is it strikethrough?")
		text["underlined"] = askYN("Is it underlined?")
		text["obfuscated"] = askYN("Is it obfuscated?")

		line.append(remValFromDict(text,False))
		done = not askYN("Do you still want to edit this line?")
	line = swap(str(line),'"',"'")
	return line



print("Welcome to Folfy_Blue's item creator!\n")
print("Let's start with the name. What do you want this item to be named?")
cmd["nbt"]["display"]["Name"] = makeJsonText()
print("\nAnd following with the lore!")

while askYN("Do you want to add a line to the lore?"):
	cmd["nbt"]["display"]["Lore"].append(makeJsonText())

print("\nTo enchants now.")
while askYN("Do you want to add an enchant?"):
	addEnch()

print("\nTo attributes now!")
while askYN("Do you want to add an attribute?"):
	addAttrModif()

print("Type the namespaced ID of the item.")
cmd["item"] = input().lower().replace("","")

for subType,itemDict in subItemTypes.items():
	if cmd["item"] in itemDict:
		locals()[subType]()
		break

final = {
	"wurst": ".give ",
	"vanilla": "/give "
}

targetSelectors = ""
for k,v in remValsFromDict(cmd["targetSelectors"],[False,{}]).items():
	targetSelectors+= k +"="+str(v)+","

nbt = str(cmd["nbt"])
nbt = re.sub(".REMOVEPREV","",nbt)
nbt = re.sub("REMOVENEXT.","",nbt)
nbt = nbt.replace("\\","")
nbt = nbt.replace("BACKSLASH","\\")


final["vanilla"] = "/give " + cmd["target"]+"["+targetSelectors+"]"+" "+cmd["item"]+nbt
final["wurst"] = ".give "+cmd["item"]+" 1 "+nbt

print()
print("GIVE COMMANDS")
print("="*20)
print("Vanilla:")
print(final["vanilla"])
print()
print("="*20)
print("Wurst:")
print(final["wurst"])



"""
//Done
	General
	Potions
	Crossbows

//Todo
Block entities
Books
Written Books
Player heads
Fireworks
Firework stars
Maps
Sus Stews
Compass

"""