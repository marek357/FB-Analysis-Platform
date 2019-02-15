from django.shortcuts import render
import os
import json
import operator
from nltk.tokenize import word_tokenize

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


def home(request):
    dire = request.POST.get('directory', '/Users/marekmasiak/Downloads/facebook-marekmasiak2')
    writeDirectory(dire)

    context = {'postdata': dire}
    return render(request, 'blog/home.html', context)


def changedir(request):
    context = {}
    return render(request, 'blog/changedir.html', context)


def adstats(request):
    context = {'tytul': 'Strona domowa'}

    directory = getDirectory()
    try:
        adDataDirectory = directory + '/ads/advertisers_who_uploaded_a_contact_list_with_your_information.json'
        adContent = ""
        temporaryFile = open(adDataDirectory, 'r')
        if temporaryFile.mode == 'r':
            adContent = (temporaryFile.read())
        temporaryFile.close()
        adJSON = json.loads(adContent)

        context = {'dirname': directory, 'tytul': 'Reklamodawcy', 'adv': adJSON['custom_audiences']}
    except FileNotFoundError:
        context = {'dirname': directory, 'tytul': 'Reklamodawcy', 'error': 'Niestety w podanej ścieżce nie znaleziono plików z danymi Facebooka'}

    return render(request, 'blog/adstats.html', context)


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

        """
        Kod zbiera zawartosci poszczegolnych plikow
        zawierajace wiadomosci
        """
        messageContent = []
        words = {}

        for i in messagePaths:
            temporaryFile = open(i, 'r')
            if temporaryFile.mode == 'r':
                try:
                    tempContainer = json.loads(temporaryFile.read())
                    messageContent.append(json.loads(json.dumps(tempContainer).encode('latin1').decode('utf-8')))
                except:
                    pass
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
        for i in range(0, 50):
            wordList.append(words[i][0] + ' (' + str(words[i][1]) + ')')
            wordDict[words[i][0]] = words[i][1]
            wordKeys.append(words[i][0])
            wordItems.append(words[i][1])
        # plt.plot(wordKeys,wordItems)
        # plt.xlabel('Słowo')
        # plt.ylabel('Liczba wystąpień')
        # plt.savefig('/stat.png')
        context = {'tytul': 'Strona domowa', 'words': wordList, 'data': wordDict, 'pic': '/stat.png'}

    return render(request, 'blog/wordstats.html', context)


def messagestats(request):
    # context = {'dirname': '/users/asfd/asd/asdf', 'tytul': 'asdfasdfasdf', 'range': range(13)}
    try:
        directory = getDirectory()

        """
        Kod znajduje sciezki do
        wszystkich osob z ktorymi pisales
        i przechowuje je w messagePaths
        """
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
        """
        Kod zbiera zawartosci poszczegolnych plikow
        zawierajace wiadomosci
        """
        messageContent = []
        messageCount = {}
        for i in messagePaths:
            temporaryFile = open(i, 'r')
            if temporaryFile.mode == 'r':
                try:
                    messageContent.append(json.loads(temporaryFile.read()))
                except:
                    pass

            temporaryFile.close()

        """
        ZADANIE 1
        Kod liczy ilosc rzeczy z JSONArray messages
        i srednia ilosc wiadomosci
        """
        averageNumberOfMessages = 0

        for i in range(0, len(messageContent)):
            messageCount[i] = len(messageContent[i]['messages'])
            averageNumberOfMessages += messageCount[i]
        messageCount = sorted(messageCount.items(), key=operator.itemgetter(1), reverse=True)

        averageNumberOfMessages /= len(messageContent)

        """
        Wypisuje top 5 osob,
        z ktorymi pisales
        """

        #print('5 osob, z ktorymi najczesciej pisales to:')

        numberOfGroupChats = 1
        # print(len(messageCount))
        ppl = []
        for i in range(0, len(messageCount)):
            if len(messageContent[messageCount[i][0]]['participants']) <= 2:
                #print(str(messageContent[messageCount[i][0]]['participants'][0]['name']) + '(' + str(messageCount[i][1])+')')
                ppl.append(str(messageContent[messageCount[i][0]]['participants'][0]['name']) + '(' + str(messageCount[i][1]) + ')')
            else:
                numberOfGroupChats += 1
        context = {'dirname': directory, 'tytul': 'Strona Domowa', 'range': range(13), 'nr': numberOfGroupChats, 'avgmsg': averageNumberOfMessages, 'ppl': ppl}

    return render(request, 'blog/messagestats.html', context)


def about(request):
    context = {'tytul': 'o nas'}
    return render(request, 'blog/about.html', context)
