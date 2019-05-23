#by agricola
import sopel
import random

suit = ['m','p','s']
tiles_per_suit = 9*4
hand_size = 14

def hand_to_str(hand):
    output = ""
    for x in range(len(hand)):
        hand[x].sort()
        for y in hand[x]:
            output += str(y + 1)
        if hand[x]:
            output += suit[x]
    return output

@sopel.module.commands('mj')
def mj(bot, trigger):
    hand = [[],[],[]]
    for y in random.sample(range(tiles_per_suit*3),hand_size):
        hand[y // tiles_per_suit].append((y % tiles_per_suit) // 4)
    bot.say("http://tenhou.net/2/?q={}".format(hand_to_str(hand)))
