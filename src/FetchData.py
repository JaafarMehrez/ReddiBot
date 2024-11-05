import praw
import pandas as pd

reddit = praw.Reddit(client_id='YourClientID',
                     client_secret='YourClientSecretKey',
                     redirect_uri="http://localhost/8080",
                     user_agent='YourUserAgent')

def fetch_top_posts(subreddit_list='SubredditName', limit=1000, time_filter='all'):

    posts = reddit.subreddit(subreddit_list).top(time_filter="all", limit=100)
    
    # Post DataFrame
    posts_df = []

    for post in posts:
        posts_df.append({'post_id': post.id,
                        'subreddit': post.subreddit,
                        'created_utc': post.created_utc,
                        'selftext':post.selftext,
                        'post_title': post.title,
                        'link_flair_text': post.link_flair_text,
                        'score': post.score,
                        'num_comments': post.num_comments,
                        'upvote_ratio':post.upvote_ratio
                        })
    return pd.DataFrame(posts_df)

posts_df = fetch_top_posts(subreddit_list='SubredditName', limit=1000, time_filter='all')
posts_df.to_csv('subredd_posts.csv', header=True, index=False)

# Fetch Comments from Posts
comments_list = []

for post_id in posts_df['post_id']:
    submission = reddit.submission(post_id)

    submission.comments.replace_more(limit=100)
    for comment in submission.comments.list():
        comments_list.append({'post_id': post_id,
                              'comment': comment.body})
comments_df = pd.DataFrame(comments_list)
comments_df.to_csv('subredd_comments.csv', header=True, index=False)
