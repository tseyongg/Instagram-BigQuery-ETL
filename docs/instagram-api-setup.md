# Instagram API Setup

> **NOTE**: the Meta API endpoints are notorious for being hard to handle. In addition, they are constantly updated and changed with time, so additional handling is needed to manoeuvre around. Here, I referred to Meta API documentations and certain StackOverflow threads to implement workarounds and solutions.

These are the steps (albeit lengthy), but required by Meta, to generate an access token. An access token is needed to query the Instagram API, to get data from your Instagram Business Account. I originally used the newly created [Instagram API with Instagram Login](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login), but later on, because I needed insights, I switched to the [Instagram API with Facebook Login](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-facebook-login).

Disclaimer: I began working on this project on Nov 2024. As of Feb 2025, whilst documenting this markdown, I just checked the Instagram API with Instagram Login now allows insights. Back then, the Instagram API with Instagram Login was still an extremely new concept, having been introduced in [Aug 2024](https://developers.facebook.com/blog/post/2024/07/30/instagram-api-with-instagram-login/). I am proud to say I was one of the first to use it!

## Meta App Creation

The first steps needed are to ensure that you have:

1. An Instagram Business Account
2. A Facebook Page connected to the same Instagram Business Account
3. A Facebook Developer Account given admin priviledges by the above Facebook Page
4. Created a Meta app on the [Meta Developer Platform](https://developers.facebook.com/docs/development/create-an-app), using the same Facebook Developer Account

This is what you should see with your Meta App up:

![meta-app-overview](/docs/images/meta-app-overview.png)

Ensure your app is set to **Live** mode, otherwise you [would not be able to retrieve any data later on](https://stackoverflow.com/questions/78792152/the-instagram-api-is-returning-no-comments-data-for-the-specified-post).

Next, create a configuration. In our case, we desire posts, comments and insights, thus we need these six [permissions](https://developers.facebook.com/docs/permissions/):

![meta-app-config](/docs/images/meta-app-config.png)

## Get an Access Token

Now, head over to [Graph API Explorer](https://developers.facebook.com/tools/explorer/) to generate an access token:

![gen-token](/docs/images/gen-token.png)

Then, complete the Facebook Login modal that pops up.

# Exchange for Long-Lived Token

In the previous step, we obtained a short-term access token (valid only for about 1-2 hours). Now we have to exchange it for a [long-lived token](https://developers.facebook.com/docs/facebook-login/guides/access-tokens/get-long-lived/) (valid for 60 days).

Using your App ID and App Secret under Basic App Settings:

![app-id-secret](/docs/images/app-id-secret.png)

Then proceed to run the follwing command in your terminal:

```bash
curl -i -X GET "https://graph.facebook.com/{graph-api-version}/oauth/access_token?  
    grant_type=fb_exchange_token&          
    client_id={app-id}&
    client_secret={app-secret}&
    fb_exchange_token={your-access-token}"
```

After that, store the long-lived token safely.

## Debugging

To debug your access token, you may do so [here](https://developers.facebook.com/tools/debug/accesstoken/).

Below is an example of the status of my own long-lived saccess token:

![access-token-info](/docs/images/access-token-info.png)


***

[Previous Step](/README.md) | [Next Step](/docs/instagram-api-workflow.md)