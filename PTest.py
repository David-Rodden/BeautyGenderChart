import praw
from private_info.Login import private_login
import re

reddit = private_login()
for submission in reddit.subreddit("amiugly").new(limit=10):
    gender = re.search(".*(\d+)?(M|F)(\d+)?.*", submission.title)
    if not gender:
        continue
    print("Gender: " + gender.group(2))
    for comment in submission.comments:
        m = re.search('.*(\d+(\.\d+)).*', comment.body)
        if m:
            print(m.group(1))
