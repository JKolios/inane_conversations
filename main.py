import threading
import queue
import random
from time import sleep
import os

from chatterbot.conversation import Statement
from reddit_trainer import RedditTrainer

import bot_creator
from sentence_cleaner import clean_sentence_text

q = queue.Queue()

def chatbot_worker(chatbot=None):
  while True:
      sentence = q.get()
      sentence.text = clean_sentence_text(sentence.text)
      response = chatbot.get_response(sentence)
      response.text = clean_sentence_text(response.text)
      print(f'{chatbot.name}: {response}')
      q.put(response)
      q.task_done()
      sleep(0.1)


def main():
  q.put(Statement("Hi!"))

  bots = bot_creator.create_bots(['Alice', 'Bob'])
  for bot in bots:
    bot_trainer = RedditTrainer(bot)
    bot_trainer.train(10)
  
  for bot in bots:
    threading.Thread(target=chatbot_worker, daemon=True, kwargs={'chatbot': bot}).start()

  q.join()

if __name__ == '__main__':
  main()