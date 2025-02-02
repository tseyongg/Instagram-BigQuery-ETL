import aiohttp
from datetime import datetime
from typing import List, Dict, Optional
import asyncio

class InstagramClient:
    def __init__(self, account_id: str, access_token: str, singapore_tz):
        self.account_id = account_id
        self.access_token = access_token
        self.base_url = 'https://graph.facebook.com/v20.0'
        self.singapore_tz = singapore_tz
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def fetch_posts(self, limit: int = 4000) -> List[Dict]:
        """Fetch Instagram posts"""
        fields = 'id,caption,media_type,timestamp,like_count,comments_count,permalink'
        url = f'{self.base_url}/{self.account_id}/media'
        
        params = {
            'access_token': self.access_token,
            'fields': fields,
            'limit': limit
        }

        try:
            async with self.session.get(url, params=params) as response:
                response.raise_for_status()
                data = await response.json()
                posts_data = data.get('data', [])
                return [self._process_post(post) for post in posts_data]
        except Exception as e:
            print(f"Error fetching posts: {e}")
            return []

    async def fetch_comments_for_post(self, post_id: str) -> List[Dict]:
        """Fetch comments for a specific post"""
        fields = 'id,text,timestamp,from,like_count'
        url = f'{self.base_url}/{post_id}/comments'
        
        params = {
            'access_token': self.access_token,
            'fields': fields,
            'limit': 100
        }
        
        all_comments_for_post = []
        
        try:
            async with self.session.get(url, params=params) as response:
                response.raise_for_status()
                data = await response.json()
                comments_data = data.get('data', [])
                all_comments_for_post.extend(comments_data)
                
                # Safer way to check for next page
                paging = data.get('paging', {})
                next_url = paging.get('next')
                
                while next_url:
                    async with self.session.get(next_url) as next_response:
                        next_response.raise_for_status()
                        data = await next_response.json()
                        comments_data = data.get('data', [])
                        all_comments_for_post.extend(comments_data)
                        # Update next_url for next iteration
                        paging = data.get('paging', {})
                        next_url = paging.get('next')
            
            return [self._process_comment(comment, post_id) for comment in all_comments_for_post]
        except Exception as e:
            print(f"Error fetching comments for post {post_id}: {e}")
            return []

    async def _fetch_insights_with_metrics(self, post_id: str, metrics: str) -> Optional[Dict]:
        """Helper method to fetch insights with given metrics"""
        url = f'{self.base_url}/{post_id}/insights'
        params = {
            'access_token': self.access_token,
            'metric': metrics
        }
        
        try:
            async with self.session.get(url, params=params) as response:
                response.raise_for_status()
                data = await response.json()
                insights_data = data.get('data', [])
                return self._process_insights(insights_data, post_id)
        except Exception as e:
            raise  # Re-raise the exception to be caught by the caller

    async def fetch_insights_for_post(self, post_id: str, media_type: str) -> Optional[Dict]:
        """Fetch insights for a specific post"""
        if media_type == 'VIDEO':
            try:
                # Try new video metrics
                return await self._fetch_insights_with_metrics(post_id, 'reach,shares,saved,plays,ig_reels_avg_watch_time')
            except:
                try:
                    # Try mid-age video metrics
                    return await self._fetch_insights_with_metrics(post_id, 'impressions,profile_visits,reach,shares,saved')
                except:
                    # For oldest videos
                    metrics = 'impressions,reach,saved'
        else:
            metrics = 'impressions,profile_visits,reach,shares,saved'
        
        try:
            return await self._fetch_insights_with_metrics(post_id, metrics)
        except Exception as e:
            print(f"Error fetching insights for post {post_id}: {e}")
            return None

    def _process_post(self, post: Dict) -> Dict:
        """Process a single post"""
        try:
            post_time = datetime.strptime(post.get('timestamp'), '%Y-%m-%dT%H:%M:%S%z')
            post_time_sg = post_time.astimezone(self.singapore_tz)
            post_timestamp = post_time_sg.strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            print(f"Error parsing post timestamp: {e}")
            post_timestamp = None

        return {
            'post_id': post.get('id'),
            'caption': post.get('caption', ''),
            'media_type': post.get('media_type'),
            'post_timestamp': post_timestamp,
            'post_like_count': post.get('like_count', 0),
            'comments_count': post.get('comments_count', 0),
            'permalink': post.get('permalink'),
            'post_collected_at': datetime.now(self.singapore_tz).strftime('%Y-%m-%d %H:%M:%S')
        }

    def _process_comment(self, comment: Dict, post_id: str) -> Dict:
        """Process a single comment"""
        try:
            comment_time = datetime.strptime(comment.get('timestamp'), '%Y-%m-%dT%H:%M:%S%z')
            comment_time_sg = comment_time.astimezone(self.singapore_tz)
            comment_timestamp = comment_time_sg.strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            print(f"Error parsing comment timestamp: {e}")
            comment_timestamp = None

        return {
            'comment_id': comment.get('id'),
            'postid': post_id,
            'comment_text': comment.get('text', ''),
            'comment_timestamp': comment_timestamp,
            'username': comment.get('from', {}).get('username', ''),
            'comment_like_count': comment.get('like_count', 0),
            'comment_collected_at': datetime.now(self.singapore_tz).strftime('%Y-%m-%d %H:%M:%S')
        }

    def _process_insights(self, insights_data: List[Dict], post_id: str) -> Dict:
        """Process insights data for a post"""
        insights = {
            'post_id': post_id,
            'impressions': None,
            'profile_visits': None,
            'reach': None,
            'shares': None,
            'saved': None,
            'plays': None,
            'ig_reels_avg_watch_time': None,
            'insights_collected_at': datetime.now(self.singapore_tz).strftime('%Y-%m-%d %H:%M:%S')
        }
        
        try:
            for metric in insights_data:
                metric_name = metric.get('name')
                if metric_name in insights:
                    value = metric.get('values', [{}])[0].get('value', None)
                    # Convert milliseconds to seconds for watch time
                    if metric_name == 'ig_reels_avg_watch_time' and value is not None:
                        value = value / 1000
                    insights[metric_name] = value
            
            return insights
            
        except Exception as e:
            print(f"Error processing insights for post {post_id}: {e}")
            return insights
