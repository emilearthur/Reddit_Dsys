from celery import Task
from celery.schedules import crontab
import logging
import logging
from typing import List
import praw
import pandas as pd
from datetime import datetime
import json
import logging
import os
import json
from celery import Celery
from fastapi import Depends



from utils.models import Extracted_Created_Date, Subreddit, SubredditDB
from utils.datetime_fixer import datetimefixer

from app.models.subreddit import SubredditCreate, SubredditInDB
from app.db.repositories.subreddits import SubredditRepository
from app.api.dependencies.database import get_repository


logging.basicConfig(filename='redditscrapper.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',)


app = Celery('scrapper_worker')

app.conf.broker_url = "redis://redis:6379/0"
app.conf.result_backend = "redis://redis:6379/0"
app.conf.timezone = 'UTC'

app.conf.beat_schedule = {
    'scraping-task-reddit-ten-min': {
        'task': 'tasks.scrape_data_reddit_ml',
        'schedule': crontab(minute='*/30'),
    },

    'scraping-task-fifteen-min': {
        'task': 'tasks.scrape_data_reddit_bitcoin',
        'schedule': crontab(minute='*/360')
    },
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


class SqlALchemyTask(Task):
    """Refered to http://www.prschmid.com/2013/04/using-sqlalchemy-with-celery-tasks.html"""
    abstract = False
    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        #db.remove()
        pass

#@app.task(base=SqlALchemyTask)
# @app.task()
async def insert_intodb(new_subreddit: SubredditCreate):
    """Input scrapped subreddit into db."""
    subreddit_repo: SubredditRepository = Depends(get_repository(SubredditRepository))
    await subreddit_repo.create_subreddit(new_subreddit=new_subreddit)
    # params = SubredditDB(**subreddit.dict(exclude={"extracted_at", "created_at"}))
    # datetime_fixed  = datetimefixer(extracted_at=subreddit.extracted_at, created_at=subreddit.created_at)
    # updated_params = params.copy(update=datetime_fixed.dict())
    # CREATE_SUBREDDIT_QUERY = """
    # INSERT INTO posts (extracted_at, name, post_id, title, score, url, author, subreddit, description, created_at, isscore)
    # VALUES(:extracted_at, :name, :post_id, :title, :score, :url, :author, :subreddit, :description, :created_at, :isscore)
    # """

    # await db.execute(query=CREATE_SUBREDDIT_QUERY, values=updated_params.dict())

def save_data(outputfilename: str, data_list = List[dict[str, str]], csv=True) -> None:
    """[summary]

    Args:
        site (str): [description]
        data_list ([type], optional): [description]. Defaults to List[dict[str, str]].
        csv (bool, optional): [description]. Defaults to True.
    """
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

@app.task
def reddit_scrap(outputfile: str, subreddit:str, limit: int = 10, csv: bool = True) -> None:
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
            data_subreddit = SubredditCreate(**data_dict)
            # post_subreddit(json.dumps(data_subreddit.dict()))
            insert_intodb(new_subreddit=data_subreddit)            
            data.append(data_subreddit.dict())
        return save_data(outputfilename=outputfile, data_list=data, csv=csv)
    except Exception as e:
        logging.exception("Reddit Data extraction failed")


@app.task
def scrape_data_reddit_ml(serializer='json'):
    subreddit, csv = 'MachineLearning', True
    outputfile = f"output_{subreddit}_{datetime.now().strftime('%d-%m-%Y-%H-%M')}"
    reddit_scrap.delay(outputfile = outputfile, subreddit=subreddit, limit=20, csv=True)
    #action_data_indb(data=outputfile, csv=csv)
    return "Process Sent"


@app.task
def scrape_data_reddit_bitcoin(serializer='json'):
    subreddit, csv = 'Bitcoin', True
    outputfile = f"output_{subreddit}_{datetime.now().strftime('%d-%m-%Y-%H-%M')}"
    reddit_scrap.s(outputfile = outputfile, subreddit=subreddit, limit=20, csv=True).apply_async()
    return "Process Sent"


def action_data_indb(data:str, csv=bool):
    insert_intodb.apply_async(args=(data, csv))
