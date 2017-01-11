import sopel
import json
import requests
from string import Template

URL = 'https://shadowverse-portal.com/api/v1/cards?format=json&lang=en'

class Card:
    def __init__(self, json, index, start):
        self.json = json
        self.index = index
        self.start = start

def get_cards():
    response = requests.get(URL)
    return response.json()

def find_index(term, name):
    n = name.lower()
    t = term.lower()
    return n.find(t)

def is_start_of_word(w, i):
    return True if (i == 0 or w[i-1] == " " or w[i-1] == "-" or w[i-1] == "'") else False

def create_a_card(search_term, card):
    n = card['card_name']
    index = find_index(search_term, n)
    is_start = is_start_of_word(n, index) if index > -1 else False
    return Card(card, index, is_start)

def create_cards(search_term, cards):
    return map(lambda card: create_a_card(search_term, card), cards)

def filter_cards(search_term, cards):
    return filter(lambda card: card.index > -1, cards)

def card_sort_value(card):
    ind = card.index
    return ind if card.start else len(card.json['card_name']) + ind

def sort_cards(cards):
    return sorted(cards, key=card_sort_value)

def card_output(card):
    c = card.json
    char_type = c['char_type']
    if char_type == 1:
        s = Template('$name, [$type], Cost: $cost, $atk/$hp ($eatk/$ehp), "$eff" ("$eveff")')
        r = s.substitute(name=c['card_name'], type="Minion", cost=c['cost'],
        atk=c['atk'], hp=c['life'], eatk=c['evo_atk'], ehp=c['evo_life'],
        eff=c['skill_disc'], eveff=c['evo_skill_disc'])
    else:
        s = Template('$name, [$type], Cost: $cost, "$eff"')
        t = "Spell" if char_type == 4 else "Amulet"
        r = s.substitute(name=c['card_name'], type=t, cost=c['cost'], eff=c['skill_disc'])
    return r

def process_json_data(data):
    return data['data']['cards']

def search_cards(search_term, callback, json_data=None):
    js_data = json_data if json_data else get_cards()
    card_data = process_json_data(js_data)
    cards = create_cards(search_term, card_data)
    filtered_cards = filter_cards(search_term, cards)
    sorted_cards = sort_cards(filtered_cards)
    relevant_cards = list(sorted_cards)
    if len(relevant_cards) < 1:
        callback('Card not found')
    else:
        final_card = relevant_cards[0]
        output = card_output(final_card)
        callback(output)

@sopel.module.commands('sv','shadowverse')
def sv(bot,trigger):
    if not trigger.group(2):
        return bot.say("Please enter a card name.")
    search_cards(trigger.group(2), bot.say)
