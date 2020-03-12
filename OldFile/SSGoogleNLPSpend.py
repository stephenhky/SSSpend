# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 14:48:37 2013

@author: hok1
"""

from OldFile import SSGoogleNLP as ssnlp, SSGoogleSpend as spend
import sys
from operator import add
from gdata.service import BadAuthentication

class SSFinNLPGoogle(spend.SSFinGoogle):
    def __init__(self, username, password):
        spend.SSFinGoogle.__init__(self, username, password)
        self.normalizer = ssnlp.CategoryNormalizer(username, password)
    
    def getDataFromMonth(self, month):
        data = spend.SSFinGoogle.getDataFromMonth(self, month)
        for item in data:
            item['Category'] = self.normalizer.normalizeCategory(item['Category'])
        return data
    
def help():
    print 'Usage:'
    print '> python SSGoogleNLPSpend.py'
    print '  Display this help message.\n'
    print '> python SSGoogleNLPSpend.py all'
    print '  Display the summary for all months.\n'
    print '> python SSGoogleNLPSpend.py <month> [<month> <month>]'
    print '  Display the summary for all months specified in the argument.'
    
if __name__ == '__main__':
    argvs = sys.argv
    try:
        if len(argvs) >= 2:
            username, password = spend.SSFinGoogleAPI.getLoginInfo()
            ssg = SSFinNLPGoogle(username, password)
            if len(argvs) == 2 and (argvs[1] in ['all', 'All', 'table']):
                months = filter(lambda name: name!='Summary', ssg.sheetsDict.keys())
            else:
                months = argvs[1:]
            analyzers = [spend.SpendDataAnalyzer(ssg.getDataFromMonth(month)) for month in months]
            combinedData = [analyzer.getCategorizedSpending() for analyzer in analyzers]
            if argvs[1] == 'table':
                spend.StatMerger.printTable(combinedData)
            else:
                combinedStat = spend.StatMerger.getMergedStat(combinedData)
                for category, totaldebit in sorted(combinedStat.items(), 
                                                   key=lambda item: item[1], 
                                                   reverse=True):
                    print category, ' : ', totaldebit
                print 'Total Spending = ', reduce(add, combinedStat.values())
        else:
            help()
    except BadAuthentication:
        print 'Incorrect gmail or password.'