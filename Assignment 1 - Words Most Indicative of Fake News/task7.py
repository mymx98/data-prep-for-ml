import os
import json
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import time

articleDirectory = '/course/data/a1/content/HealthStory'
reviewDirectory = '/course/data/a1/reviews/HealthStory.json'

def task7():
    #Word dictionary from Task 6
    with open('task6.json') as f:
        wordDict = json.load(f)
    
    #Initalising list
    reviewRating = {} #Dictionary containing rating for every article
    outputRows = []

    #For each review, extract news_id and rating
    with open(reviewDirectory) as f:
        reviews = json.load(f)
        for review in reviews:
            rating = review['rating']
            newsId = review['news_id']
            reviewRating[newsId] = rating
 
    #Number of real and fake articles based on rating (less than 3 if fake)
    numRealArticles = len([article[0:-5] for article in os.listdir(articleDirectory) if reviewRating[article[0:-5]] >= 3])
    numFakeArticles = len([article[0:-5] for article in os.listdir(articleDirectory) if reviewRating[article[0:-5]] < 3])

    #For each word in dictionary, calculate odds ratio and log odds ratio
    for word in wordDict:
        wordOddsRatio = oddsRatio(word, wordDict, numRealArticles, numFakeArticles, reviewRating)
        #Check that word did not have zero real or fake articles and has odds ratio between 0 and 1
        if wordOddsRatio is not None:
            wordLogOddsRatio = round(math.log10(wordOddsRatio), 5)
            outputRows.append([word, wordLogOddsRatio, wordOddsRatio])

    #Create dataframe from list of word-odds ratio records, sorted by log_odds_ratio in ascending order
    outputDf = pd.DataFrame(outputRows,columns=['word','log_odds_ratio','odds_ratio']).sort_values(by=['log_odds_ratio'],ascending=True)

    #Save output as CSV, sorted alphabetically (Task 7a)
    outputDf.drop('odds_ratio', axis=1).sort_values(by=['word'], ascending=True).to_csv('task7a.csv', index=False)
    

    #Create boxplot of log odds ratios distribution for all words (Task 7b)
    data = outputDf['log_odds_ratio']
    plt.boxplot(data)

    #Set tick limit and interval, x/y labels, title and gridlines
    plt.xlabel("All Words")
    plt.ylabel("Log Odds Ratio")
    plt.title("Task 7B: Log Odds Ratio Distribution of All Words")
    plt.gca().yaxis.grid(True)
    
    #Save graph as PNG
    plt.savefig('task7b')
    plt.close()
    
    #Best 15 and worst 15 words via bar graph (Task 7c)
    outputFilteredDf = pd.concat([outputDf.head(15),outputDf.tail(15)])
    x = outputFilteredDf['word']
    y = outputFilteredDf['odds_ratio']
    fig, ax = plt.subplots()
    ax.barh(x,y)
    
    #Set size, x/y labels, title and gridlines
    fig.set_figheight(8)
    fig.set_figwidth(15)
    ax.set_xlabel("Odds Ratio")
    ax.set_ylabel("Word")
    ax.set_title("Task 7C: Top 15 Words With Highest/Lowest Odds Ratios")
    plt.gca().xaxis.grid(True)

    #Save graph as PNG
    plt.savefig('task7c')
    plt.close()
    return 

def oddsRatio(word, wordDict, numRealArticles, numFakeArticles, reviewRating):
    #Number of real and fake articles based on rating given word appears
    #For each word in dictionary, search for the article's review rating and store if less than or equal/greater than 3
    numRealArticlesContainingWord = len([reviewRating[article] for article in wordDict[word] if reviewRating[article] >= 3])
    numFakeArticlesContainingWord = len([reviewRating[article] for article in wordDict[word] if reviewRating[article] < 3])

    #Total number of articles and total number of articles containing word
    numArticles = numRealArticles + numFakeArticles
    numArticlesContainingWord = numRealArticlesContainingWord + numFakeArticlesContainingWord

    #To avoid divide by zero error and exclude words that appear in fewer than 10 articles or appear in all articles
    if numRealArticles != 0 and numFakeArticles != 0 and numArticlesContainingWord >= 10 and numArticlesContainingWord < numArticles:
        #Calculate probability word appears in real/fake article
        probWordAppearsReal = numRealArticlesContainingWord/numRealArticles
        probWordAppearsFake = numFakeArticlesContainingWord/numFakeArticles
        #To avoid odds of 0 and infinity
        if (0 < probWordAppearsReal < 1) and (0 < probWordAppearsFake < 1):    
            #Calculate odds words appears in real/fake article
            oddsReal = probWordAppearsReal/(1 - probWordAppearsReal)
            oddsFake = probWordAppearsFake/(1 - probWordAppearsFake)
            return oddsFake/oddsReal
        else:
            return
    else:
        return

