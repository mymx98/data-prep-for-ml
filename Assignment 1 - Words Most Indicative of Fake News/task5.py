import os
import json
import pandas as pd
import matplotlib.pyplot as plt

articleDirectory = '/course/data/a1/content/HealthStory'
reviewDirectory = '/course/data/a1/reviews/HealthStory.json'
tweetsDirectory = '/course/data/a1/engagements/HealthStory.json'

def task5():
    #Initialising lists
    reviewRows = []
    tweetRows = []
    
    #For each review, extract news_id and rating
    with open(reviewDirectory) as f:
        reviews = json.load(f)
        for review in reviews:
            newsId = review['news_id']
            rating = review['rating']
            reviewRows.append([newsId, rating])

    #For each article, add the count of tweets, retweets, replies(no duplicates)
    with open(tweetsDirectory) as f:
        tweets = json.load(f)
        for article in tweets:
            numTweets = len(set(tweets[article]['tweets'] + tweets[article]['replies'] + tweets[article]['retweets']))
            tweetRows.append([article, numTweets])
    
    #Create dataframe from lists of review and tweet records
    reviewDf = pd.DataFrame(reviewRows, columns=['news_id','rating'])
    tweetDf = pd.DataFrame(tweetRows, columns=['news_id', 'num_tweets'])

    #Left join review and tweet dataframes on news_id, then obtain the average number of tweets for each rating class
    outputDf = pd.merge(reviewDf, tweetDf, how = 'left', on = ['news_id']).groupby(by=['rating']).mean()

    #Create bar chart of average number of tweets for each rating class
    x = outputDf.index
    y = outputDf['num_tweets']
    plt.bar(x, y)

    #Set title, x/y labels and gridlines
    plt.xlabel("Rating")
    plt.ylabel("Average Number of Tweets")
    plt.title("Task 5: Average Number of Tweets for Each Article-Rating Group")
    plt.gca().yaxis.grid(True)

    #Save graph
    plt.savefig('task5')
    plt.close()
    return
