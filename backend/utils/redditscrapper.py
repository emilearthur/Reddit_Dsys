from typing import List, Dict
import praw
import asyncpraw
import pandas as pd
from datetime import datetime
import json
import logging
import os
import asyncio
import httpx

from utils import models


logging.basicConfig(handlers=[logging.FileHandler(filename="logs/redditscrapper.log", 
                                                 encoding='utf-8', mode='a+')],
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s', 
                    datefmt="%F %A %T", 
                    level=logging.DEBUG)


def save_data(site: str, data_list = List[Dict[str, str]], csv=True) -> None:
    """[summary]

    Args:
        site (str): [description]
        data_list ([type], optional): [description]. Defaults to List[dict[str, str]].
        csv (bool, optional): [description]. Defaults to True.
    """
    outputfilename = f"output_{site}_{datetime.now().strftime('%d-%m-%Y-%H-%M')}"
    if not csv:
        with open(os.path.join('./Data', outputfilename+".txt"), "w") as outfile:
            outfile.write(json.dumps(data_list))
            outfile.close()
            logging.info(f"Data saved in Data folder as {outputfilename}.txt")
    else:
        data = pd.DataFrame(data_list, columns=['extracted_at', 'name', 'id', 'title', 'score', 'url', 'author', 
                                                'subreddit', 'description', 'created_at'])
        data.to_csv(os.path.join('./Data', outputfilename+'.csv'), index=False)
        logging.info(f"Data saved in Data folder as {outputfilename}.csv")


def reddit_scrap(subreddit: str, limit: int = 10, csv: bool = True) -> None:
    """Extracts subbreddit. Not using asyncpraw library.

    Args:
        subreddit (str): [The subreddit you will like to scape]
        limit (int, optional): [the number of subreddit you will like to scrape]. Defaults is 100.
        csv (bool, optional): [Set True if you like output file to be in csv. Else false]. Defaults to True.

    Returns:
        [None]: [Send data extracted to the save_data function]
    """
    reddit = praw.Reddit("Scapper1")
    data = []
    try:
        posts = reddit.subreddit(subreddit).hot(limit=limit)
        for post in posts:
            data_dict = {
                'extracted_at': datetime.utcnow().timestamp(),
                'name': post.name,
                'post_id': post.id,
                'title': post.title,
                'score': post.score,
                'url': post.url,
                'author': str(post.author), 
                'subreddit': post.subreddit_name_prefixed,
                'description': post.selftext,
                'created_at': post.created_utc,
            }
            data_subreddit = models.Subreddit(**data_dict)
            # post_subreddit(json.dumps(data_subreddit.dict()))
            worker.insert_intodb.delay(data_subreddit)
            
            data.append(data_subreddit.dict())

        return save_data(site=f"{subreddit}-Reddit", data_list=data, csv=csv)
    except Exception as e:
        logging.exception("Reddit Data extraction failed")
        # print("Reddit Data extraction failed. See Exception")
        # print(e)


async def reddit_scrap_async(subreddit: str = "MachineLearning", limit: int = 100, csv: bool = True) -> None:
    """Extracts subbreddit. Using asyncpraw library

    Args:
        subreddit (str): [The subreddit you will like to scape]. Defaults is "MachineLearning".
        limit (int, optional): [the number of subreddit you will like to scrape]. Defaults is 100.
        csv (bool, optional): [Set True if you like output file to be in csv. Else false]. Defaults to True.

    Returns:
        [None]: [Send data extracted to the save_data function]
    """
    reddit = asyncpraw.Reddit("Scapper1")
    data = []
    try:
        subreddit = await reddit.subreddit(subreddit)
        posts = [post async for post in subreddit.hot(limit=limit)]
        for post in posts:
            data_dict = {
                'extracted_at': str(datetime.utcnow()),
                'name': post.name,
                'id': post.id,
                'title': post.title,
                'score': post.score,
                'url': post.url,
                'author': str(post.author), 
                'subreddit': post.subreddit_name_prefixed,
                'description': post.selftext,
                'created_at': str(datetime.utcfromtimestamp(post.created_utc)),
            }

            data.append(data_dict)

        return save_data(site=f"{subreddit}-Reddit", data_list=data, csv=csv)
    except Exception as e:
        logging.exception("Reddit Data extraction failed")



def post_subreddit(data: dict, url=f"http://localhost:8000/api/subreddit/"):
    """Disabled due to partially initialized module error"""
    try:
        resp = httpx.post(url, data=json.dumps(data))
        logging.INFO(f"{resp.json()['post_id']} with status{resp.status_code}")

    except Exception:
        logging.exception("Reddit Data extraction failed")


logging.info("Start Data Reddit Data Scraping")
reddit_scrap(subreddit='MachineLearning', limit=10, csv=True)
logging.info("Finished scraping")