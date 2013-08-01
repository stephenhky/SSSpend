# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 15:34:46 2013

@author: hok1
"""

import SSGoogleSpend as ssgs
from nltk.stem import PorterStemmer
from nltk import pos_tag

#################### Data Wrangling Functions ###################
stemmer = PorterStemmer()

class DataCollector:
    @staticmethod
    def readCSVDefFile(inFile):
        csvdef = {}
        inff = open(inFile, 'rb')
        for line in inff.readlines()[1:]:
            item = line.strip().split(',')
            csvdef[item[0]] = item[1].lstrip('"').strip()
        inff.close()
        return csvdef

    @staticmethod    
    def getSSSpendData(username=None, password=None):
        if username==None or password==None:
            username, password = ssgs.SSFinGoogleAPI.getLoginInfo()
        ssg = ssgs.SSFinGoogle(username, password)
        months = filter(lambda name: name!='Summary', ssg.sheetsDict.keys())
        analyzers = [ssgs.SpendDataAnalyzer(ssg.getDataFromMonth(month)) for month in months]
        combinedData = [analyzer.getCategorizedSpending() for analyzer in analyzers]
        return combinedData

    @staticmethod        
    def getRawCategories(combinedData):
        categories = set([])
        for data in combinedData:
            categories = categories.union(data.keys())
        return list(categories)

    @staticmethod        
    def stemWords(words):
        wordList = words.lower().split(' ')
        stemmedWordList = []
        for word in wordList:
            stemmedWordList.append(stemmer.stem(word))
        return ' '.join(stemmedWordList)

    @staticmethod        
    def stemmedDictCategories(categories):
        stemmedDict = {}
        for category in categories:
            stemmedCategory = DataCollector.stemWords(category)
            if stemmedCategory in stemmedDict:
                stemmedDict[stemmedCategory] += [category]
            else:
                stemmedDict[stemmedCategory] = [category]
        return stemmedDict

#################### Getting Data ########################

class WordsChooser:
    @staticmethod
    def chooseBestCategory(wordList):
        if len(wordList) == 1:
            return wordList[0]
        else:
            scores = [0.0] * len(wordList)
            parts_of_speech = pos_tag(wordList)
            # Rule 1: prefer '-ing' ending (gerund)
            for i in range(len(wordList)):
                scores[i] += 1 if parts_of_speech[i]=='VBG' else 0
            # Rule 2: prefer capitalized start
            for i in range(len(wordList)):
                tokens = wordList[i].split(' ')
                if reduce(lambda a, b: a and b,
                          map(lambda word: word[0].isupper(), tokens)):
                    scores[i] += 1
            # Rule 3: prefer singular
            for i in range(len(wordList)):
                scores[i] += 1 if parts_of_speech[i]=='NN' or parts_of_speech[i]=='NNP' else 0
            maxPos = scores.index(max(scores))
            return wordList[maxPos]

class CategoryNormalizer:
    def __init__(self, username, password):
        self.categoryCrosswalk = DataCollector.readCSVDefFile('SSSpendCatCrosswalk.csv')
        self.combinedData = DataCollector.getSSSpendData(username, password)
        self.stemDict = DataCollector.stemmedDictCategories(DataCollector.getRawCategories(self.combinedData))
    
    def normalizeCategory(self, category):
        # remove the period at the end
        category = category.rstrip('.')
        stemmedCategory = DataCollector.stemWords(category)
        if self.categoryCrosswalk.has_key(stemmedCategory):
            stemmedCategory = self.categoryCrosswalk[stemmedCategory]
        if self.stemDict.has_key(stemmedCategory):
            unstemmedCategories = self.stemDict[stemmedCategory]
            return WordsChooser.chooseBestCategory(unstemmedCategories)
        else:
            return category
            
    
if __name__ == '__main__':
    user_gmail, user_password = ssgs.SSFinGoogleAPI.getLoginInfo()
    
    normalizer = CategoryNormalizer(user_gmail, user_password)
    categories = DataCollector.getRawCategories(normalizer.combinedData)
    for category in categories:
        print category, ' : ', normalizer.normalizeCategory(category)