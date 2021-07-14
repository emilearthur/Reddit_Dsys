from os import execlp
from typing import List
import praw
import pandas as pd
from datetime import datetime
import json
import logging

logging.basicConfig(filename='redditscrapper.log', encoding='utf-8', level=logging.DEBUG)

def save_data(site: str, data_list = List[dict[str, str]], csv=True):
    """
    Recieves a list of data scrapped and saves outputs as txt file or csv file
    """
    outputfilename = f"output_{site}_{datetime.now().strftime('%d-%m-%Y-%H-%M')}"
    if not csv:
        with open(outputfilename+".txt", "w") as outfile:
            json.dump(data_list, outfile)
            
    
    data = pd.DataFrame(data_list, columns=['id', 'title', 'score', 'url', 'author', 'subreddit', 'description'])
    data.to_csv(outputfilename, index=False)
    logging.info(f"Data saved as{outputfilename}")


def reddit_scrap(subreddit: str, limit: int) -> None:
    reddit = praw.Reddit(client_id='rM9D0StsGDcFEEqEhkFyOw', client_secret='Uf7u48btvM5WtHovscPdzOEe4NPRLQ', user_agent='emile_scrapper')
    data = []
    try:
        hot_posts = reddit.subreddit(subreddit).hot(limit=limit)
        for post in hot_posts:
            data_dict = {
                'id': post.id,
                'title': post.title,
                'score': post.score,
                'url': post.url,
                'author': post.author, 
                'subreddit': post.subreddit_name_prefixed,
                'description': post.selftext
            }
        # add logger here
        return save_data(site="Reddit", data_list=data, csv=True)
    except Exception as e:
        logging.exception("Reddit Data extraction failed")
        # print("Reddit Data extraction failed. See Exception")
        # print(e)


logging.info("Start Data Reddit Data Scraping")
reddit_scrap(topic='MachineLearning, 20')
logging.info("Finished scraping")