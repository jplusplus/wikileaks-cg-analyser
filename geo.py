# -*- coding: utf-8 -*-
import json
import os
# for relative paths
here = lambda x: os.path.join(os.path.abspath(os.path.dirname(__file__)), x)
# Cities and countries data
data = {}

def load_data():
    global data
    # Load cities
    city_path = here("data/cities.json")
    city_file = open(city_path)
    data["cities"] = json.load(city_file)
    # Load countries
    country_path = here("data/countries.json")
    country_file = open(country_path)
    data["countries"] = json.load(country_file)

def get_cities(content):
    global data
    if data == {}: load_data()
    return get_entities_from_list(content, data["cities"])

def get_countries(content):
    global data
    if data == {}: load_data()
    return get_entities_from_list(content, data["countries"])

def get_entities_from_list(content, lst):
    global data
    mentions = set()
    # Same case comparaison
    content = content.upper()
    # Look for each entity
    for key, entity in enumerate(lst):
        # Get all entity aliases
        aliases = entity["alias"].upper().split(",")
        # Add the entity name as an alias
        aliases.insert(0, entity["name"].upper())
        # Look for each alias
        for alias in aliases:
            # Clean the alias
            alias = alias.strip()
            # entity is mentioned
            if len(alias) > 4 and content.find(alias) > -1:
                mentions.add(key)
    # Transform entity set in list of dict
    return [ lst[key] for key in mentions ]

print get_countries(u"Test: lonDRes est une très belle ville comparé à Berlin pour une ville dans le Andorra.")