import os

import praw
from praw.models import MoreComments
from chatterbot.trainers import ListTrainer

class RedditTrainer(ListTrainer):
  def __init__(self, chatbot):
      super().__init__(chatbot)
      self.reddit_api = self.init_reddit_api()
      self.subreddit = None
      self.current_submission = None
      self.current_submission_comments_retrieved = False
      self.current_comment = None
  
  def train(self, training_rounds):
    for training_round in range(training_rounds):
      print('Training bot: {0} round {1}'.format(self.chatbot.name, training_round))
      self.subreddit = self.get_random_subreddit()
      self.current_submission = self.get_random_submission()
      self.current_submission_comments_retrieved = False

      conversation = self.get_reddit_conversation()
      if conversation:
        print('Conversation: {0}'.format(conversation))
        super().train(conversation)
      else:
        print('No usable conversation')

  def get_subreddit(self, name):
    print(f'Getting subreddit {name}')
    return self.reddit_api.subreddit(name)

  def get_random_subreddit(self, nsfw=False):
    print('Getting random subreddit')
    subreddit = self.reddit_api.random_subreddit(nsfw) 
    print(f'Got subreddit: {subreddit.display_name}')
    return subreddit

  def get_submissions(self, limit):
    print(f'Getting {limit} submissions')
    return self.subreddit.hot(limit=limit)

  def get_random_submission(self):
    print('Getting random submission')
    submission = self.subreddit.random() 
    print(f'Got submission: {submission.title}')
    return submission

  @staticmethod
  def init_reddit_api():
    return praw.Reddit(
      client_id=os.getenv('CLIENT_ID'),
      client_secret=os.getenv('CLIENT_SECRET'),
      username=os.getenv('USERNAME'),
      password=os.getenv('PASSWORD'),
      user_agent="RandomTextSource by /u/RandomWordSource",
    )

  def retrieve_submission_comments(self, max_replace_more_count=1):
    print(f'Replacing up to {max_replace_more_count} replace_more for submission: {self.current_submission.title}')
    self.current_submission.comments.replace_more(limit=max_replace_more_count)  
    self.current_submission_comments_retrieved = True
    
  def get_reddit_conversation(self, max_length=10):
      print(f'Processing submission {self.current_submission.title}')
      if not self.current_submission_comments_retrieved:
        self.retrieve_submission_comments()
      return self.get_conversation_from_current_submission(max_length)  

  def get_conversation_from_current_submission(self, max_length):
    conversation = []
    if not self.current_submission.comments:
      return conversation
    self.current_comment = (self.current_submission.comments[0])
    print(self.current_comment.body)
    conversation = [self.current_comment.body]
    if not self.current_comment.replies:
      return conversation
    conversation.extend(self.get_conversation_statements(self.current_comment.replies[0], max_length-1))
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
