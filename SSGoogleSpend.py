# -*- coding: utf-8 -*-
"""
Created on Fri May 31 14:15:57 2013

@author: hok1
"""

from google_spreadsheet.api import SpreadsheetAPI
import getpass
from gdata.service import BadAuthentication
from operator import add
import sys
import csv

SSSpendingID = 't-cP5RjsrrdhW6qxupaT_xg'

month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
               'Sep', 'Oct', 'Nov', 'Dec']

class SSFinGoogleAPI:
    @staticmethod
    def getLoginInfo():
        user_gmail = raw_input('You Gmail address? ')
        user_password = getpass.getpass('Your Gmail password? ')
        return user_gmail, user_password
        
    @staticmethod
    def getWorksheetsDict(worksheets):
        worksheetDict = {}
        for name, code in worksheets:
            worksheetDict[name] = code
        return worksheetDict

    @staticmethod        
    def currencyStrToFloat(currencyStr):
        curStr = currencyStr.replace(',', '').replace('$', '').replace('"', '')
        return float(curStr)

    @staticmethod        
    def wrapRowsData(rows):
        headerRow = rows[0]
        headerDict = {}
        for rowCode in headerRow:
            headerDict[headerRow[rowCode]] = rowCode
            
        data = []
        for row in rows[1:]:
            item = {}
            debit = SSFinGoogleAPI.currencyStrToFloat(row[headerDict['Debit']])
            for name in headerDict:
                if headerDict[name] in row:
                    item[name] = debit if name=='Debit' else row[headerDict[name]]
            data.append(item)    
        return data
        
class SSFinGoogle:
    def __init__(self, username, password):
        self.api = SpreadsheetAPI(username, password, '')
        worksheets = self.api.list_worksheets(SSSpendingID)
        self.sheetsDict = SSFinGoogleAPI.getWorksheetsDict(worksheets)
        
    def getDataFromMonth(self, month):
        sheet = self.api.get_worksheet(SSSpendingID,
                                       self.sheetsDict[month])
        rows = sheet.get_rows()
        return SSFinGoogleAPI.wrapRowsData(rows)
        
class SpendDataAnalyzer:
    def __init__(self, data):
        self.data = data
        
    def getTotalSpending(self):
        return reduce(add, map(lambda item: item['Debit'], self.data))
        
    def getFilteredData(self, filter_criterion):
        return filter(filter_criterion, self.data)
        
    def getCategorizedColumnSpending(self, column):
        catSpending = {}
        for category in set(map(lambda item: item[column], self.data)):
            catSpending[category] = reduce(add,
                                           map(lambda item: item['Debit'],
                                               self.getFilteredData(lambda item: item[column]==category)))
        return catSpending        
    
    def getCategorizedSpending(self):
        return self.getCategorizedColumnSpending('Category')
    
    def getIndividualSpending(self):
        return self.getCategorizedColumnSpending('Individual')

class StatMerger:
    @staticmethod
    def getMergedStat(datastats):
        categories = set([])
        for data in datastats:
            categories = categories.union(data.keys())
        
        mergedStat = {}
        for category in categories:
            getDebit = lambda item: item[category] if category in item else 0
            mergedStat[category] = reduce(add, map(getDebit, datastats))
        return mergedStat
        
    @staticmethod
    def mergeTable(datastats):
        mergedStat = StatMerger.getMergedStat(datastats)
        categories = map(lambda item: item[0], mergedStat.items())
                                
        merged_table = {}
        for category in categories:
            spendDict = {}
            for month_idx in range(len(datastats)):
                if datastats[month_idx].has_key(category):
                    spendDict[month_names[month_idx]] = datastats[month_idx][category]
            merged_table[category] = spendDict
        
        return merged_table
        
    @staticmethod
    def printTable(datastats):
        outf = open('SSSpendsummary.csv', 'wb')
        writer = csv.writer(outf, delimiter=',')
        
        combinedStat = StatMerger.getMergedStat(datastats)
        merged_table = StatMerger.mergeTable(datastats)
        #print '\t\t', '\t'.join(month_names[:len(datastats)])
        writer.writerow(['']+month_names[:len(datastats)])
        for category in map(lambda item: item[0],
                            sorted(combinedStat.items(), 
                                   key=lambda item: item[1], 
                                   reverse=True)):
            #rowToPrint = category + '\t\t'
            rowToWrite = [category]
            for month_name in month_names[:len(datastats)]:
                if merged_table[category].has_key(month_name):
                    #rowToPrint += str(merged_table[category][month_name]) + '\t'
                    rowToWrite.append(merged_table[category][month_name])
                else:
                    #rowToPrint += '0\t'
                    rowToWrite.append(0)
            #print rowToPrint
            writer.writerow(rowToWrite)
        
        outf.close()

def help():
    print 'Usage:'
    print '> python SSGoogleSpend.py'
    print '  Display this help message.\n'
    print '> python SSGoogleSpend.py all'
    print '  Display the summary for all months.\n'
    print '> python SSGoogleSpend.py <month> [<month> <month>]'
    print '  Display the summary for all months specified in the argument.'
    
if __name__ == '__main__':
    argvs = sys.argv
    try:
        if len(argvs) >= 2:
            username, password = SSFinGoogleAPI.getLoginInfo()
            ssg = SSFinGoogle(username, password)
            if len(argvs) == 2 and (argvs[1] in ['all', 'All', 'table']):
                months = filter(lambda name: name!='Summary', ssg.sheetsDict.keys())
            else:
                months = argvs[1:]
            analyzers = [SpendDataAnalyzer(ssg.getDataFromMonth(month)) for month in months]
            combinedData = [analyzer.getCategorizedSpending() for analyzer in analyzers]
            if argvs[1] == 'table':
                StatMerger.printTable(combinedData)
            else:
                combinedStat = StatMerger.getMergedStat(combinedData)
                for category, totaldebit in sorted(combinedStat.items(), 
                                                   key=lambda item: item[1], 
                                                   reverse=True):
                    print category, ' : ', totaldebit
                print 'Total Spending = ', reduce(add, combinedStat.values())
        else:
            help()
    except BadAuthentication:
        print 'Incorrect gmail or password.'