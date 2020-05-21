from __future__ import unicode_literals

import ast
### for audio processing###
###
from fastdtw import fastdtw
from scipy.io.wavfile import read
from scipy.spatial.distance import euclidean

###
### for audio processing###

from flask import *
from flask import Flask, render_template, request,flash\
    , redirect,url_for,session,logging
# for sign up and login forms ####
from flask_mysqldb import MySQL

from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
from functools import wraps

# for sign up and login forms ####

import youtube_dl
from os import listdir
import urllib
import json
import imutils
import cv2
import threading
import time
from lxml import etree
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import pairwise_distances
from flask import Flask, render_template
from flask import Flask, redirect, url_for, session
from flask_oauth import *
from urllib.request import urlopen
from urllib.error import URLError
from urllib.request import Request
import mysql.connector
import os
import numpy as np
from werkzeug.utils import secure_filename
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip



##for converting filtered video to mp4 #####
####
import subprocess


####
##for converting filtered video to mp4 #####
#####




app=Flask(__name__, static_folder='static')


#### Audio Processing ####
####
audioArray = [] ## array  of the average numbers for each audio class
readingFiles =['Burping_or_eructation','Cello','Clarinet',
                 'Cough','Double_bass','Drawer_open_or_close','Finger_snapping',
                 'Glockenspiel','Gong','Gunshot_or_gunfire','Harmonica','Hi-hat','Knock','Laughter',
                 'Meow','Oboe','Saxophone','Shatter','Snare_drum','Tambourine','Tearing','Telephone','Trumpet','Violin_or_fiddle']


def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


def readSelectedClasses():
    readingFiles=['Burping_or_eructation','Cello','Clarinet',
                 'Cough','Double_bass','Drawer_open_or_close','Finger_snapping',
                 'Glockenspiel','Gong','Gunshot_or_gunfire','Harmonica','Hi-hat','Knock','Laughter',
                 'Meow','Oboe','Saxophone','Shatter','Snare_drum','Tambourine','Tearing','Telephone','Trumpet','Violin_or_fiddle']
    return readingFiles

def getAudioFilesPaths():
    readAudioFilesPaths=[['27172052.wav', '286df5e5.wav', '374c8729.wav', '60f3194b.wav', '6a5304b5.wav', '6de76397.wav', '715905f4.wav', '76306f8b.wav', '8128fdb4.wav', '9b1825ea.wav'],['04ab46a9.wav', '05723b3a.wav', '0fba4394.wav', '1146e063.wav', '19a686e2.wav', '2174fe5c.wav', '24adc8ef.wav', '27ebc5bc.wav', '2c14ed19.wav', '2ec85d18.wav'],['0459ee65.wav', '07d5cca9.wav', '0db65bf4.wav', '0e398b30.wav', '12a0327a.wav', '15389a70.wav', '181505d1.wav', '201b29ef.wav', '21d36543.wav', '2676d124.wav'],['07c8463e.wav', '0d6e2584.wav', '2849b57a.wav', '3e810d62.wav', '5e3e89f1.wav', '6fe61dd6.wav', '8199d25e.wav', '93243c6f.wav', '976a40fb.wav', 'bc0cd163.wav'],['023eab1f.wav', '028db587.wav', '0381efd3.wav', '0716b51d.wav', '0b32ee85.wav', '1fe092a5.wav', '2976b7eb.wav', '2cc34e65.wav', '3f7c6870.wav', '433490d3.wav'],['04b249bd.wav', '1837f058.wav', '1fc58e0f.wav', '392819ad.wav', '41111461.wav', '416d2ced.wav', '45fc6c9b.wav', '4698193e.wav', '75962078.wav', '77393d30.wav'],['17e829a7.wav', '19536d06.wav', '207b5701.wav', '41b78889.wav', '45acd2f0.wav', '536c4991.wav', '6f7fe040.wav', '76fbffde.wav', '7a135d94.wav', '92e273eb.wav'],['0a5cbf90.wav', '17a4e6f1.wav', '26e34006.wav', '3863cc53.wav', '3f303b25.wav', '419941be.wav', '46b5a369.wav', '4a51b1a7.wav', '4e0759b2.wav', '5ceab91b.wav'],['08d23bb8.wav', '0e7aea38.wav', '10dba05f.wav', '1bb20333.wav', '1cbdc6d4.wav', '25988d89.wav', '28e59c89.wav', '32393924.wav', '37d02372.wav', '4110cbce.wav'],['03c5bfbb.wav', '08e27974.wav', '0b430780.wav', '0f5182eb.wav', '1472c52c.wav', '16a2e687.wav', '1850e006.wav', '1d73513c.wav', '1dba45ae.wav', '1ef40308.wav'],['079faac8.wav', '0ef36ea1.wav', '1810cd33.wav', '1c35850e.wav', '21acb432.wav', '2804c60c.wav', '2f009392.wav', '34409de5.wav', '3c0e6e53.wav', '41ebdb67.wav'],['1a35ff8a.wav', '23071dd2.wav', '2eaff904.wav', '3919052c.wav', '75306f5f.wav', '7b7dd15e.wav', 'cbc6e28a.wav', 'd86d62ff.wav', 'f3ab1ef3.wav', 'fad0ea2e.wav'],['02fb6c5b.wav', '1ec6c9c2.wav', '1fd0397d.wav', '2487cd7b.wav', '280a3d2b.wav', '3374eb78.wav', '38957ab8.wav', '38a944f7.wav', '39409d9a.wav', '3ea8071a.wav'],['1a2f7f1a.wav', '2442e7c6.wav', '247a90a0.wav', '30a320a3.wav', '327bdcaa.wav', '38ae005d.wav', '41ee0c63.wav', '4b036d3e.wav', '4e395bf5.wav', '54aa5112.wav'],['0586f0e0.wav', '07c95625.wav', '0c91a6b2.wav', '2750c860.wav', '2cb6b373.wav', '375d2777.wav', '39b23710.wav', '5b7ab76d.wav', '763efe7a.wav', '7c6c426f.wav'],['00326aa9.wav', '07682400.wav', '0fe4e425.wav', '22f3b36c.wav', '24f112b3.wav', '2fd2722a.wav', '3ce96793.wav', '3d5d1b2b.wav', '3e28d521.wav', '45d66815.wav'],['007759c4.wav', '008afd93.wav', '059d5420.wav', '0967cebd.wav', '0995f876.wav', '09c9b50b.wav', '09d2d1c0.wav', '09e83f2a.wav', '0bb807c0.wav', '0fd76662.wav'],['1f8ce32b.wav', '2f1c2612.wav', '40d3c212.wav', '67eb9a30.wav', '766d0eb4.wav', '8a2793a4.wav', '8de247b4.wav', '9e4016e8.wav', 'a5f420d3.wav', 'aebe749b.wav'],['0638da1a.wav', '32a5773b.wav', '539c0118.wav', '897a1c21.wav', '8d13a005.wav', '95adeda9.wav', 'a911ed29.wav', 'aa41eeec.wav', 'acd9adb9.wav', 'ae1e828a.wav'],['058e63ea.wav', '16aaa6b7.wav', '191087dd.wav', '36a2202d.wav', '3ad721ec.wav', '3b6964dc.wav', '41703f1f.wav', '433d59e7.wav', '4b8aa2a7.wav', '518f0af2.wav'],['0f4edd6e.wav', '4ed15aa6.wav', '52aaf874.wav', '53ffaeb3.wav', '58848256.wav', '66660ca1.wav', '6b6c0405.wav', '7336a65e.wav', '7fbc0a0e.wav', '897071cd.wav'],['030db750.wav', '06c535eb.wav', '1b004964.wav', '1d2feaeb.wav', '3ac46d6b.wav', '439acbcc.wav', '451d1eb2.wav', '500fa310.wav', '536199a4.wav', '55d3227f.wav'],['05ad10fb.wav', '0d99cfde.wav', '18b390aa.wav', '2d6de409.wav', '2e42ccd2.wav', '3c7db3ac.wav', '51ab7f85.wav', '55f687f3.wav', '570a1821.wav', '58a13aa9.wav'],['06e4c394.wav', '08904a43.wav', '097cdef5.wav', '14dcf709.wav', '163b9ad7.wav', '16d0c74a.wav', '17cfddcf.wav', '18d8abc6.wav', '1b12b1e4.wav', '1b7c4e2b.wav']]
    return readAudioFilesPaths

def CropAndProcessAudio(file_name):
    file_name = file_name.replace(".mp4", "")
    folderPath = "../pythonAnyWhere1/audios/"
    deleteAudioFiles(folderPath)
    command = f"ffmpeg -i ../pythonAnyWhere1/static/{file_name}.mp4 -ab 160k -ac 2 -ar 44100 -vn ../pythonAnyWhere1/audios/audioFile.wav"
    subprocess.call(command, shell=True)
    audioFilePath = '../pythonAnyWhere1/audios/audioFile.wav'

    readAudioFilesPaths=getAudioFilesPaths()
    readingFiles=[]
    readingFiles = readSelectedClasses()
    i=0



    print("readingFiles: ",len(readingFiles))
    print("readAudioFilesPaths: ",len(readAudioFilesPaths))

    while i<len(readingFiles):
        print('readAudioFilesPaths[i] in ',i,' : ',readAudioFilesPaths[i])
        print('readAudioFilesPaths[i] in ',i,' : ',readAudioFilesPaths[i])

        processSounds(audioFilePath=audioFilePath,allSounds=readAudioFilesPaths[i],folderPath=folderPath,readingFiles=readingFiles[i])
        i+=1

def processSounds(audioFilePath,allSounds,folderPath,readingFiles):
    i=0
    min=0
    a = read(audioFilePath)
    a = np.array(a[1])
    print("Uploaded Audio File", a)
    distances=[]
    folderPath = os.path.join(folderPath,readingFiles)
    while i<10:
        allSoundsPath = find(allSounds[i], folderPath)
        allSoundsPath= str(allSoundsPath)
        allSoundsPath = allSoundsPath.replace('\\', '/')
        b=read(str(allSoundsPath))

        b=np.array(b[1])
        print("Existing Audio File",i," is ",b)




        distance, path = fastdtw(a, b, dist=euclidean)
        print("distance: ",distance)
        distances.append(distance)
        #
        i+=1
    i=0
    while i<len(allSounds):

       if min==distances[i]:
           print("index: ",i)

       i+=1
    distancesSum=0
    print('length of disctances: ',len(distances))
    i=0
    while i<len(distances):
        distancesSum+=distances[i]
        i+=1
    distancesAverage=distancesSum/len(distances)
    global audioArray
    audioArray.append(distancesAverage)
    print('distancesAverage: ',distancesAverage)
####
#### Audio Processing ####

######## Database Connection ########
db_connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd="",
    database="rec_system"
)
my_database = db_connection.cursor()

mycursor = db_connection.cursor()
######## Database Connection ########

objectsDetected = []
noOfOccurences = []
emptyArray = []
Total=[]


############### Classification variables needed  ###############
###############
noOfClusters=3
numberOfTopN=3 # the N  most similar videos to the unseen video
sql="SELECT COUNT(*) FROM movie"
mycursor.execute(sql)
mainResult = mycursor.fetchall()
mainResultValue=mainResult[0][0]
arrayOfArrays=[[] for _ in range(mainResultValue)]
NoOfOccurencesTotal=[[] for _ in range(mainResultValue)]
arrayOfArraysFrequency=[[] for _ in range(mainResultValue)]


###############
############### Classification  needed ###############

############### Filter Video global variable ###############
###############
globalOriginalVideo=""
###############
############### Filter Video global variable  ###############


#### user Id ####
userId=-1
#### user Id ####


#### Decode google account data and convert it to json object ####
def decodeData(GmailData):

    GmailData = GmailData.decode('utf-8')
    d = json.loads(GmailData)
    return d

#### Decode google account data ####



############### Sign in choices page################################
###############

@app.route('/signInChoicesPage')
def signInButton():
    access_token = session.get('access_token')
    if access_token is None:
        return render_template("SignInPage.html")
    else:
        if request.method == 'GET':
            return redirect(url_for('Choose'))



###############
############### Sign in choices page################################
##############the Settings page###########################
##########
@app.route('/settings',methods=["GET","POST"])
def settings():
    print('user id:',userId)
    mycursor.execute("SELECT * FROM filtervideo WHERE userId = %s", [(str(userId))])
    myresult = mycursor.fetchall()
    if len(myresult) <= 0:
        query="INSERT INTO filtervideo(userId,isFilter) VALUES(%s,%s)"
        mycursor.execute(query,(str(userId),-1))
        db_connection.commit()
    return render_template("settings.html")
##########
##############the Settings page###########################

############### Google Sign In API ################################
###############
GOOGLE_CLIENT_ID = '85769935833-dkv26gf8hg3rm8iv62h4djo5jq40altu.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'gqtHrkbgSpwrNlRDGptA7ErZ'
REDIRECT_URI = '/'  # one of the Redirect URIs from Google APIs console
SECRET_KEY = 'X3-_/xa7q(/xe2/xf4/xd4/xd8/x12/x9e/x81/xc1`d/xe5/xcc/xf4/x9bG/xe7/xcc'
app.secret_key = SECRET_KEY
oauth = OAuth()
google = oauth.remote_app('google',
                          base_url='https://www.google.com/accounts/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile',
                                                'response_type': 'code'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={'grant_type': 'authorization_code'},
                          consumer_key=GOOGLE_CLIENT_ID,
                          consumer_secret=GOOGLE_CLIENT_SECRET)

@app.route('/GoogleIndex')
def index():
    access_token = session.get('access_token')

    if access_token is None:
        return redirect(url_for('login'))
    access_token = access_token[0]
    headers = {'Authorization': 'OAuth '+access_token}
    req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
                  None, headers)




    try:
        res = urlopen(req)
        session['GmailData']=decodeData(res.read())
        #insert the email data in database
        savegoogleAccount()
        #insert the email data in database
    except URLError as e:
        if e.code == 401:
            # Unauthorized - bad token
            session.pop('access_token', None)
            return redirect(url_for('login'))
        return res.read()

    access_token = session.get('access_token')
    if access_token != None:
        return render_template("SignInSuccessful.html")
@app.route('/login')
def login():
    callback = url_for('authorized', _external=True)
    return google.authorize(callback=callback)
@app.route('/authorized')
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return redirect(url_for('index'))


@google.tokengetter
def get_access_token():
    return session.get('access_token')


###############
############### Google Sign In API ################################

############### Save google account data to database ################################
###############
def savegoogleAccount():
    ID=session['GmailData']["id"]
    fname=session['GmailData']["given_name"]
    lname=session['GmailData']["family_name"]
    email=session['GmailData']["email"]
    username=session['GmailData']["email"].replace('@gmail.com', '')
    password='notAvailable'
    session['email']=session['GmailData']["email"]

    mycursor.execute("SELECT * FROM user WHERE email = %s", [email])
    myresult = mycursor.fetchall()
    if len(myresult) > 0:
        global userId
        userId = myresult[0][0]
    elif len(myresult) <= 0:

        mycursor.execute("INSERT INTO user(fname,lname,email,username,password) VALUES(%s, %s, %s, %s, %s)",(fname, lname, email, username, password))
        userId = mycursor.lastrowid
        print('user id: ',userId)
        db_connection.commit()



###############
############### Save google account data to database ################################






############### Youtube Function to get the name of the youtube video ############

def getYoutubeName(videoPath):
    youtube = etree.HTML(urllib.request.urlopen(videoPath).read())
    video_title = youtube.xpath("//span[@id='eow-title']/@title")
    return video_title
############### Youtube Function to get the name of the youtube video ############



############### Filter Video  ###############
###############
@app.route('/isFilteredYes',methods=["GET","POST"])
def isFilteredYes():

    if request.method == 'GET':
        sql = "UPDATE filtervideo SET isFilter = 0 WHERE filtervideo.userId ="+str(userId)

        mycursor.execute(sql)
        db_connection.commit()

        return redirect(url_for('settings'))

@app.route('/isOriginalYes',methods=["GET","POST"])
def isOriginalYes():
    if request.method == 'GET':

        sql = "UPDATE filtervideo SET isFilter = -1 WHERE filtervideo.userId ="+str(userId)

        mycursor.execute(sql)
        db_connection.commit()

        return redirect(url_for('settings'))
@app.route('/originalVideoDirectory',methods=["GET","POST"])
def originalVideoFunction():

    if request.method == 'POST':
        global globalOriginalVideo
        print('global Original Video: ',globalOriginalVideo)
        globalOriginalVideoString=str(globalOriginalVideo)

        return render_template("originalVideo.html",originalVideo=globalOriginalVideoString)

@app.route('/filteredVideoDirectory',methods=["GET","POST"])
def filteredVideoFunction():
    if request.method == 'POST':
        return render_template('filteredVideo.html')
###############
############### Filter Video  ###############

### Getting cluster head Ids ###
###
def cosineSimilarity(sortedFreq):
    dist_out = 1 - pairwise_distances(sortedFreq, metric="cosine")

    global maxNumber
    i=0
    while i<(noOfClusters-1):
        if maxNumber<dist_out[3][i]:
            maxNumber=dist_out[3][i]

        i+=1

    i=0
    global maxNumberIndex
    while i<(noOfClusters-1):
        if maxNumber == dist_out[3][i]:
            maxNumberIndex = i
        i += 1

def getClusterHeadsIds(): ## to get the  movie Ids of each cluster
    movieIdArray=[]
    clusterHead = 0
    while clusterHead < noOfClusters:
        mycursor.execute("SELECT * FROM movie WHERE movie.clusterHead=0")
        myresult = mycursor.fetchall()

        for x in myresult:
            if  x[0] in movieIdArray:
                continue
            else:
                movieIdArray.append(x[0])

        clusterHead+=1
    #print('movieIdArray: ', movieIdArray)
    return movieIdArray


###
### Getting cluster head Ids ###

#### Organizing arrays with all object names ###
###
def constructAllObjectsInOrder(same):
    column = 0
    while column < len(objectsDetected):
        lastRow = mainResultValue - 1
        arrayOfArrays[lastRow].append(objectsDetected[column])
        arrayOfArraysFrequency[lastRow].append(noOfOccurences[column])
        column += 1

    mint = 0

    while True:
        for z in arrayOfArrays[mint]:
            for zzz in Total:
                if z == zzz:
                    same = True
            if same == False:
                Total.append(z)
            same = False
        mint += 1
        if mint == 4:
            break

    tint = 0

    i = 0
    while True:

        if (i <= len(Total)):
            NoOfOccurencesTotal[tint].append(0)
        elif (i > len(Total)):
            i = 0
            tint += 1

        i += 1
        if tint >= mainResultValue:
            break
    i = 0



    sortedFreq = [[] for _ in range(mainResultValue)]
    obj = 0
    while obj < len(Total):
        moviesCount = 0
        while moviesCount < mainResultValue:
            Founder = 0
            value = 0
            while Founder < len(arrayOfArrays[moviesCount]):
                if Total[obj] == arrayOfArrays[moviesCount][Founder]:
                    value = arrayOfArraysFrequency[moviesCount][Founder]
                    break

                Founder += 1
            sortedFreq[moviesCount].append(value)
            moviesCount += 1

        obj += 1

    cosineSimilarity(sortedFreq)
## end constructAllObjectsInOrder ##

###getting the object of the topN videos###
###
def readVideo(objectsDetected,noOfOccurences):
    movieIdArray=[]
   
    movieIdArray=getClusterHeadsIds()
    same=False
    clusterId = 0
    i = 0
    while clusterId < noOfClusters:
        mycursor.execute("SELECT * FROM processed WHERE MovieID="+str(movieIdArray[clusterId]))
        myresult = mycursor.fetchall()

        for x in myresult:






             arrayOfArrays[i].append(x[2])
             arrayOfArraysFrequency[i].append(x[3])



        clusterId+=1
        i += 1
        # print(movieId)

        constructAllObjectsInOrder(same)









### Seeing the similarity between the topN and the video of the user ###
###
def readForConfusionMatrix(arrayOfArrays, arrayOfArraysFrequency, NoOfOccurencesTotal, Total, same,
                           numberOfVideosTopN, idS):
    arrayOfArrays.append(objectsDetected)
    arrayOfArraysFrequency.append(noOfOccurences)


    mint = 0
    while True:
        for z in arrayOfArrays[mint]:
            for zzz in Total:
                if z == zzz:
                    same = True
            if same == False:
                Total.append(z)
            same = False
        mint += 1
        if mint == numberOfTopN:
            break

    tint = 0
    i = 0
    while True:

        if (i <= len(Total)):
            NoOfOccurencesTotal[tint].append(0)
        elif (i > len(Total)):
            i = 0
            tint += 1

        i += 1
        if tint >= numberOfTopN:
            break
    i = 0

    sortedFreq = [[] for _ in range(numberOfTopN+1)]
    obj = 0
    while obj < len(Total):
        moviesCount = 0
        while moviesCount < (numberOfTopN+1):
            Founder = 0
            value = 0
            while Founder < len(arrayOfArrays[moviesCount]):
                if Total[obj] == arrayOfArrays[moviesCount][Founder]:
                    value = arrayOfArraysFrequency[moviesCount][Founder]
                    break

                Founder += 1
            sortedFreq[moviesCount].append(value)
            moviesCount += 1

        obj += 1

    return sortedFreq

### Seeing the similarity between the topN and the video of the user ###
###

def getConfusionMatrix(topNVariableHere):
    sql = "SELECT * FROM movie INNER JOIN processed ON movie.ID= processed.MovieID AND movie.topN="
    sql2 = " ORDER BY movie.ID ASC"
    mycursor.execute(sql + str(topNVariableHere) + sql2)
    myresult = mycursor.fetchall()
    numberOfVideosTopN = len(myresult)
    arrayOfArrays = [[] for _ in range(numberOfTopN)]
    NoOfOccurencesTotal = [[] for _ in range(numberOfTopN)]
    arrayOfArraysFrequency = [[] for _ in range(numberOfTopN)]
    Total = []
    same = False
    idS = []  # the similar videos links in one array
    i = 0
    for x in myresult:
        if (x[0] in idS) == False and idS != []:
            idS.append(x[0])
            i += 1
            # print("movieUrl: ",x[0])
        arrayOfArrays[i].append(x[8])
        arrayOfArraysFrequency[i].append(x[9])
        if idS == []:
            idS.append(x[0])
    sortedFreq=readForConfusionMatrix(arrayOfArrays, arrayOfArraysFrequency, NoOfOccurencesTotal, Total, same, numberOfVideosTopN, idS)

### Getting Related Video Links that are related to the video inserted by the user
###
def getRelatedVideosLinks():
    # Taking the maxNumber Index extracted from read which gets the similar cluster to the video then
    # by using the clusterHeadId we can get the related videos by getting 3 videos from the database
    movieIdArray = getClusterHeadsIds()
    clusterHeadMovieId=movieIdArray[maxNumberIndex]
    mycursor.execute("SELECT clusterId FROM movie WHERE movie.ID="+str(clusterHeadMovieId))
    myresult = mycursor.fetchall()
    similarVideoClusterId=-1 # getting the cluster Id here
    for x in myresult:

        similarVideoClusterId=x[0] ##getting the cluster id which is the cluster similar to the unseen video the user inserted
    getTopN(similarVideoClusterId)
    topNVariableHere=0 # Top N boolean in the movie table(database)






    getConfusionMatrix(topNVariableHere)






    mycursor.execute("SELECT movieUrl FROM movie WHERE topN=" + str(topNVariableHere))
    myresult = mycursor.fetchall()
    relatedVideosLinks=[] # the similar videos links in one array
    for x in myresult:

        relatedVideosLinks.append(x[0])
    return relatedVideosLinks
###
### Getting Related Video Links that are related to the video inserted by the user

### Getting the most similar videos to the video insert by the user
###

### Here getting the cosine similarity
###
def cosineSimilarityTopN(sortedFreq,movieIdArrayInOneCluster):
    dist_out = 1 - pairwise_distances(sortedFreq, metric="cosine")

    i=0
    maxNumbers=[]
    while i<numberOfTopN:
        maxNumbers.append(0.1)
        i+=1
    numberOfMovies=len(movieIdArrayInOneCluster)
    topNIndex=0
    #print(len(dist_out)-1)
    while topNIndex<numberOfTopN:
        i=0
        while i<(numberOfMovies-1):
            if topNIndex>0:
                if maxNumbers[topNIndex]<maxNumbers[topNIndex-1] and dist_out[len(dist_out)-1][i]<maxNumbers[topNIndex-1]:
                    # print("maxNumbers[topNIndex-1]: ",maxNumbers[topNIndex-1])
                    if maxNumbers[topNIndex]<dist_out[len(dist_out)-1][i]:
                        maxNumbers[topNIndex]=dist_out[len(dist_out)-1][i]
            elif topNIndex==0:
                if maxNumbers[topNIndex] < dist_out[len(dist_out)-1][i]:
                    maxNumbers[topNIndex] = dist_out[len(dist_out)-1][i]

            i+=1
        topNIndex+=1
    topNIndex = 0
    maxNumberIndices = []
    while topNIndex < numberOfTopN:
        i=0
        while i<(numberOfMovies-1):

            if maxNumbers[topNIndex] \
                    == dist_out[len(dist_out)-1][i]:
                maxNumberIndices.append(i)
                topNIndex += 1
                if topNIndex>2:
                    break
            i += 1
    topNIndex=0
    while topNIndex<numberOfTopN:
        topNMaxNumberindex=maxNumberIndices[topNIndex]
        sql = "UPDATE movie SET topN = %s WHERE ID = %s"
        val = (0, movieIdArrayInOneCluster[topNMaxNumberindex])
        mycursor.execute(sql, val)
        db_connection.commit()
        topNIndex+=1

###
### Here getting the cosine similarity

def getTopN(similarVideoClusterId): #Get top 3 videos similar to the unseen video
    sql = "SELECT * FROM      movie WHERE clusterId="
    mycursor.execute(sql + str(similarVideoClusterId))
    myresult = mycursor.fetchall()
    numberOfVideosInCluster=len(myresult)
    arrayOfArrays = [[] for _ in range(numberOfVideosInCluster)]
    NoOfOccurencesTotal = [[] for _ in range(numberOfVideosInCluster)]
    arrayOfArraysFrequency = [[] for _ in range(numberOfVideosInCluster)]
    Total = []
    same=False
    sql = "SELECT * FROM movie INNER JOIN processed ON movie.ID= processed.MovieID AND movie.clusterId="
    sql2 = " ORDER BY movie.ID ASC"
    mycursor.execute(sql+ str(similarVideoClusterId)+ sql2)
    myresult = mycursor.fetchall()
    idS = []  # the similar videos links in one array
    i = 0
    for x in myresult:
        if (x[0] in idS) == False and idS != []:
            idS.append(x[0])
            i += 1
        arrayOfArrays[i].append(x[8])
        arrayOfArraysFrequency[i].append(x[9])
        if idS == []:
            idS.append(x[0])
    readTopN(arrayOfArrays,arrayOfArraysFrequency,NoOfOccurencesTotal,Total,same,numberOfVideosInCluster,idS)

def readTopN(arrayOfArrays,arrayOfArraysFrequency,NoOfOccurencesTotal,Total,same,numberOfVideosInCluster,idS):
    column = 0
    while column < len(objectsDetected):
        lastRow = numberOfVideosInCluster - 1
        arrayOfArrays[lastRow].append(objectsDetected[column])
        arrayOfArraysFrequency[lastRow].append(noOfOccurences[column])
        column += 1


    mint = 0
    while True:
        for z in arrayOfArrays[mint]:
            for zzz in Total:
                if z == zzz:
                    same = True
            if same == False:
                Total.append(z)
            same = False
        mint += 1
        if mint == numberOfVideosInCluster:
            break

    tint = 0
    i = 0
    while True:

        if (i <= len(Total)):
            NoOfOccurencesTotal[tint].append(0)
        elif (i > len(Total)):
            i = 0
            tint += 1

        i += 1
        if tint >= numberOfVideosInCluster:
            break
    i = 0


    sortedFreq = [[] for _ in range(numberOfVideosInCluster)]
    obj = 0
    while obj < len(Total):
        moviesCount = 0
        while moviesCount < numberOfVideosInCluster:
            Founder = 0
            value = 0
            while Founder < len(arrayOfArrays[moviesCount]):
                if Total[obj] == arrayOfArrays[moviesCount][Founder]:
                    value = arrayOfArraysFrequency[moviesCount][Founder]
                    break

                Founder += 1
            sortedFreq[moviesCount].append(value)
            moviesCount += 1

        obj += 1

    cosineSimilarityTopN(sortedFreq,idS)

###
### Getting the most similar videos to the video insert by the user


############### Classification getting the array got from processing ###############
###############

maxNumber=0
maxNumberIndex = -1



###############
############### Classification getting the array got from processing ###############

##### Sign up (Native) ##############################
#######
# Register Form Class
class RegisterForm(Form):
    fname = StringField('First Name', [validators.Length(min=1, max=50)])
    lname = StringField('Last Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50),validators.email("Please enter a valid email address.")])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        fname = form.fname.data
        lname = form.lname.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        # mycursor= mysql.connection.cursor()

        # Execute query
        mycursor.execute("SELECT * FROM user WHERE email = %s", [email])
        myresult = mycursor.fetchall()
        if len(myresult) > 0:
            flash(u'This email is taken please choose another email', 'success')

        else:
            mycursor.execute("INSERT INTO user(fname,lname,email,username,password) VALUES(%s, %s, %s, %s, %s)", (fname,lname, email, username, password))
            # Commit to DB
            db_connection.commit()

            # Close connection
            # mycursor.close()

            flash('You are now registered and can log in', 'success')

            return redirect(url_for('loginNative'))
    return render_template('register.html', form=form)
#######
##### Sign up (Native) ##############################


##### Login (Native) ##############################
#######


# User login
@app.route('/login(Native)', methods=['GET', 'POST'])
def loginNative():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']


        # Get user by username
        mycursor.execute("SELECT * FROM user WHERE username = %s", [username])
        myresult = mycursor.fetchall()
        if len(myresult) > 0:
            # Get stored hash
            # data = mycursor.fetchall()
            #print('data: ',myresult[0][5])
            password = myresult[0][5]
            global userId
            userId = myresult[0][0]


            print("userId: ",userId)


            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username
                flash('You are now logged in', 'success')
                return redirect(url_for('Choose'))
            else:
                error = 'Invalid login'
                return render_template('login(Native).html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login(Native).html', error=error)

    return render_template('login(Native).html')


#######
##### Login (Native) ##############################
# Check if user logged in #################
#######
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap
#######
# Check if user logged in #################

# Logout  #################
#######
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('loginNative'))

#######
# Logout  #################


### Choosing either uploading or inserting video link
@app.route('/',methods=["GET","POST"])
def Choose():

    if request.method == 'POST' and 'media' in request.files:
        pass
        #print('Choose URL')
    return render_template("choice.html")
###
### Choosing either uploading or inserting video link


### The Loading page before the user gets to the related videos
###

@app.route('/loadingScreen',methods=["GET","POST"])
def loadingScreen():
    if request.method == 'POST' and 'media' in request.files:
        #print('Choose URL')
        return render_template("loadingScreen.html")
    if request.method == 'GET':
        return render_template("loadingScreen.html")
    return render_template("loadingScreen.html")
    # else:
    #     return redirect(url_for('testing'))


###
### The Loading page before the user gets to the related videos ###


###The page where you upload the video ###
###
@app.route("/uploadSection",methods=["GET","POST"])
def upload():

    # print(clip.duration)

    return render_template("file_upload.html")

###
###The page where you upload the video ###

##Output related videos || also makes the processing video in it runs in the background [success() function]###
##

@app.route("/test",methods=["GET","POST"])
def testing():

    ############
    new_path = ''
    # print(time.time())
    if request.method == 'POST' and 'media' in request.files:
        pass
        # print('Test dir')
        # return redirect(url_for('Choose'))
    if request.method == 'POST':
        f = request.files['file']
        success.file_name = f.filename

        #print('success.file_name: ',success.file_name)

        allFilePath=' '+success.file_name

        processAudioThread = threading.Thread(target=CropAndProcessAudio, args=(f.filename,))
        processAudioThread.start()
        # audio_processing()

        if f:
            filename = secure_filename(f.filename)
            f.save(os.path.join('../pythonAnyWhere1/static', secure_filename(f.filename)))
            # print(contents)
            new_path = os.path.abspath(f.filename)
            #print('new_path: ',new_path)

            baseName = os.path.basename(new_path)
            baseName = str(baseName)
            #print("baseName: ",baseName)

            fileProcessed = '../pythonAnyWhere1/static/'+baseName
            processVideoThread = threading.Thread(target=success, args=(fileProcessed,))
            processVideoThread.start()




    VideoLinksArray = getRelatedVideosLinks()
    #print("VideoLinksArray: ", VideoLinksArray)
    videoPaths=[]

    i=0
    while i<3:
        videoPaths.append(VideoLinksArray[i])


        i += 1

    videoNames=['a','b','c'] # filling the video names and then retrieving it from getYoutubeName function
    i=0
    while i<3:
        videoNames[i]=''.join(getYoutubeName(videoPaths[i]))

        i+=1
    isFilter=-1
    # userId=session['ID']
    if request.method == 'GET':
        mycursor.execute("SELECT *  FROM filtervideo WHERE filtervideo.userId=" + str(userId))
        myresult = mycursor.fetchall()
        for x in myresult:
            isFilter=x[2]
            print('isFilter: ',isFilter)
    mycursor.execute("SELECT *  FROM filtervideo WHERE filtervideo.userId=" + str(userId))
    myresult = mycursor.fetchall()
    for x in myresult:
        isFilter = x[2]
        print('isFilter: ', isFilter)

    #the if conditions is for what button to show the original video button or the filterVideo button
    #####
    if isFilter ==-1:
        return render_template("test.html",filePath=new_path,ThePath=videoPaths[0],ThePath2=videoPaths[1],ThePath3=videoPaths[2],
                               videoName=videoNames[0],videoName2=videoNames[1],videoName3=videoNames[2]
                               )
    elif isFilter==0:
        return render_template("test2.html", filePath=new_path, ThePath=videoPaths[0], ThePath2=videoPaths[1],
                               ThePath3=videoPaths[2],
                               videoName=videoNames[0], videoName2=videoNames[1], videoName3=videoNames[2]
                               )
    #####
    # end if ############################################################


    #######


##
##Output related videos || also makes the processing video in it runs in the background [success() function]###


## Delete the audio file that was processed already###
##

def deleteAudioFiles(folderPath):
    for file_name in listdir(folderPath):
        if file_name.endswith('.wav'):
            os.remove(folderPath + file_name)

##
## Delete the audio file that was processed already###

## Process the video and extract frequencies and object names from and filer it which is gone to the filtered file directory ###
##

@app.route("/success",methods=['GET', 'POST'])
def success(filename):

    file_name=filename
    #print('file name: ',file_name)
    global globalOriginalVideo
    globalOriginalVideo =str(os.path.basename(file_name))
    cv2.VideoCapture(file_name)



    yolo_coco_dir = os.path.dirname('yolo-coco')
    coco_file_path = 'yolo-coco/coco.names'
    # os.path.join(yolo_coco_dir, 'coco.names')
    cfg_file_path = 'yolo-coco/yolov3.cfg'
    # os.path.join(yolo_coco_dir, 'yolov3.cfg')
    weights_file_path = 'yolo-coco/yolov3.weights'
    
    # os.path.join(yolo_coco_dir, 'yolov3.weights')
    # this_directory = os.path.abspath(os.path.dirname(__file__))
    # parent_directory = os.path.split(this_directory)[0]
    labelsPath = 'yolo-coco/coco.names'
    LABELS = open(labelsPath).read().strip().split("\n")
    print(LABELS)
    done = False
    filterVideo = False

    np.random.seed(42)
    COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")
    # derive the paths to the YOLO weights and model configuration
    # up is working well
    net = cv2.dnn.readNetFromDarknet(cfg_file_path, weights_file_path)
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    vs = cv2.VideoCapture(file_name)
    writer = None
    (W, H) = (None, None)
    try:
        prop = cv2.cv.CV_CAP_PROP_FRAME_COUNT if imutils.is_cv2() \
            else cv2.CAP_PROP_FRAME_COUNT
        total = int(vs.get(prop))
        #print("[INFO] {} total frames in video".format(total))

    # an error occurred while trying to determine the total
    # number of frames in the video file
    except:
        #print("[INFO] could not determine # of frames in video")
        #print("[INFO] no approx. completion time can be provided")
        total = -1

    # loop over frames from the video file stream
    while True:
        # read the next frame from the file
        (grabbed, frame) = vs.read()

        # if the frame was not grabbed, then we have reached the end
        # of the stream
        if not grabbed:
            break

        # if the frame dimensions are empty, grab them
        if W is None or H is None:
            (H, W) = frame.shape[:2]

        # construct a blob from the input frame and then perform a forward
        # pass of the YOLO object detector, giving us our bounding boxes
        # and associated probabilities
        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
                                     swapRB=True, crop=False)
        net.setInput(blob)
        start = time.time()
        layerOutputs = net.forward(ln)
        end = time.time()

        # initialize our lists of detected bounding boxes, confidences,
        # and class IDs, respectively
        boxes = []
        confidences = []
        classIDs = []

        # loop over each of the layer outputs
        for output in layerOutputs:
            # loop over each of the detections
            for detection in output:
                # extract the class ID and confidence (i.e., probability)
                # of the current object detection
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                # filter out weak predictions by ensuring the detected
                # probability is greater than the minimum probability
                if done == False:
                    print('out')
                    done = True
                theConfidence=0.3
                if confidence > theConfidence:
                    print('in')
                    # scale the bounding box coordinates back relative to
                    # the size of the image, keeping in mind that YOLO
                    # actually returns the center (x, y)-coordinates of
                    # the bounding box followed by the boxes' width and
                    # height
                    # box = detection[0:4] * np.array([W, H, W, H])
                    # (centerX, centerY, width, height) = box.astype("int")
                    #
                    # # use the center (x, y)-coordinates to derive the top
                    # # and and left corner of the bounding box
                    # x = int(centerX - (width / 2))
                    # y = int(centerY - (height / 2))
                    #
                    # # update our list of bounding box coordinates,
                    # # confidences, and class IDs
                    # boxes.append([x, y, int(width), int(height)])
                    # confidences.append(float(confidence))
                    # classIDs.append(classID)

        # apply non-maxima suppression to suppress weak, overlapping
        # bounding boxes
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, theConfidence,
                                0.3)

        # ensure at least one detection exists
        if len(idxs) > 0:
            # loop over the indexes we are keeping
            for i in idxs.flatten():
                # extract the bounding box coordinates
                # (x, y) = (boxes[i][0], boxes[i][1])
                # (w, h) = (boxes[i][2], boxes[i][3])
                #
                # # draw a bounding box rectangle and label on the frame
                # color = [int(c) for c in COLORS[classIDs[i]]]
                # cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                # text = "{}: {:.4f}".format(LABELS[classIDs[i]],
                #                            confidences[i])
                # cv2.putText(frame, text, (x, y - 5),
                #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                # #print("Object Detected Array", LABELS[classIDs[i]])

                # print("noOfOccurences",noOfOccurences)
                if (LABELS[classIDs[i]] == 'pistol'):
                    filterVideo = False
                elif (LABELS[classIDs[i]] == 'rifle'):
                    filterVideo = False
                else:
                    filterVideo = True
                if objectsDetected == emptyArray:
                    objectsDetected.append(LABELS[classIDs[i]])
                    # if objectsDetected[0] == LABELS[classIDs[i]]:
                    # objectsDetected[0] =text
                    if noOfOccurences == emptyArray:
                        noOfOccurences.append(1)
                # else:
                # 	noOfOccurences[0]+=1
                # elif objectsDetected[0] != LABELS[classIDs[i]]:
                m = 0
                same = False
                for obj in objectsDetected:

                    if obj == LABELS[classIDs[i]]:
                        noOfOccurences[m] += 1
                        same = True
                    # objectsDetected.append(LABELS[classIDs[i]])
                    # noOfOccurences.append(1)

                    else:
                        m += 1
            if same == False:
                objectsDetected.append(LABELS[classIDs[i]])
                noOfOccurences.append(1)

        # check if the video writer is None
        if writer is None:
            # initialize our video writer
            fourcc = cv2.VideoWriter_fourcc(*"MJPG")
            writer = cv2.VideoWriter('filteredVideo.avi', fourcc, 30,
                                     (frame.shape[1], frame.shape[0]), True)

            # some information on processing single frame
            if total > 0:
                elap = (end - start)
                print("[INFO] single frame took {:.4f} seconds".format(elap))
                print("[INFO] estimated total time to finish: {:.4f}".format(
                    elap * total))

        # write the output frame to disk
        if filterVideo == True:
            writer.write(frame)
            filterVideo = False

    # release the file pointers
    print("[INFO] cleaning up...")
    subprocess.call('ffmpeg -i static/filteredVideo.avi static/filteredVideo.mp4')

    ##
    ## Process the video and extract frequencies and object names from and filer it which is gone to the filtered file directory ###

    # writer.release()
    # #
    # # print (object)
    objectsDetectedmin, objectsDetectedmax = min(objectsDetected), max(objectsDetected)
    for i, val in enumerate(objectsDetected):
        objectsDetected[i] = (val - objectsDetectedmin) / (objectsDetectedmax - objectsDetectedmin)


    global audioArray
    global readingFiles

    audioArraymin, audioArraymax = min(audioArray), max(audioArray)
    for i, val in enumerate(audioArray):
        audioArray[i] = (val - audioArraymin) / (audioArraymax - audioArraymin)
    i=0
    while i<len(audioArray):
        noOfOccurences.append(audioArray[i])
        i+=1
    i = 0
    while i < len(readingFiles):
        objectsDetected.append(readingFiles[i])
        i += 1



    readVideo(objectsDetected,noOfOccurences)


### the user puts the link of the video
@app.route("/putYoutubeUrl",methods=['GET', 'POST'])
def putURL():
    return render_template("putYoutubeUrl.html")

### the user puts the link of the video


### ### getting the video link data and processing it###


@app.route("/getYoutubeUrl",methods=['GET', 'POST'])
def getURL():
    Youtube_path= ''
    if request.method == 'POST':
        #print(request.form['youtubeURL'])
        # print(Youtube_path)
        Youtube_path =request.form['youtubeURL']
        print('Youtube_path: ',Youtube_path)
        ydl_opts = {}
        os.chdir('static/')
        
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            youtubeInformation=ydl.extract_info(Youtube_path)
            #print('youtubeInformation: ',youtubeInformation)
            videoTitle=youtubeInformation.get('title',None)
            videoId=youtubeInformation.get('id',None)
            ydl.download([Youtube_path])

            # print('youtube Title: ',videoTitle)
            # print('test')
            videoPath=os.path.join(videoTitle,'-',videoId,'.mkv')
            videoPath=videoPath.replace("\\", "")
            global globalOriginalVideo
            globalOriginalVideo = str(os.path.basename(videoPath))
            # videoPath=videoPath.replace(" ", "")

            #print('youtube Title with video extension: ',videoPath)

    ############### Classification  of the video link ###############
    ###############
        # success(videoPath)
    processVideoThread = threading.Thread(target=success, args=(videoPath,))  # <- 1 element list
    processVideoThread.start()


    ###############
    ############### Classification  ###############
    #########################Database Youtube URLs #######################################
    ##############
    VideoLinksArray = getRelatedVideosLinks()
    #print("VideoLinksArray: ", VideoLinksArray)
    videoPaths = []

    i = 0
    while i < 3:
        videoPaths.append(VideoLinksArray[i])

        i += 1


    videoNames = ['a', 'b', 'c']
    i = 0
    while i < 3:
        videoNames[i] = ''.join(getYoutubeName(videoPaths[i]))

        i += 1
    # print('vidName3: ',videoNames[2])

    #############
    #########################Database Youtube URLs #########################################


    return render_template("getYoutubeUrl.html",youtubeURL=videoTitle,ThePath=videoPaths[0],ThePath2=videoPaths[1],ThePath3=videoPaths[2],
                           videoName=videoNames[0],videoName2=videoNames[1],videoName3=videoNames[2])

### getting the video link data and processing it###




if __name__ == "__main__":
    app.run(debug=True)