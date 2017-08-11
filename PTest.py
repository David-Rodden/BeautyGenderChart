import praw
from private_info.Login import private_login
import re

reddit = private_login()

female_stats = []
male_stats = []
for submission in reddit.subreddit("amiugly").new(limit=20):
    gender = re.search(".*(\d+)?(m|f)(\d+)?.*", submission.title.lower())
    if not gender:
        continue
    for comment in submission.comments:
        m = re.search('.*(\d+(\.\d+)).*', comment.body)
        if m:
            score = float(m.group(1))
            print(str(score) + ": " + submission.url)
            if score < 10:
                if gender.group(2) == "f":
                    female_stats.append(score)
                else:
                    male_stats.append(score)
print(female_stats)
print(male_stats)
