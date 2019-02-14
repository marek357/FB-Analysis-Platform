#!/usr/bin/env python
import os
import json
import operator
import pandas as ps
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime, timedelta
from nltk.tokenize import word_tokenize
directory = '/Users/marekmasiak/Downloads/facebook-marekmasiak2'
messagePaths = []
data = os.listdir(directory)
messageDataDirectory = directory + '/messages/inbox'
messageData = os.listdir(messageDataDirectory)

for i in range(0, len(messageData)):
    if messageData[i] != '.DS_Store':
        messagePaths.append(messageDataDirectory + '/' + messageData[i] + '/message.json')

"""
Kod zbiera zawartosci poszczegolnych plikow
zawierajace wiadomosci
"""
messageContent = []
words = {}

for i in messagePaths:
    temporaryFile = open(i, 'r')
    if temporaryFile.mode == 'r':
        tempContainer = json.loads(temporaryFile.read())
        messageContent.append(json.loads(json.dumps(tempContainer).encode('latin1').decode('utf-8')))
    temporaryFile.close()

"""
Kod robi statystyki 100 najczesciej uzywanych slow
"""

for i in range(0, len(messageContent)):
    for a in messageContent[i]['messages']:
        a['content'] = str(a['content']).encode('latin1').decode('utf-8', 'ignore')
        for x in word_tokenize(a['content']):
            if x not in words:
                words[x] = 1
            else:
                words[x] += 1

words = sorted(words.items(), key=operator.itemgetter(1), reverse=True)
wordList = []
wordDict = {}
wordKeys = []
wordItems = []
for i in range(0, 100):
    wordList.append(words[i][0] + ' (' + str(words[i][1]) + ')')
    wordDict[words[i][0]] = words[i][1]
for i in range(0, 20):
    wordKeys.append(words[i][0])
    wordItems.append(words[i][1])
fig1, ax1 = plt.subplots()
ax1.pie(wordItems, labels=wordKeys, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.show()
# plt.xlabel('Słowo')
# plt.ylabel('Liczba wystąpień')
plt.savefig('/Users/marekmasiak/Desktop/stat.png')
# plt.show()
