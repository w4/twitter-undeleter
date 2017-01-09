from datetime import datetime

from settings import twitter, subreddit
import models

def main():
    """Main entrypoint of the application."""

    # loop over all the users we have been designated to watch
    for user in models.Tracking.select():
        print('Checking {}'.format(user.twitter))

        try:
            # get the user's latest 200 tweets
            tweets = twitter.user_timeline(user_id=user.twitter, count=200,
                                           exclude_replies=False)
            # save them to the database
            save_tweets(tweets, user.twitter)

            # array containing all the ids of the tweets current live on the user's timeline
            tweet_ids = []

            # add the tweets we got above to this list
            tweet_ids.extend([tweet.id_str for tweet in tweets])

            # get the offset for the next loop
            oldest = tweets[-1].id - 1

            while len(tweets) > 0:
                # get the next 200 tweets from the user
                tweets = twitter.user_timeline(user_id=user.twitter, count=200,
                                               max_id=oldest, exclude_replies=False)

                if len(tweets) == 0:
                    # stop looping if we've finished getting all of the user's tweets
                    break

                # save them to the database
                save_tweets(tweets, user.twitter)

                # add the tweets we got to the "live tweets" list
                tweet_ids.extend([tweet.id_str for tweet in tweets])

                # get the new offset for the next loop
                oldest = tweets[-1].id - 1

            Tweet = models.Tweet.alias()
            TweetAlias = models.Tweet.alias()

            # get all the tweets we know about that dont exist in the "live tweets" list
            # we've used a subquery here because we want to limit by 3200 and THEN run the
            # where. not the other way around.
            deleted_tweets = [t.id for t in Tweet.select().where(Tweet.id << (
                TweetAlias.select(TweetAlias.id)
                    .where(TweetAlias.twitter == user.twitter)
                    .order_by(TweetAlias.id.desc())
                    .limit(3200)
            )).where(Tweet.deleted_at == None).where(~(Tweet.id << tweet_ids))]

            if len(deleted_tweets):
                # we've got some deleted tweets! update the entry in our database and
                # tell the world about it.
                models.Tweet.update(deleted_at=datetime.now()).where(models.Tweet.id <<
                                                                   deleted_tweets).execute()

                for id in deleted_tweets:
                    deleted_tweet = models.Tweet.get(id=id)
                    screen_name = models.Tracking.get(models.Tracking.twitter == deleted_tweet.twitter).screen_name

                    print(' Deleted a tweet from {}. {}'.format(
                        screen_name,
                        deleted_tweet.created_at,
                        deleted_tweet.tweet
                    ))

                    submission = subreddit.submit(title='@{} | {} | {}'.format(
                        screen_name,
                        deleted_tweet.created_at,
                        deleted_tweet.tweet
                    ), selftext=deleted_tweet.tweet)

                    twitter.update_status('.@{} has deleted a tweet from {}. {}'.format(
                        screen_name,
                        deleted_tweet.created_at,
                        submission.shortlink
                    ))
        except Exception as e:
            print(str(e))

def save_tweets(tweets, uid):
    for tweet in tweets:
        models.Tweet.create_or_get(id=tweet.id_str, twitter=uid,
                                   tweet=tweet.text.encode("utf-8"),
                                   created_at=tweet.created_at)


if __name__ == '__main__':
    while True:
        main()