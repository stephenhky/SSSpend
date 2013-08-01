# -*- coding: utf-8 -*-
"""
Created on Mon May 13 09:59:23 2013

@author: hok1
"""

import numpy as np
from functools import partial
import sys

fileHeader = ['date', 'place', 'category', 'city', 'debit', 'comment',
              'individual', 'paymentmethod']
colType = ['S10', 'S100', 'S30', 'S50', 'S15', 'S100', 'S10', 'S50']
debitLoc = fileHeader.index('debit')
categoryLoc = fileHeader.index('category')
individualLoc = fileHeader.index('individual')
paymentmethodLoc = fileHeader.index('paymentmethod')

class FileSSSpending:
    def __init__(self, filename):
        # count number of empty lines at the end of the file
        numEmptyLines = 0        
        for line in open(filename):
            splitwords = line.rstrip('\n').split('\t')
            elementNotEmpty = set(splitwords) - set(['']).intersection(set(splitwords))
            if len(elementNotEmpty) == 0:
                numEmptyLines += 1
        
        data = np.genfromtxt(filename, delimiter='\t', skip_header=1,
                             skip_footer=numEmptyLines,
                             dtype={'names': tuple(fileHeader),
                                    'formats': tuple(colType)})
        data = list(data)
        for item in data:
            item[debitLoc] = item[debitLoc].replace(',', '').replace('$', '').replace('"', '')
        self.data = data
        
        retSingle = lambda item, loc: item[loc]
        
        self.categories = list(set(map(partial(retSingle, loc=categoryLoc),
                                       data)))
        
    @staticmethod
    def amount(item):
        return float(item[debitLoc])
    
    @staticmethod
    def category(item):
        return item[categoryLoc]
    
    @staticmethod
    def individual(item):
        return item[individualLoc]
    
    @staticmethod
    def paymentmethod(item):
        return item[paymentmethodLoc]
    
    def categorizedSpending(self):
        cateSpending = {}
        for category in self.categories:
            cateSpending[category] = 0.0
        for item in self.data:
            cateSpending[FileSSSpending.category(item)] += FileSSSpending.amount(item)
        
        for category, amount in sorted(cateSpending.items(), 
                                       key=lambda item: item[1], reverse=True):
            print category, ' : ', amount
            
    def individualSpending(self):
        individuals = {}
        for item in self.data:
            name = FileSSSpending.individual(item)
            if name in individuals:
                individuals[name] += FileSSSpending.amount(item)
            else:
                individuals[name] = FileSSSpending.amount(item)
                
        for name, amount in sorted(individuals.items(), 
                                   key=lambda item: item[1], reverse=True):
            print name, ' : ', amount
            
    def sortPaymentMethod(self):
        methods = {}
        for item in self.data:
            method = FileSSSpending.paymentmethod(item)
            if method in methods:
                methods[method] += FileSSSpending.amount(item)
            else:
                methods[method] = FileSSSpending.amount(item)
                
        for method, amount in sorted(methods.items(), 
                                     key=lambda item: item[1], reverse=True):
            print method, ' : ', amount

def help():
    print 'Usage: python SSSpendAnalysis.py <filename>'
        
if __name__ == '__main__':
    argvs = sys.argv
    if len(argvs) == 2:
        filename = argvs[1]        
        
        may2013 = FileSSSpending(filename)
        print '=== Spending of Individuals ==='
        may2013.individualSpending()
        print '=== Spendin Categories ==='
        may2013.categorizedSpending()
        print '=== Payment Methods ==='
        may2013.sortPaymentMethod()
    else:
        help()