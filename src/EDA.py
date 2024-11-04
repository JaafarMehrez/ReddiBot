import pandas as pd
import datetime as dt

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns

from transformers import pipeline

posts_df = pd.read_csv('subredd_posts.csv')
comments_df = pd.read_csv('subredd_comments.csv')
