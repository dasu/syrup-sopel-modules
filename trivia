import requests
import json
import sopel
import html.parser
from random import shuffle

g_question = None

@sopel.module.commands('trivia')
def trivia(bot, input):
    header =  {"User-Agent": "Syrup/1.0"}
    response = requests.get("https://opentdb.com/api.php?amount=1", headers=header)
    data = response.json()
    if data['response_code'] != 0:
        bot.say("Error getting question, sorry.")
        return

    global g_question
    g_question = data["results"][0]

    if g_question["type"] == "multiple":
        options = [g_question["correct_answer"],] + g_question["incorrect_answers"]
        shuffle(options)
        possible_answers = ", ".join(options)
    else:
        possible_answers = "True/False"

    response = "Trivia: {0} | [{1}]".format(g_question["question"], possible_answers)
    bot.say(html.parser.HTMLParser().unescape(response))

@sopel.module.commands('answer')
def trivia_answer(bot, input):
    if g_question is None:
        return bot.say("I don't have an answer for you.")

    global g_question
    question = g_question["question"]
    answer = g_question["correct_answer"]
    bot.say(html.parser.HTMLParser().unescape("Trivia: %s | Answer: %s" % (question, answer)))
