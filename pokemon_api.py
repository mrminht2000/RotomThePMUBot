import os
import requests
import json
import difflib
from pokemon_data import get_ability_data

BASE_API = 'https://pokeapi.co/api/v2/'
POKEMON_API = 'pokemon/'
ABILITY_API = 'ability/'
pokemon_file = open('Data/PokemonData/Pokemons.json')
pokemon_data = json.load(pokemon_file)
file = open('Data/PokemonData/Pokemons.json')
pokemon_data = json.load(file)

def pokemon(name):
    res = requests.get(BASE_API + POKEMON_API + "-".join(name.lower().strip().split()))

    if res.status_code == 404:
        dct = {item["Name"]: item["RawInfo"] for item in pokemon_data}
        suggestions = difflib.get_close_matches(name, dct.keys())

        if suggestions == []:
            return "Cannot find any pokemon's named " + "**"+ name + "**" + "!"
        else:
            return "Do you mean " + ", ".join(map(lambda x: "*" + x + "*", suggestions)) + "?"
    else:
        resp = "Information about **" + name.capitalize() + "**: \n\n"
        # Types
        pkm_type = [ptype['name'] for ptype in [item['type'] for item in res.json()['types']]]
        resp += "__Type:__  " + "  -  ".join(map(lambda x: "**" + x.capitalize() + "**", pkm_type)) + "\n"

        # Abilities
        pkm_abi = [abi['name'] for abi in [item['ability'] for item in res.json()['abilities']]]
        resp += '__Abilities:__\n'
        for abi in pkm_abi:
            status, abi_req = ability(name=abi)
            status, abi_pmu = get_ability_data(abi)
            resp += "  " + " ".join(map(lambda x: "**" + x.capitalize() + "**",abi.split('-'))) + ": " + abi_req['short_effect'] + '\n'
            resp += "  *PMU*: " + (abi_pmu["ShortDescription"].replace("Ã©", "é") if status == 1 else abi_pmu) + '\n' 
        
        # Base Experience
        resp += '__Base experience:__ ' + str(res.json()['base_experience']) + '\n'
        
        # Stats
        resp += '__Stats:__\n'
        for stat in res.json()['stats']:
            resp += "  **" + " " .join(stat['stat']['name'].split('-')).capitalize() + '**:   *' + str(stat['base_stat']) +'*\n'
        return resp

def ability(name=None, id=None):
    if name==None and id==None:
        return ""

    req = id if name==None else "-".join(name.lower().strip().split())
    res = requests.get(BASE_API + ABILITY_API + req)

    if res.status_code == 404:
        return 0, "Cannot find any ability !"
    else:
        for eff in res.json()['effect_entries']:
            if eff['language']['name'] == 'en':
                return 1, eff

ability('No guard')