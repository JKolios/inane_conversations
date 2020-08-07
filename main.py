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

# def chatbot_converse(chatbot=None):
#   while True:
#       sentence = q.get()
#       sentence.text = clean_sentence_text(sentence.text)
#       response = chatbot.get_response(sentence)
#       response.text = clean_sentence_text(response.text)
#       print(f'{chatbot.name}: {response}')
#       q.put(response)
#       q.task_done()
#       sleep(0.1)

# def chatbot_train(chatbot=None):
#   bot_trainer = RedditTrainer(chatbot)
#   while True:
#       bot_trainer.train(10)
#       sleep(30)

def train_bot(bot):
	bot_trainer = RedditTrainer(bot)
	try:
		bot_trainer.train(5)
	except:
		pass # Ignore any training errors for now

def main():
	# q.put(Statement("Hi!"))
	bots = bot_creator.create_bots(['Alice', 'Bob'])
	conversation_index = 0
	training_iterations = 0
	topic = 'Hi'
	while True:
		if conversation_index == 100:
			print(f'Training bots, iteration {training_iterations}')
			for bot in bots:
				train_bot(bot)
			training_iterations +=1
			conversation_index = 0
		else:
			for bot in bots:
				topic = bot.get_response(topic)
				print(f'{bot.name}: {topic}')
				conversation_index += 1
				# sleep(0.1)
		


	


	

	# for bot in bots:
	# threading.Thread(target=chatbot_converse, daemon=True, kwargs={'chatbot': bot}).start()
	# threading.Thread(target=chatbot_train, daemon=True, kwargs={'chatbot': bot}).start()

	# q.join()

if __name__ == '__main__':
	main()