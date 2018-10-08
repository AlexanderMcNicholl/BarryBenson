Human = 1
Orc = 2
Dwarf = 3
Night_Elf = 4
Undead = 5
Tauren = 6
Gnome = 7
Troll = 8
Blood_Elf = 10
Draenei = 11

AC_KEYSTONE_MASTER = 11162
AC_KEYSTONE_CONQUEROR = 11185
AC_KEYSTONE_CHALLENGER = 11184
AC_ARENA_CHALLENGER = 2090
AC_ARENA_RIVAL = 2093
AC_ARENA_DUELIST = 2092
AC_ARENA_GLADIATOR = 2091
AC_AOTC_UD = 12536
AC_CE_UD = 12535
AC_HIGH_WARLORD = 5356
AC_CHAMPION = 5353
AC_FIRST_SERGEANT = 5349
AC_GRAND_MARSHALL = 5343
AC_LIEUTENANT_COMMANDER = 5339
AC_SERGEANT_MAJOR = 5334
AC_HIGH_WARLORD_NAME = 'High Warlord'
AC_CHAMPION_NAME = 'Champion'
AC_FIRST_SERGEANT_NAME = 'First Sergeant'
AC_GRAND_MARSHALL_NAME = 'Grand Marshall'
AC_LIEAUTENANT_COMMANDER_NAME = 'Lieutenant Commander'
AC_SERGEANT_MAJOR_NAME = 'Sergeant Major'
CLASS_WARRIOR = 1
CLASS_PALADIN = 2
CLASS_HUNTER = 3
CLASS_ROGUE = 4
CLASS_PRIEST = 5
CLASS_DEATH_KNIGHT = 6
CLASS_SHAMAN = 7
CLASS_MAGE = 8
CLASS_WARLOCK = 9
CLASS_MONK = 10
CLASS_DRUID = 11
CLASS_DEMON_HUNTER = 12
CLASS_WARRIOR_COLOUR = 0xC79C6E
CLASS_PALADIN_COLOUR = 0xF58CBA
CLASS_HUNTER_COLOUR = 0xABD473
CLASS_ROGUE_COLOUR = 0xFFF569
CLASS_PRIEST_COLOUR = 0xFFFFFF
CLASS_DEATH_KNIGHT_COLOUR = 0xC41F3B
CLASS_SHAMAN_COLOUR = 0x0070DE
CLASS_MAGE_COLOUR = 0x69CCF0
CLASS_WARLOCK_COLOUR = 0x9482C9
CLASS_MONK_COLOUR = 0x00FF96
CLASS_DRUID_COLOUR = 0xFF7D0A
CLASS_DEMON_HUNTER_COLOUR = 0xA330C9

def get_class_color(x):
	if x == CLASS_WARRIOR:
		return CLASS_WARRIOR_COLOUR
	elif x == CLASS_PALADIN:
		return CLASS_PALADIN_COLOUR
	elif x == CLASS_HUNTER:
		return CLASS_HUNTER_COLOUR
	elif x == CLASS_ROGUE:
		return CLASS_ROGUE_COLOUR
	elif x == CLASS_PRIEST:
		return CLASS_PRIEST_COLOUR
	elif x == CLASS_DEATH_KNIGHT:
		return CLASS_DEATH_KNIGHT_COLOUR
	elif x == CLASS_SHAMAN:
		return CLASS_SHAMAN_COLOUR
	elif x == CLASS_MAGE:
		return CLASS_MAGE_COLOUR
	elif x == CLASS_WARLOCK:
		return CLASS_WARLOCK_COLOUR
	elif x == CLASS_MONK:
		return CLASS_MONK_COLOUR
	elif x == CLASS_DRUID:
		return CLASS_DRUID_COLOUR
	elif x == CLASS_DEMON_HUNTER:
		return CLASS_DEMON_HUNTER_COLOUR
	else:
		return CLASS_WARRIOR_COLOUR

def get_race(x):
	if x == Human:
		return "Human"
	elif x == Orc:
		return "Orc"
	elif x == Dwarf:
		return "Dwarf"
	elif x == Tauren:
		return "Tauren"
	elif x == Night_Elf:
		return "Night Elf"
	elif x == Undead:
		return "Undead"
	elif x == Tauren:
		return "Tauren"
	elif x == Gnome:
		return "Gnome"
	elif x == Troll:
		return "Troll"
	elif x == Blood_Elf:
		return "Bloodelf"
	elif x == Draenei:
		return "Draenei"
	else:
		return "Unknown Race"

def get_class(x):
	if x == CLASS_WARRIOR:
		return "Warrior"
	elif x == CLASS_PALADIN:
		return "Paladin"
	elif x == CLASS_HUNTER:
		return "Hunter"
	elif x == CLASS_ROGUE:
		return "Rogue"
	elif x == CLASS_PRIEST:
		return "Priest"
	elif x == CLASS_DEATH_KNIGHT:
		return "Death Knight"
	elif x == CLASS_SHAMAN:
		return "Shaman"
	elif x == CLASS_MAGE:
		return "Mage"
	elif x == CLASS_WARLOCK:
		return "Warlock"
	elif x == CLASS_MONK:
		return "Monk"
	elif x == CLASS_DRUID:
		return "Druid"
	elif x == CLASS_DEMON_HUNTER:
		return "Demon Hunter"
	else:
		return "Unknown Class"

