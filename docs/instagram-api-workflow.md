# Instagram API Workflow

Here, I lay out some the fields obtained for each post, comment and insight. I also describe my handling of the insights endpoint, which requires additional care than the posts and insights endpoints. fields with an asterisk are transformed / added fields.

> NOTE: Each post has only 1 insight. However, each post can have 0, 1, or multiple comments. This job also **does not** collect replies to comments, which has a [separate endpoint and syntax altogether](https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-comment/replies/).

***

`posts`

| **field**          | **description**                     | 
| ------------------ | ----------------------------------- |
| id                 | post id                             |
| caption            | the post's caption                  |
| media_type         | `IMAGE`, `VIDEO`, `CAROUSELL_ALBUM` |
| timestamp          | time post was created               |
| like_count         | number of likes                     |
| comments_count     | number of comments                  |
| permalink          | web url of ig post                  |
| post_collected_at* | time our job retrieves the post     |

`comments`

| **field**             | **description**                    | 
| --------------------- | ---------------------------------- |
| id                    | comment id                         |
| post_id*              | id of post the comment is under    |
| text                  | the comment's text                 |
| timestamp             | time comment was created           |
| from                  | number of comments                 |
| like_count            | number of likes                    |
| comment_collected_at* | time our job retrieves the comment |

`insights`

| **field**               | **description**                         | **applies to which media type**   |
| ----------------------- | --------------------------------------- | --------------------------------- |
| post_id*                | id of post the insight is under         | all                               |
| impressions             | total no. of times post has been seen   | all except new `VIDEO`            |
| profile_visits          | no. of profile visits after seeing post | all except new and oldest `VIDEO` |
| reach                   | no.of unique views                      | all                               |
| shares                  | no. of shares                           | all except oldest `VIDEO`         |
| saved                   | no. of saves                            | all                               |
| plays                   | no. of times vid plays                  | new `VIDEO` only                  |
| ig_reels_avg_watch_time | avg time spent playing the video        | new `VIDEO` only                  |
| insight_collected_at*   | time our job retrieves the insight      | all                               |

***

### Handling Video Insights Fallbacks

As in the above `insights` table, I have added a visual column `applies to which media type` just for better understanding. Here we see that the `VIDEO` media type requires multiple fallback attempts due to Instagram's evolving API. In the code block (below), the function first requests the latest available metrics, including `ig_reels_avg_watch_time` and `plays`. If the API does not support these, it retries with an older set of metrics, dropping the 2 above for `impressions` and `profile_visits` instead. If that also fails, it falls back to the most basic metrics (`impressions`, `reach`, `saved`). This ensures maximum data retrieval while handling API inconsistencies gracefully.

```python
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
```

> NOTE: the `IMAGE` and `CAROUSELL_ALBUM` media types do not suffer from these issues.
