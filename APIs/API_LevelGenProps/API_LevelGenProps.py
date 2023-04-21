import Shrines as Shrines
import Consumables as Consumables
import random

#
# add shrine type
#

SHRINE_COMMON = Shrines.COMMON
SHRINE_UNCOMMON = Shrines.UNCOMMON
SHRINE_RARE = Shrines.RARE

def add_shrine(shrine, rarity = SHRINE_COMMON):
	Shrines.new_shrines.append((shrine, rarity))


#
# Add new kinds of primary/secondary props that can generate
#

RUBY_HEART_WEIGHT = 0.3
SPELL_CIRCLE_WEIGHT = 0.4
SHRINE_WEIGHT = 0.3

primary_props = [
	(Shrines.hp_shrine, RUBY_HEART_WEIGHT, lambda level: True),
	(Shrines.library, SPELL_CIRCLE_WEIGHT, lambda level: True),
	(Shrines.shrine, SHRINE_WEIGHT, lambda level: level > 2)
]
def add_primary_prop_type(prop_generator, weight, condition=lambda level: True):
	primary_props.append((prop_generator, weight, condition))

secondary_props = []
def add_secondary_prop_type(prop_generator, weight, condition=lambda level: True):
	secondary_props.append((prop_generator, weight, condition))


#
# Define chances for how many secondary props are generated in a level (eg, "I want there to be a 50% chance for a level to generate 3 secondary props past level 5": add_num_secondary_props_random_option(3, .5, lambda level: level > 5))
#

# NO_EXTRA_PROPS_WEIGHT = .5
random_num_extra_props = [
	# (0, NO_EXTRA_PROPS_WEIGHT, lambda level: True)
]
def add_num_secondary_props_random_option(num, weight, condition = lambda level: True):
	random_num_extra_props.append((num, weight, condition))



#
# Items
#

# item_generator function takes no params, returns Item object
# eg:
# def heal_potion():
# 	item = Item()
# 	item.name = "Healing Potion"
# 	item.description = "Drinking this potion restores the drinker to full health"
# 	item.set_spell(HealPotSpell())
# 	return item
def add_item_type(item_generator, weight):
	Consumables.all_consumables.append((item_generator, weight))

ITEM_COMMON =  Consumables.COMMON
ITEM_UNCOMMON = Consumables.UNCOMMON
ITEM_RARE = Consumables.RARE
ITEM_SUPER_RARE = Consumables.SUPER_RARE

#
# Level generation
#

def pre_populate_level(levelgenerator, prng = None):
	if not len(random_num_extra_props):
		return
	level = levelgenerator.difficulty

	levelgenerator.extra_props = []
	if not prng:
		prng = random

	opts = [(num, weight) for (num, weight, condition) in random_num_extra_props if condition(level)]
	if not len(opts):
		return

	num = prng.choices([o[0] for o in opts], weights=[o[1] for o in opts])[0]

	for i in range(num):
		opts = [(generator, weight) for (generator, weight, condition) in secondary_props if condition(level)]
		extra_prop = prng.choices([o[0] for o in opts], weights=[o[1] for o in opts])[0]
		levelgenerator.extra_props.append(extra_prop)
	

def place_extra_props(levelgenerator):
	if hasattr(levelgenerator, "extra_props"):
		for prop in levelgenerator.extra_props:
			p = levelgenerator.empty_spawn_points.pop()
			levelgenerator.level.add_prop(prop, p.x, p.y)



#
# Overrides
#		
	
# enable generation of new primary prop types
def roll_shrine(level, prng=None):
	opts = [(generator, weight) for (generator, weight, condition) in primary_props if condition(level)]

	if not prng:
		prng = random

	return prng.choices([o[0] for o in opts], weights=[o[1] for o in opts])[0]


# https://discord.com/channels/645130221435092992/906059860024623124/945412545030799370
# def make_shrine(shrine, player):


	
# def make_shrine(shrine, player):
# 	shrine_prop = ShrineShop(lambda : list(shrine.get_buffs(player)))
# 	shrine_prop.name = "%s Shrine" % shrine.name
# 	shrine_prop.description = shrine.get_description()

# 	# Use custom asset if exists
# 	maybe_asset = ['tiles', 'shrine', shrine.name.lower().replace(' ', '_')]
# 	if os.path.exists(os.path.join('rl_data', *maybe_asset) + '.png'):
# 		shrine_prop.asset = maybe_asset

# 	maybe_asset = ['tiles', 'shrine', 'animated', shrine.name.lower().replace(' ', '_')]
# 	if os.path.exists(os.path.join('rl_data', *maybe_asset) + '.png'):
# 		shrine_prop.asset = maybe_asset

# 	return shrine_prop


# TODO: override
	# Level.Item.
	# def get_asset(self):
	# 	asset = ['tiles', 'items', 'animated', self.name.lower().replace(' ', '_')]
	# 	# use generic trinket asset if specific asset is not present
	# 	if not os.path.exists(os.path.join('rl_data', *asset) + '.png'):
	# 		asset = ['tiles', 'items', 'animated', 'trinket']
		
	# 	return asset

