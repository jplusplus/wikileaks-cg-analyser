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
    # country_path = here("data/countries.json")
    # country_file = open(country_path)
    # data["countries"] = json.load(country_file)


def get_cities(content):
    global data
    mentions = set()
    # Same case comparaison
    content = content.upper()
    # Look for each city
    for key, city in enumerate(data["cities"]):
        # Get all city aliases
        aliases = city["alias"].upper().split(",")
        # Add the city name as an alias
        aliases.insert(0, city["name"].upper())
        # Look for each alias
        for alias in aliases:
            # Clean the alias
            alias = alias.strip()
            # City is mentioned
            if len(alias) > 4 and content.find(alias) > -1:
                mentions.add(key)
    # Transform city set in list of dict
    cities = [ data["cities"][key] for key in mentions ]
    print cities


load_data()
get_cities(u"Test: lonDRes est une très belle ville comparé à Berlin.")