import os
import json
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import OrderedDict

articleDirectory = '/course/data/a1/content/HealthStory/'
stopWords = set(stopwords.words('english'))

#Supporting text prepocessing functions
def convertNonAlphabetic(text):
    return re.sub(r'[^a-zA-Z\s]'," ",text)

def convertSpacingToSingleSpace(text):
    return re.sub(r'\s+', " ", text)

def removeStopWords(listWords, stopWords):
    return [word for word in listWords if not word in stopWords]

def removeSingleCharacter(listWords):
    return [word for word in listWords if not len(word) == 1]

def task6():
    #For each article, extract text, apply preprocessing steps and save output as row
    dictOfWords = {}
    for item in os.listdir(articleDirectory):
        with open(articleDirectory + item) as f:
            article = json.load(f)
            text = article['text']
            text = convertNonAlphabetic(text)
            text = convertSpacingToSingleSpace(text)
            text = text.lower()
            text = text.split()
            text = removeStopWords(text, stopWords)
            text = removeSingleCharacter(text)
            for word in set(text):
                if word in dictOfWords:
                    dictOfWords[word] += [item[:-5]]
                    dictOfWords[word].sort()
                else:
                    dictOfWords[word] = [item[:-5]]
    
    #Saves dictionary as JSON output and sort key by alphabetical order
    jsonOutput = json.dumps(dictOfWords,sort_keys=True)
    with open("task6.json","w") as outfile:
        outfile.write(jsonOutput)
    return
