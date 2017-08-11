import praw
from private_info.Login import private_login

reddit = private_login()
for submission in reddit.subreddit("amiugly").new(limit=25):
    for comment in submission.comments:
        print("__________\n" + comment.body)
