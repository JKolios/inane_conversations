import threading
import queue
import random
from time import sleep

import ipdb

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.storage import SQLStorageAdapter
from chatterbot.filters import get_recent_repeated_responses
from chatterbot.conversation import Statement

import praw
from praw.models import MoreComments

def init_reddit_api():
  return praw.Reddit(client_id="lM64lMYD0mcKVQ",
                      client_secret="wJpUO-nWJQ28D-uwmUNjTokUT18",
                      password="1VOIDoblivion#",
                      user_agent="RandomTextSource by /u/RandomWordSource",
                      username="RandomWordSource")

def get_reddit_comments(reddit):
  subreddit = reddit.subreddit("all")
  for comment in subreddit.stream.comments(pause_after=5):
    if comment is None:
        break
    yield comment

q = queue.Queue()

translation_table = dict.fromkeys(map(ord, '+!@#$'), None)

def clean_sentence_text(text):
  clean_text = text.translate(translation_table)
  if clean_text == "":
    clean_text = '...'
  return clean_text

def chatbot_worker(chatbot=None):
  while True:
      sentence = q.get()
      sentence.text = clean_sentence_text(sentence.text)
      response = chatbot.get_response(sentence)
      response.text = clean_sentence_text(response.text)
      print(f'{chatbot.name} hears {sentence} and responds: {response}')
      q.put(response)
      q.task_done()
      sleep(random.randint(1,3))

def sentence_injector_worker(reddit=None):
  while True:
    for comment in get_reddit_comments(reddit):
      injected_statement = Statement(comment.body)  
      print(f'INJECTING STATEMENT: {injected_statement}')
      q.put(injected_statement)
    sleep(random.randint(60,100))

chatbot_kwargs = {
  "storage_adapter": "chatterbot.storage.MongoDatabaseAdapter",
  "database_uri":"mongodb://192.168.99.105:27017/inane"
  }

alice = ChatBot("Alice", filters=[get_recent_repeated_responses], **chatbot_kwargs)
trainer = ChatterBotCorpusTrainer(alice)
trainer.train("chatterbot.corpus.english")

bob = ChatBot("Bob", filters=[get_recent_repeated_responses], **chatbot_kwargs)
trainer = ChatterBotCorpusTrainer(bob)
trainer.train("chatterbot.corpus.english")

chuck = ChatBot("Chuck", filters=[get_recent_repeated_responses], **chatbot_kwargs)
trainer = ChatterBotCorpusTrainer(chuck)
trainer.train("chatterbot.corpus.english")

bots = [alice, bob, chuck]

q.put(Statement("Good morning"))

for bot in bots:
  threading.Thread(target=chatbot_worker, daemon=True, kwargs={'chatbot': bot}).start()

threading.Thread(target=sentence_injector_worker, daemon=True, kwargs={'reddit': init_reddit_api()}).start()

q.join()

# while True:
#   for bot in bots:
#     response = bot.get_response(response)
#     if str(response) == '':
#       response = '...'
#     print('{0}: {1}'.format(bot.name, response))
