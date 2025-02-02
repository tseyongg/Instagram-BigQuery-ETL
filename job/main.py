import os
import pytz
from datetime import datetime
import asyncio
import logging
from instagram_client import InstagramClient
from bigquery_loader import BigQueryLoader

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    try:
        instagram_id = os.environ.get('INSTAGRAM_ACCOUNT_ID')
        instagram_token = os.environ.get('INSTAGRAM_ACCESS_TOKEN')
        
        if not instagram_id or not instagram_token:
            logger.error("Instagram credentials are not set in environment variables.")
            return
        
        singapore_tz = pytz.timezone('Asia/Singapore')
        bigquery = BigQueryLoader("winged-yeti-440908-r9.instagram_analytics")
        
        async with InstagramClient(instagram_id, instagram_token, singapore_tz) as instagram:
            posts = await instagram.fetch_posts()
            logger.info(f"Successfully fetched {len(posts)} posts")
            
            comments_tasks = []
            insights_tasks = []
            for post in posts:
                post_id = post['post_id']
                comments_tasks.append(instagram.fetch_comments_for_post(post_id))
                insights_tasks.append(instagram.fetch_insights_for_post(post_id, post['media_type']))
            
            all_comments_lists = await asyncio.gather(*comments_tasks)
            all_insights = await asyncio.gather(*insights_tasks)
            
            all_comments = []
            for i, comments_list in enumerate(all_comments_lists):
                all_comments.extend(comments_list)
                posts[i]['comments_count'] = len(comments_list)
            
            all_insights = [insight for insight in all_insights if insight is not None]
        
        logger.info(f"Loading {len(posts)} posts into {bigquery.project_dataset}.posts with WRITE_TRUNCATE...")
        posts_loaded = bigquery.load_posts(posts)
        logger.info(f"Loaded {posts_loaded} posts into {bigquery.project_dataset}.posts")

        if all_comments:
            logger.info(f"Loading {len(all_comments)} comments into {bigquery.project_dataset}.comments with WRITE_TRUNCATE...")
            comments_loaded = bigquery.load_comments(all_comments)
            logger.info(f"Loaded {comments_loaded} comments into {bigquery.project_dataset}.comments")
        else:
            comments_loaded = 0
        
        if all_insights:
            logger.info(f"Loading {len(all_insights)} insights into {bigquery.project_dataset}.insights with WRITE_TRUNCATE...")
            insights_loaded = bigquery.load_insights(all_insights)
            logger.info(f"Loaded {insights_loaded} insights into {bigquery.project_dataset}.insights")
        else:
            insights_loaded = 0
        
        logger.info(f"Job completed successfully at {datetime.now(singapore_tz).strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"Posts processed: {posts_loaded}, Comments processed: {comments_loaded}, Insights processed: {insights_loaded}")
        
    except Exception as e:
        logger.error(f"Unexpected error occurred: {type(e).__name__} - {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())