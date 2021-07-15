from typing import List
import praw
import asyncpraw
import pandas as pd
from datetime import datetime
import json
import logging
import os
import asyncio


logging.basicConfig(handlers=[logging.FileHandler(filename="redditscrapper.log", 
                                                 encoding='utf-8', mode='a+')],
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s', 
                    datefmt="%F %A %T", 
                    level=logging.DEBUG)


async def save_data(site: str, data_list = List[dict[str, str]], csv=True) -> None:
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



async def reddit_scrap(subreddit: str, limit: int = 100, csv: bool = True) -> None:
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

        return await save_data(site="Reddit", data_list=data, csv=csv)
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

        return await save_data(site="Reddit", data_list=data, csv=csv)
    except Exception as e:
        logging.exception("Reddit Data extraction failed")


logging.info("Start Data Reddit Data Scraping")
asyncio.run(reddit_scrap(subreddit='MachineLearning', limit=500, csv=True))
logging.info("Finished scraping")