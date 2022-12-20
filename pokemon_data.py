import json
import difflib

def get_pokemon_data(name):
	file = open('Data/Pokemons.json')
	pokemon_data = json.load(file)
	for pkm in pokemon_data:
		if (name.lower() == pkm["Name"].lower()):
			res = "**"+ name + "**" + " can be found in:\n\n"
			try:
				res = res + "   " + "\n   ".join(pkm["RawInfo"])
			except:
				for i in pkm["RawInfo"]:
					for key, value in i.items():
						res = res + "   **" + str(key) + "**:\n     " + "\n    ".join(value) + '\n\n'

			if (pkm["Note"] is not None):
				res = res + "\n  ```css\n" + pkm["Note"] + "\n```"
			return res
	dct = {item["Name"]: item["RawInfo"] for item in pokemon_data}
	suggestions = difflib.get_close_matches(name, dct.keys())

	if suggestions == []:
		return "Cannot find any pokemon's named " + "**"+ name + "**" + "!"
	else:
		return "Do you mean " + ", ".join(map(lambda x: "*" + x + "*", suggestions)) + "?"