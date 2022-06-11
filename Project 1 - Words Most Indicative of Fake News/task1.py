import os
import json

articleDirectory = '/course/data/a1/content/HealthStory'
reviewDirectory = '/course/data/a1/reviews/HealthStory.json'
tweetsDirectory = '/course/data/a1/engagements/HealthStory.json'

def task1():
    #Counts number of article files in content/HealthStory folder
    articleCount = len(os.listdir(articleDirectory))
    
    #Counts number of reviews within JSON file in reviews/HealthStory folder
    with open(reviewDirectory) as open_reviews:
        reviews = json.load(open_reviews)
        reviewCount = len(reviews)

    #Counts number of distinct tweets within JSON file in engagements/HealthStory folder
    with open(tweetsDirectory) as open_tweets:
        tweets = json.load(open_tweets)
        listOfTweets = set()
        for article in tweets:
            listOfTweets.update(tweets[article]['tweets'])
            listOfTweets.update(tweets[article]['replies'])
            listOfTweets.update(tweets[article]['retweets'])
    tweetsCount = len(listOfTweets)

    #Create and save JSON output
    jsonOutput = json.dumps({"Total number of articles": articleCount, 
    "Total number of reviews": reviewCount,
    "Total number of tweets": tweetsCount})
    with open("task1.json", "w") as outfile:
        outfile.write(jsonOutput)
    return
