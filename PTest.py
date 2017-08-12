import praw
import plotly.plotly as plot
import plotly.graph_objs as gobs

from private_info.Login import reddit_login, set_plotly_config
import re

reddit = reddit_login()

female_stats = []
male_stats = []
for submission in reddit.subreddit("amiugly").new(limit=5000):
    gender = re.search(".*(\d+)?(m|f)(\d+)?.*", submission.title.lower())
    if not gender:
        continue
    for comment in submission.comments:
        m = re.search('.*(\d+(\.\d+)).*', comment.body)
        if m:
            score = float(m.group(1))
            # print(str(score) + ": " + submission.url)
            if score < 10:
                if gender.group(2) == "f":
                    female_stats.append(score)
                else:
                    male_stats.append(score)

female_bplot = gobs.Box(name="Female", fillcolor='rgba(249, 119, 191, 0.4)', y=female_stats, boxpoints='all',
                        jitter=0.3, pointpos=-1.8)
male_bplot = gobs.Box(name="Male", fillcolor='rgba(66, 152, 244, 0.4)', y=male_stats, boxpoints='all', jitter=0.3,
                      pointpos=-1.8)
set_plotly_config()
plot.plot([male_bplot, female_bplot])
