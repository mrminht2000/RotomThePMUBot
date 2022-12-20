import json
import difflib

def get_pokemon_data(name):
	file = open('Data/Pokemons.json')
	pokemon_data = json.load(file)
	for pkm in pokemon_data:
		if (name.lower() == pkm["Name"].lower()):
			return pkm["RawInfo"]
	closest_value = difflib.get_close_matches(name, pokemon_data)
	if closest_value == []:
		return "Cannot find any pokemon's named " + name + "!"
	else:
		return closest_value