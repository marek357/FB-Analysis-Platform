from django.shortcuts import render
import os
import json
import operator
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from datetime import datetime, timedelta
from django.http import HttpResponse
# from django.core.files import File
# from .models import Audio


def getDirectory():
    file = open("direG.txt", "r")
    toReturn = file.read()
    file.close()
    if len(toReturn) > 0:
        return toReturn
    else:
        return 'nie ustalono lokalizacji danych'


def writeDirectory(directo):
    file = open("direG.txt", "w+")
    file.write(str(directo))
    file.close
    return


def writeDate(datePeriod):
    file = open("dateG.txt", "w+")
    file.write(str(datePeriod))
    file.close
    return


def getDate(mode):
    file = open("dateG.txt", "r")
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
    dire = request.POST.get('directory', '')
    days = request.POST.get('days', '')
    if len(str(dire)) > 0:
        writeDirectory(dire)
    if len(str(days)) > 0:
        writeDate(days)

    try:
        directory = getDirectory()
        lokDataDirectory = directory + '/Historia lokalizacji/Historia lokalizacji.json'
        temporaryFile = open(lokDataDirectory, 'r')
        context = {'postdata': getDirectory(), 'period': getDate(0), 'alert': "success", 'title': "Dane są poprawne"}
    except Exception as e:
        context = {'postdata': getDirectory(), 'period': getDate(0), 'alert': "error", 'title': 'Dane są niepoprawne'}

    # try:
    #     audioRecordingsDirectory = directory + '/Moja aktywność/Głos i dźwięk'
    #     audioData = os.listdir(audioRecordingsDirectory)
    #     for audioFile in audioData:
    #         print(audioFile)
    #         reopen = open(audioRecordingsDirectory + "/" + audioFile, "rb")
    #         audioFileRecording = File(reopen)
    #         nagranie = Audio(tytul=audioFile, nagranie=audioFileRecording)
    #         nagranie.save()

    #     print(Audio.objects.all())
    # except Exception as e:
    #     print (e)
    return render(request, 'googleproject/home.html', context)


def lokalizacja(request):
    directory = getDirectory()
    try:
        lokDataDirectory = directory + '/Historia lokalizacji/Historia lokalizacji.json'
        print()
        print(lokDataDirectory)
        print()
        temporaryFile = open(lokDataDirectory, 'r')
        places = []
        if temporaryFile.mode == 'r':
            tempContainer = json.loads(temporaryFile.read())
        temporaryFile.close()
        locationJSON = json.loads(json.dumps(tempContainer).encode('latin1').decode('utf-8', 'ignore'))
        jsonWithActualLocationArray = locationJSON["locations"]
        ile = len(jsonWithActualLocationArray)
        places = []
        for place in jsonWithActualLocationArray:
            a = ""
            a += str(place["latitudeE7"])[:2]
            a += "."
            a += str(place["latitudeE7"])[2:]
            b = ""
            b += str(place["longitudeE7"])[:2]
            b += "."
            b += str(place["longitudeE7"])[2:]
            places.append((a, b))

        goodPlaces = []
        for i in range(0, 50):
            print(places[i])
            goodPlaces.append((places[i][0], places[i][1]))
        for place in goodPlaces:
            print(place)
        context = {'postdata': 'hgjkhgjghkjghk', 'period': 'bbhjjhbhjb', 'data': places}
    except FileNotFoundError:
        context = {'postdata': 'hgjkhgjghkjghk', 'period': 'bbhjjhbhjb', 'data': 'nie udalo sie'}
    return render(request, 'googleproject/lokalizacja.html', context)


def changedir(request):
    context = {}
    return render(request, 'googleproject/changedir.html', context)


def image1(request):
    context = {}
    return HttpResponse("<meta http-equiv=\"refresh\" content=\"0; url=https://raw.githubusercontent.com/googlemaps/v3-utility-library/master/markerclusterer/images/m1.png\" />")


def image2(request):
    context = {}
    return HttpResponse("<meta http-equiv=\"refresh\" content=\"0; url=https://raw.githubusercontent.com/googlemaps/v3-utility-library/master/markerclusterer/images/m2.png\" />")


def image3(request):
    context = {}
    return HttpResponse("<meta http-equiv=\"refresh\" content=\"0; url=https://raw.githubusercontent.com/googlemaps/v3-utility-library/master/markerclusterer/images/m3.png\" />")


def image4(request):
    context = {}
    return HttpResponse("<meta http-equiv=\"refresh\" content=\"0; url=https://raw.githubusercontent.com/googlemaps/v3-utility-library/master/markerclusterer/images/m4.png\" />")


def image5(request):
    context = {}
    return HttpResponse("<meta http-equiv=\"refresh\" content=\"0; url=https://raw.githubusercontent.com/googlemaps/v3-utility-library/master/markerclusterer/images/m5.png\" />")


def audio(request):
    context = {}
    nagrania = {}
    try:
        directory = getDirectory()
        audioPaths = []
        audioRecordingsDirectory = directory + '/Moja aktywność/Głos i dźwięk'
        audioData = os.listdir(audioRecordingsDirectory)
        for rec in audioData:
            nagrania[rec] = (audioRecordingsDirectory + "/" + rec).encode("utf-8").decode()

        for rec in nagrania:
            print(str(rec) + " " + str(nagrania[rec]))

        context = {'dirname': directory, 'tytul': 'Statystyki nagrań', 'audio': audioData}
    except FileNotFoundError:
        context = {'dirname': directory, 'tytul': 'Statystyki nagrań', 'error': 'Niestety w podanej ścieżce nie znaleziono plików z nagraniami Google\'a'}

    return render(request, 'googleproject/audio.html', context)
