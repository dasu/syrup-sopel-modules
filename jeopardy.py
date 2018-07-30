import requests
import sopel

j_question = None

@sopel.module.commands('jeopardy','j')
def jeopardy(bot, trigger):
  x = requests.get("http://jservice.io/api/random").json()
  global j_question
  j_question = x[0]
  question = x[0]['question']
  value = x[0]['value']
  title = x[0]['category']['title']
  bot.say("[{} | {}] {}".format(title, value, question))

@sopel.module.commands('jeopardyanswer','ja')
def jeopardy_answer(bot, trigger):
  if j_question is None:
    return bot.say("I don't have an answer for you")
  global j_question
  question = j_question['question']
  answer = j_question['answer']
  bot.say("Question: {}| Answer: {}".format(question, answer))
