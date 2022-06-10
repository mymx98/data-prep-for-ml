import os
import json
import pandas as pd
import matplotlib.pyplot as plt

reviewDirectory = '/course/data/a1/reviews/HealthStory.json'

def task4():
    #Initialising list
    reviewRows = []

    #For each review, extract news_id, news_source and rating
    with open(reviewDirectory) as f:
        reviews = json.load(f)
        for review in reviews:
            newsId = review['news_id'][-5:]
            newsSource = review['news_source']
            rating = review['rating']
            if newsSource != None:
                reviewRows.append([newsId, newsSource, rating])

    #Create dataframe from list of review records, sorted by news_id in ascending order
    reviewDf = pd.DataFrame(reviewRows, columns=['news_id', 'news_source', 'rating']).sort_values(by=['news_id'], ascending = True)

    #Generate count and mean values for each news_source category
    newsSourceCountDf = reviewDf.groupby(by=['news_source']).count()
    newsSourceAverageDf = reviewDf.groupby(by=['news_source']).mean()
    
    #Left join count and average dataframes on news_source
    outputDf = pd.merge(newsSourceCountDf, newsSourceAverageDf, how = 'left', on = ['news_source']).drop(columns=['news_id'])
    outputDf.columns = ['num_articles', 'avg_rating']

    #Exclude articles with blank news_source
    outputDf = outputDf[outputDf.index != '']
    
    #Output dataframe as CSV file (Task 4A)
    outputDf.to_csv('task4a.csv')

    #Filter dataframe where number of articles is at least 5
    outputFilteredDf = outputDf[outputDf['num_articles'] >= 5].sort_values(by=['avg_rating'], ascending = True)
    
    #Create horizontal bar plot
    x = outputFilteredDf.index.tolist()
    y = outputFilteredDf['avg_rating']
    fig, ax = plt.subplots()
    ax.bar(x,y)

    #Set dimensions, x-axis limits and gridlines
    fig.set_figheight(12)
    fig.set_figwidth(18)
    ax.set_xticks(x)
    ax.set_xticklabels(x, rotation=25, ha="right")
    plt.gca().yaxis.grid(True)
    
    #Set title and x/y labels
    ax.set_title("Task 4B: Average Rating of Each News Source")
    ax.set_xlabel("News Source")
    ax.set_ylabel("Average Rating")
    
    #Save plot to file
    plt.savefig('task4b')
    plt.close()
    return
