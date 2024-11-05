import pandas as pd
import datetime as dt

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns

from transformers import pipeline

posts_df = pd.read_csv('subredd_posts.csv')
comments_df = pd.read_csv('subredd_comments.csv')

# some useful metrics
number_of_posts = posts_df.shape[0]
number_of_comments = comments_df.shape[0]
count_subreddits = posts_df['subreddit'].nunique()

# Convert Date of creation to DataTime values
posts_df['created_date'] = posts_df['created_utc'].apply(lambda x: dt.datetime.fromtimestamp(x))
posts_df['created_year'] = posts_df['created_date'].dt.year
posts_df

# Combine posts with comments
comments_posts_df = posts_df.merge(comments_df, on='post_id', how='left')
# Delete Posts with no comments
comments_posts_df = comments_posts_df[~comments_posts_df['comment'].isnull()]

# Classification based on sentiment
sentiment_classifier = pipeline(model="finiteautomata/bertweet-base-sentiment-analysis",max_length=512,truncation=True)

def get_sentiment(text):
    try:
        sentiment = sentiment_classifier(text)[0]['label']
    except:
        sentiment = 'Not classified'
    return sentiment

comments_posts_df_sub = comments_posts_df[comments_posts_df['post_title'].str.contains('YourInput')]

# Add a column of the sentiment corresponding to the evaluated comment
comments_posts_df_sub['sentiment'] = comments_posts_df_sub['comment'].astype(str).apply(lambda x: get_sentiment(x))

# Classification based on emotions
emotion_classifier = pipeline("text-classification",model='bhadresh-savani/distilbert-base-uncased-emotion', top_k=None)

def get_emotion(text):
    pred_scores = emotion_classifier(text)
    emotion = max(pred_scores[0], key=lambda x: x['score'])['label']
    return emotion

# Add a column of the emotional score to the evaluated comment
comments_posts_df_sub['emotion'] = comments_posts_df_sub['comment'].astype(str).apply(lambda x: get_emotion(x))

# Merge all posts and comments into a text file
comments_posts_df_tmp = comments_posts_df[['post_title', 'selftext','comment']].astype(str)
agg_comments = comments_posts_df_tmp.groupby(['post_title', 'selftext'])['comment'].apply('. '.join).reset_index()

#  RUN AND SAVE ONCE
agg_comments['combined_text'] = agg_comments.astype(str).agg('. '.join, axis=1)
all_text = ' '.join(agg_comments['combined_text'])

# Save all the text to .txt file
f = open("../data/SampleData.txt", "w")
f.write(all_text)
f.close()
