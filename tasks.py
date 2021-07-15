from celery import Celery
from celery.schedules import crontab
import logging

from typing import List
import praw
import pandas as pd
from datetime import datetime
import json
import logging
import os
import asyncio
from redditscrapper import save_data, reddit_scrap


logging.basicConfig(filename='redditscrapper.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',)

app = Celery('tasks') # define the app anme to be used in our flag

app.conf.timezone = 'UTC'

app.conf.beat_schedule = {
    # executes every 1 minute
    'scraping-task-one-min': {
        'task': 'tasks.scrape_data',
        'schedule': crontab(minute='*/10'),
    },
    # # executes every 15 minutes
    # 'scraping-task-fifteen-min': {
    #     'task': 'tasks.hackernews_rss',
    #     'schedule': crontab(minute='*/15')
    # },
    # # executes daily at midnight
    # 'scraping-task-midnight-daily': {
    #     'task': 'tasks.hackernews_rss',
    #     'schedule': crontab(minute=0, hour=0)
    # }
}


@app.task
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
        data = pd.DataFrame(data_list, columns=['extracted_at', 'id', 'title', 'score', 'url', 'author', 
                                                'subreddit', 'description', 'created_at'])
        data.to_csv(os.path.join('./Data', outputfilename+'.csv'), index=False)
        logging.info(f"Data saved in Data folder as {outputfilename}.csv")



@app.task
def scrape_data():
    asyncio.run(reddit_scrap(subreddit='MachineLearning', limit=500, csv=True))

# run this at terminal 
# celery -A tasks worker -l info
# celery -A tasks worker -B -l info