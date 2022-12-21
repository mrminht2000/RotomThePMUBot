import json
import difflib

def get_pmu_pokemon_data(name):
	file = open('Data/PokemonData/Pokemons.json')
	pokemon_data = json.load(file)
	for pkm in pokemon_data:
		if (name.lower() == pkm["Name"].lower()):
			res = "**"+ pkm["Name"] + "**" + " can be found in:\n\n"
			try:
				res = res + "   " + "\n   ".join(pkm["RawInfo"])
			except:
				for i in pkm["RawInfo"]:
					for key, value in i.items():
						res = res + "   **" + str(key) + "**:\n    " + "\n    ".join(value) + '\n\n'

			if (pkm["Note"] is not None):
				res = res + "\n  ```css\n" + pkm["Note"] + "\n```"
			return res
	dct = {item["Name"]: item["RawInfo"] for item in pokemon_data}
	suggestions = difflib.get_close_matches(name, dct.keys())

	if suggestions == []:
		return "Cannot find any pokemon's named " + "**"+ name + "**" + "!"
	else:
		return "Do you mean " + ", ".join(map(lambda x: "*" + x + "*", suggestions)) + "?"

def get_recruitable_data(name):
	file = open('Data/PokemonData/Recruitable.json')
	recruitable_data = json.load(file)
	for pkm in recruitable_data:
		if (name.lower() == pkm["Name"].lower()):
			res = "**"+ name + "**" + " can be found in:\n"
			for location in pkm["Locations"]:
				res = res + "   " + location["Dungeon"] + " (" + location["Floor"] + "), (" + location["Time"] + "), *Recruite rate: " + str(location["RecruitRate"]) +"%*. \n"
			return res
	dct = {item["Name"]: item["Locations"] for item in recruitable_data}
	suggestions = difflib.get_close_matches(name, dct.keys())

	if suggestions == []:
		return "Cannot find any recruitable pokemon's named " + "**"+ name + "**" + "!"
	else:
		return "Do you mean " + ", ".join(map(lambda x: "*" + x + "*", suggestions)) + "?"

def get_ability_data(name):
	file = open('Data/PokemonData/Abilities.json')
	ability_data = json.load(file)
	for ability in ability_data:
		if (name.lower() == ability["Name"].lower()):
			return 1, ability
	return 0, "This ability has't been described in PMU game yet."