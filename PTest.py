import praw
import plotly.plotly as plot
import plotly.graph_objs as gobs

from private_info.Login import reddit_login, set_plotly_config
import re

reddit = reddit_login()

female_stats = []
male_stats = []
current = 0
gender_sample = 100
female = male = gender_sample
for submission in reddit.subreddit("amiugly").new(limit=gender_sample * 3):
    gender = re.search(".*(\d+)?(m|f)(\d+)?.*", submission.title.lower())
    if not gender:
        continue
    gender_letter = gender.group(2)
    if not gender_letter:
        continue
    if gender_letter is 'f' and female is 0:
        continue
    if gender_letter is 'm' and male is 0:
        continue
    for comment in submission.comments:
        m = re.search('(.*s+)?(\d+(\.\d+)?)\s*/\s*10.*', comment.body)
        potentiality = re.search('(could be|potential|almost)', comment.body)
        if potentiality:
            continue
        if m:
            score = None
            for g in m.groups():
                if g is None:
                    continue
                try:
                    score = float(g)
                except ValueError:
                    continue
            if score is None:
                continue
            if score <= 10:
                if gender_letter is "f":
                    female_stats.append(score)
                else:
                    male_stats.append(score)

female_bplot = gobs.Histogram(x=female_stats, histnorm='Score', name='female',
                              xbins=dict(start=0.0, end=10.0, size=1.0), marker=dict(color='rgb(255, 99, 143)'),
                              opacity=0.5)
male_bplot = gobs.Histogram(x=male_stats, name='male',
                            xbins=dict(start=0.0, end=10.0, size=1.0), marker=dict(color='rgb(66, 152, 244)'),
                            opacity=0.5)
layout = gobs.Layout(title='r/amiugly Scores by Gender', xaxis=dict(title='Score'), yaxis=dict(title='Prevalence'),
                     bargap=0.3, bargroupgap=0.1)
set_plotly_config()
plot.plot(gobs.Figure(data=[male_bplot, female_bplot], layout=layout))
