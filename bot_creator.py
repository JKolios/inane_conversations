import os

import chatterbot 
from chatterbot.filters import get_recent_repeated_responses
from chatterbot.trainers import ChatterBotCorpusTrainer

default_chatbot_filters = [get_recent_repeated_responses]

default_chatbot_kwargs = {
  "storage_adapter": "chatterbot.storage.MongoDatabaseAdapter",
  "database_uri":os.getenv('MONGO_URI')
}

def create_bots(names):
  bots = []
  for name in names:
    bot = chatterbot.ChatBot(name,filters=default_chatbot_filters, **default_chatbot_kwargs)
    bots.append(bot)
  return bots
