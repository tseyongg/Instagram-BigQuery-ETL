# Final Results

Here, with successsful [Cloud Run](/docs/cloud-deployment.md) and [Composer](/docs/airflow-integration.md) deployments, you will be able to see the loaded tables in [BigQuery](https://cloud.google.com/bigquery/docs/introduction). I display mine, here, in order of load:

## BigQuery Tables

`posts`

- Schema:

![posts-schema](/docs/images/posts-schema.png)

- Data:

![posts-preview](/docs/images/posts-preview.png) <br><br>

`comments`

- Schema:

![comments-schema](/docs/images/comments-schema.png)

- Data:

![comments-preview](/docs/images/comments-preview.png) <br><br>

`insights`

- Schema:

![insights-schema](/docs/images/insights-schema.png)

- Data:

![insights-preview](/docs/images/insights-preview.png)

## Data Analysis

The tables are joinable on 

```sql
posts.post_id = comments.postid = insights.post_id
```

For example, we can conduct analysis on recent comments linked to their parent posts:

```sql
SELECT *
FROM `winged-yeti-440908-r9.instagram_analytics.posts` p
LEFT JOIN `winged-yeti-440908-r9.instagram_analytics.comments` c
    ON p.post_id = c.postid
ORDER BY p.post_timestamp DESC;
```

Result:

![joined-post-comments](/docs/images/joined-post-comments.png) <br><br>

Or, we may want to conduct analysis on post insights:

```sql
SELECT *
FROM `winged-yeti-440908-r9.instagram_analytics.posts` p
LEFT JOIN `winged-yeti-440908-r9.instagram_analytics.insights` i
    ON p.post_id = i.post_id
ORDER BY p.post_timestamp DESC;
```

Result:

![joined-post-insights](/docs/images/joined-post-insights.png)

***

[Previous Step](/docs/airflow-integration.md)