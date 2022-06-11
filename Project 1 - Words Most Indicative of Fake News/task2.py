import os
import json
import pandas as pd

articleDirectory = '/course/data/a1/content/HealthStory/'
reviewDirectory = '/course/data/a1/reviews/HealthStory.json'

def task2():
    #Initalising list
    articleRows = []
    reviewRows = []

    #For each article, extract news_id and news_title
    for item in os.listdir(articleDirectory):
        with open(articleDirectory + item) as f:
            article = json.load(f)
            articleRows.append([item[0:-5], article['title']])

    #For each review, extract news_id, title, rating and answer for each criteria
    with open(reviewDirectory) as open_reviews:
        reviews = json.load(open_reviews)
        for review in reviews:
            newsId = review['news_id']
            reviewTitle = review['title']
            rating = review['rating']
            numSatisfactory = 0
            for criteria in review['criteria']:
                if criteria['answer'] == 'Satisfactory':
                    numSatisfactory += 1
            reviewRows.append([newsId, reviewTitle, rating, numSatisfactory])
    
    #Create dataframe from lists of article and review records
    newsDf = pd.DataFrame(articleRows, columns=['news_id', 'news_title'])
    reviewsDf = pd.DataFrame(reviewRows, columns=['news_id', 'review_title','rating','num_satisfactory'])

    #newsDf left join reviewsDf on news_id, sort by news_id in ascending order (must contain details of article)
    outputDf = newsDf.merge(reviewsDf, how = 'left', on = 'news_id').sort_values(by=['news_id'], ascending = True)
    
    #Output dataframe as CSV
    outputDf.to_csv('task2.csv', index=False)
    return
