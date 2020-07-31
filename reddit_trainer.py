import os

import praw
from praw.models import MoreComments
from chatterbot.trainers import ListTrainer

class RedditTrainer(ListTrainer):
  def __init__(self, chatbot):
      super().__init__(chatbot)
      self.reddit_api = self.init_reddit_api()
      self.subreddit = self.get_subreddit('all')
      self.submissions = self.get_next_hot_submissions()
  
  def train(self, training_rounds):
    for round in range(training_rounds):
      print('Training bot: {0} round {1}'.format(self.chatbot.name, round+1))
      conversation = self.get_reddit_conversation()
      print('Conversation: {0}'.format(conversation))
      super().train(conversation)

  def get_subreddit(self, name):
    return self.reddit_api.subreddit(name)

  def get_next_hot_submissions(self, limit=5):
    return self.subreddit.hot(limit=limit)

  
  @staticmethod
  def init_reddit_api():
    return praw.Reddit(client_id=os.getenv('CLIENT_ID'),
                        client_secret=os.getenv('CLIENT_SECRET'),
                        username=os.getenv('USERNAME'),
                        password=os.getenv('PASSWORD'),
                        user_agent="RandomTextSource by /u/RandomWordSource",
                        )

    
  def get_reddit_conversation(self, max_length=10):
    for submission in self.submissions:
      print(f'Processing submission {submission.title}')
      submission.comments.replace_more(limit=None)
      print('Finished replace_more')
      conversation = []
      for top_level_comment in submission.comments:
        print(top_level_comment.body)
        conversation = [top_level_comment.body]
        conversation.extend(self.get_conversation_statements(top_level_comment.replies[0], max_length-1))
        return conversation


  def get_conversation_statements(self, comment, conversation_length_remaining):
    print(f'Conversation length remaining {conversation_length_remaining}')
    if conversation_length_remaining == 0 or not list(comment.replies):
      print('Final')
      print(f'Comment body {comment.body}')
      return [comment.body]
    else:
      print('Not final')
      print(f'Comment body {comment.body}')
      lower_level_comments = self.get_conversation_statements(comment.replies[0], conversation_length_remaining-1)
      return [comment.body] + lower_level_comments
