import os
import json
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

articleDirectory = '/course/data/a1/content/HealthStory/'

def task3():
    #Initialising list
    articleRows = []

    #For each article, extract publish_date
    for item in os.listdir(articleDirectory):
        with open(articleDirectory + item) as f:
            article = json.load(f)
            if article['publish_date'] != None:
                publishDate = datetime.datetime.fromtimestamp(article['publish_date'])
                articleRows.append([item[:-5], publishDate.year, publishDate.month, publishDate.day])   

    #Create dataframe from lists of article records, sorted by news_id in ascending order        
    outputDf = pd.DataFrame(articleRows, columns=['news_id', 'year', 'month', 'day']).sort_values(by=['news_id'], ascending = True)
    outputDf["month"] = outputDf["month"].map("{:02}".format)
    outputDf["day"] = outputDf["day"].map("{:02}".format)
    
    #Output dataframe as CSV file (Task 3A)
    outputDf.to_csv('task3a.csv', index=False)

    #Produce bar chart of article count of each calendar year (Task 3B)
    x = outputDf['year'].value_counts().sort_index().index.values
    y = outputDf['year'].value_counts().sort_index().values
    fig, ax = plt.subplots()
    ax.bar(x,y)

    #Set dimensions, tick frequency and gridlines
    fig.set_figheight(8)
    fig.set_figwidth(15)
    plt.xticks(np.arange(min(x), max(x)+1, 1.0))
    plt.gca().yaxis.grid(True)
    
    #Set title and x/y labels
    ax.set_xlabel("Calendar Year")
    ax.set_ylabel("Number of Articles")
    ax.set_title("Task 3: Number of Articles In Each Calendar Year")

    #Save plot to file
    plt.savefig('task3b')
    plt.close()
    return

