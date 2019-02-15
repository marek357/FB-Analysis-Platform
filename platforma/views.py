from django.shortcuts import render
import os
import json
import operator
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from datetime import datetime, timedelta

#/Users/marekmasiak/Downloads/facebook-marekmasiak2


def getDirectory():
    file = open("dire.txt", "r")
    toReturn = file.read()
    file.close()
    return toReturn


def writeDirectory(directo):
    file = open("dire.txt", "w+")
    file.write(str(directo))
    file.close
    return


def writeDate(datePeriod):
    file = open("date.txt", "w+")
    file.write(str(datePeriod))
    file.close
    return


def getDate(mode):
    file = open("date.txt", "r")
    toReturn = file.read()
    file.close()
    try:
        return int(toReturn)
    except:
        if mode == 0:
            return 'nieograniczony'
        else:
            return int(1000000)


def home(request):
    dire = request.POST.get('directory', '/Users/marekmasiak/Downloads/facebook-marekmasiak2')
    days = request.POST.get('days', 'nieograniczony')
    writeDate(days)
    writeDirectory(dire)

    context = {'postdata': getDirectory(), 'period': getDate(0)}
    return render(request, 'platforma/home.html', context)


def changedir(request):
    context = {}
    return render(request, 'platforma/changedir.html', context)


def adstats(request):
    context = {'tytul': 'Strona domowa'}

    directory = getDirectory()
    try:
        adDataDirectory = directory + '/ads/advertisers_who_uploaded_a_contact_list_with_your_information.json'
        adContent = ""
        temporaryFile = open(adDataDirectory, 'r')
        if temporaryFile.mode == 'r':
            tempContainer = json.loads(temporaryFile.read())
        temporaryFile.close()
        adJSON = json.loads(json.dumps(tempContainer).encode('latin1').decode('utf-8', 'ignore'))

        context = {'dirname': directory, 'tytul': 'Reklamodawcy', 'adv': adJSON['custom_audiences']}
    except FileNotFoundError:
        context = {'dirname': directory, 'tytul': 'Reklamodawcy', 'error': 'Niestety w podanej ścieżce nie znaleziono plików z danymi Facebooka'}

    return render(request, 'platforma/adstats.html', context)


def wordstats(request):
    try:
        directory = getDirectory()
        messagePaths = []
        messageDataDirectory = directory + '/messages/inbox'
        messageData = os.listdir(messageDataDirectory)
    except FileNotFoundError:
        context = {'dirname': directory, 'tytul': 'Statystyki wiadomości', 'error': 'Niestety w podanej ścieżce nie znaleziono plików z danymi Facebooka'}

    for i in range(0, len(messageData)):
        if messageData[i] != '.DS_Store':
            try:
                messagePaths.append(messageDataDirectory + '/' + messageData[i] + '/message.json')
            except:
                pass

    messageContent = []
    words = {}

    for i in messagePaths:
        try:
            temporaryFile = open(i, 'r')
            if temporaryFile.mode == 'r':
                tempContainer = json.loads(temporaryFile.read())
                messageContent.append(json.loads(json.dumps(tempContainer).encode('latin1').decode('utf-8')))
            temporaryFile.close()
        except:
            pass

    for i in range(0, len(messageContent)):
        try:
            for a in messageContent[i]['messages']:
                a['content'] = str(a['content']).encode('latin1').decode('utf-8', 'ignore')
                tokenizer = RegexpTokenizer(r'\w+')

                for x in tokenizer.tokenize(a['content']):
                    if x not in words:
                        words[x] = 1
                    else:
                        words[x] += 1
        except:
            pass

    words = sorted(words.items(), key=operator.itemgetter(1), reverse=True)
    wordList = []
    wordDict = {}
    wordKeys = []
    wordItems = []
    for i in range(0, 50):
        wordList.append(words[i][0] + ' (' + str(words[i][1]) + ')')
        wordDict[words[i][0]] = words[i][1]
        wordKeys.append(words[i][0])
        wordItems.append(words[i][1])

    context = {'tytul': 'Strona domowa', 'words': wordList, 'data': wordDict, 'pic': '/stat.png'}

    return render(request, 'platforma/wordstats.html', context)


def messagestats(request):
    try:
        directory = getDirectory()

        messagePaths = []
        messageDataDirectory = directory + '/messages/inbox'
        messageData = os.listdir(messageDataDirectory)
    except FileNotFoundError:
        context = {'dirname': directory, 'tytul': 'Reklamodawcy', 'error': 'Niestety w podanej ścieżce nie znaleziono plików z danymi Facebooka'}

    for i in range(0, len(messageData)):
        if messageData[i] != '.DS_Store':
            try:
                messagePaths.append(messageDataDirectory + '/' + messageData[i] + '/message.json')
            except:
                pass

    messageContent = []
    messageCount = {}
    for i in messagePaths:
        try:
            temporaryFile = open(i, 'r')
            if temporaryFile.mode == 'r':
                messageContent.append(json.loads(temporaryFile.read()))
            temporaryFile.close()
        except:
            pass

    averageNumberOfMessages = 0

    for i in range(0, len(messageContent)):
        messageCount[i] = len(messageContent[i]['messages'])
        averageNumberOfMessages += messageCount[i]
    messageCount = sorted(messageCount.items(), key=operator.itemgetter(1), reverse=True)

    averageNumberOfMessages /= len(messageContent)

    for i in range(0, len(messageContent)):
        for a in messageContent[i]['messages']:
            a['timestamp_ms'] = str(datetime.fromtimestamp(int(a['timestamp_ms']) / 1000).strftime('%Y-%m-%d %H:%M:%S.%f'))

    numberOfGroupChats = 1
    ppl = []
    for i in range(0, len(messageContent)):
        if len(messageContent[messageCount[i][0]]['participants']) <= 2:
            ppl.append(str(str(messageContent[messageCount[i][0]]['participants'][0]['name']).encode('latin1').decode('utf-8') + '(' + str(messageCount[i][1]) + ')'))
        else:
            numberOfGroupChats += 1

    """
    ZADANIE 2
    """
    pplLP = []
    avgValue = 0
    lastMonthMessages = {}

    try:
        print(int(getDate(1)))
        aMonthAgo = datetime.now() - timedelta(days=getDate(1))
    except:
        aMonthAgo = datetime.now() - timedelta(days=100000)

    numberOfGroupChats = 1
    for i in range(0, len(messageContent)):
        if len(messageContent[i]['participants']) <= 2:
            lastMonthMessages[str(messageContent[i]['participants'][0]['name']).encode('latin1').decode('utf-8')] = 0
        else:
            lastMonthMessages[str('Czat Grupowy ' + str(numberOfGroupChats))] = 0
            numberOfGroupChats += 1

    numberOfGroupChats = 1
    for i in range(0, len(messageContent)):
        if len(messageContent[i]['participants']) <= 2:
            for a in messageContent[i]['messages']:
                if datetime.strptime(a['timestamp_ms'], '%Y-%m-%d %H:%M:%S.%f') >= aMonthAgo:
                    lastMonthMessages[str(messageContent[i]['participants'][0]['name']).encode('latin1').decode('utf-8')] += 1
                    avgValue += 1
        else:
            for a in messageContent[i]['messages']:
                if datetime.strptime(a['timestamp_ms'], '%Y-%m-%d %H:%M:%S.%f') >= aMonthAgo:
                    avgValue += 1
            numberOfGroupChats += 1

    realPeople = {}
    for i in lastMonthMessages:
        if lastMonthMessages[i] != 0:
            realPeople[i] = lastMonthMessages[i]
    try:
        avgValue /= len(realPeople)
    except:
        avgValue = 0
    realPeople = sorted(realPeople.items(), key=operator.itemgetter(1), reverse=True)
    avglpnb = float("{0:.1f}".format(avgValue))
    for i in range(0, len(realPeople)):
        pplLP.append(str(realPeople[i][0] + ' (' + str(realPeople[i][1]) + ')'))

    print('Średnia ilość wiadomości to: ' + str(avgValue))
    avgnb = float("{0:.1f}".format(averageNumberOfMessages))
    aver = float("{0:.1f}".format(avgValue))
    context = {'dirname': directory, 'tytul': 'Strona Domowa', 'range': range(13), 'nr': numberOfGroupChats, 'avgmsg': avgnb, 'ppl': ppl, 'pplLP': pplLP, 'avgLP': aver}

    return render(request, 'platforma/messagestats.html', context)


def about(request):
    context = {'tytul': 'o nas'}
    return render(request, 'platforma/about.html', context)
