import mysql.connector

import statistics
import numpy as np
from sklearn.cluster import SpectralClustering
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
from scipy import spatial
import numpy as np
from copy import copy, deepcopy
from sklearn.metrics import pairwise_distances
from scipy.spatial.distance import cosine

db_connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    passwd="",
    database="rec_system"
)
my_database = db_connection.cursor()

mycursor = db_connection.cursor()
Total=[]
sql="SELECT COUNT(*) FROM movie"
mycursor.execute(sql)
mainResult = mycursor.fetchall()
print(mainResult[0][0])
arrayOfArrays=[[] for _ in range(mainResult[0][0])]
NoOfOccurencesTotal=[[] for _ in range(mainResult[0][0])]
arrayOfArraysFrequency=[[] for _ in range(mainResult[0][0])]
sortedFreq = [[] for _ in range(mainResult[0][0])]

noOfClusters=3
clustersOrder=[[] for _ in range(noOfClusters)]
seperatedCosineSimilarity=[[] for _ in range(mainResult[0][0])]

##Get the most video similar to all videos in the same clusters##
def getClusterHeads(clusterIdArray,similarities):
    clusterIdCounter=0
    row=0
    # print('cluster Id 0: ', clusterIdArray.index(0))
    while clusterIdCounter <noOfClusters:
        i, = np.where(clusterIdArray == clusterIdCounter)  # integers
        clustersOrder[clusterIdCounter]=i.tolist()

        # print(i)
        clusterIdCounter+=1
    print('clustersOrder: ',clustersOrder)

    rowCounter1 = 0
    seperatedCosineSimilarity = similarities.tolist()
    while rowCounter1 <mainResult[0][0]:
        # print('rowCounter: ',rowCounter1)
        # seperatedCosineSimilarity[rowCounter1].pop(rowCounter1)
        seperatedCosineSimilarity[rowCounter1][rowCounter1]=0

        rowCounter1+=1

    print(seperatedCosineSimilarity)
#########################################################################################################
    # withoutSamePoint=mainResult[0][0]-1  # without the 1.0 between every video and itself [A relation with A 1.0 (cosine similarity)]
    clusterOrderCounter = 0
    removed = -1

    # print('withoutSamePoint: ',withoutSamePoint)
    while clusterOrderCounter<noOfClusters:
        seperatedCosineSimilarityEachCluster=deepcopy(seperatedCosineSimilarity) #for every Cluster
        notInClusterArray=[]
        notInClusterCounter=0 # element which weren't in the cluster
        while notInClusterCounter<mainResult[0][0]:
            if notInClusterCounter in clustersOrder[clusterOrderCounter]:
                notInClusterCounter += 1
            else:
                notInClusterArray.append(notInClusterCounter)
                notInClusterCounter += 1
#########################################################################################################

            # print('notInClusterCounter: ',notInClusterCounter)
        print('notInClusterArray: ', notInClusterArray)
        notInClusterArrayCounter=0 # loop on the on every row in the notInClusterArray in every clusterOrderCounter (when clusterOrderCounter in 0,1,2)
        print('removed in the first: ',removed)

        while notInClusterArrayCounter<len(notInClusterArray):
            elementCounter = 0
            while elementCounter < mainResult[0][0]:

                seperatedCosineSimilarityEachCluster[elementCounter][notInClusterArray[notInClusterArrayCounter]]=0
                seperatedCosineSimilarityEachCluster[notInClusterArray[notInClusterArrayCounter]][elementCounter]=0

                elementCounter += 1

            notInClusterArrayCounter += 1

        removed = removed-1
##############################Getting Average Values ########################################################
        print('removed in last: ',removed)
        print('seperatedCosineSimilarityEachCluster: ', seperatedCosineSimilarityEachCluster)
        # print('len(seperatedCosineSimilarityEachCluster): ',len(seperatedCosineSimilarityEachCluster[0]),' in cluster ',clusterOrderCounter)
        # print('seperatedCosineSimilarity: ',seperatedCosineSimilarity)
        eachClusterArrayLength=len(seperatedCosineSimilarityEachCluster)
        averageCounter=0
        averageValues=[]
        while averageCounter<eachClusterArrayLength:
            averageValues.append(statistics.mean(seperatedCosineSimilarityEachCluster[averageCounter]))
            averageCounter+=1
        print('Average Values',averageValues)
        i=0
        maxAverage=0
        while i<len(averageValues):
            if maxAverage<averageValues[i]:
                maxAverage=averageValues[i]
            i+=1
        print('maxAverage: ',maxAverage)
        i=0
        maxAverageIndex = 0
        while i < len(averageValues):
            if maxAverage == averageValues[i]:
                maxAverageIndex=i
            i+=1
        print('max Average Index: ',maxAverageIndex)
        maxAverageId=maxAverageIndex+1 # because array begins at index 0 and the database begins at ID 1
        updateClusterHeadsDB(movieId=maxAverageId)





##############################Getting Average Values ########################################################

        clusterOrderCounter+=1
        print('clusterOrderCounter: ',clusterOrderCounter)





##############################Updating Cluster Heads Values in DB ########################################################

def updateClusterHeadsDB(movieId):



    sql = "UPDATE movie SET clusterHead = %s WHERE ID = %s"
    val = (0, movieId)
    # val = (-1, i)
    mycursor.execute(sql, val)
    db_connection.commit()

    print(mycursor.rowcount, "Cluster Id successfully updated")

def updateclusterId(clusterIdArray,similarities):

    i=1
    col=0 # every element in the spectral cluster resulted array
    while col<mainResult[0][0]:

        sql = "UPDATE movie SET clusterId = %s WHERE ID = %s"
        val = (int(clusterIdArray[col]), i)
        # val = (-1, i)
        mycursor.execute(sql, val)
        db_connection.commit()
        i+=1
        col+=1

        print(mycursor.rowcount, "Cluster Id successfully updated")
    getClusterHeads(clusterIdArray,similarities)


def spectralClustering(similarities):
    sc = SpectralClustering(noOfClusters, affinity='precomputed', n_init=100)
    sc.fit_predict(similarities)
    print('spectral clustering')
    print(sc.labels_)
    clusterIdArray=sc.labels_
    updateclusterId(clusterIdArray,similarities)
def cosineSimilarity(sortedFreq):
    dist_out = 1 - pairwise_distances(sortedFreq, metric="cosine")

    spectralClustering(dist_out)


def read():
    same=False
    movieId = 12
    i = 0
    movieClusterIds = []
    print('movieClusterIds: ',len(movieClusterIds))
    while(True):
        if i >= mainResult[0][0]:
            break
        mycursor.execute("SELECT * FROM processed WHERE `MovieID`="+str(movieId))
        myresult = mycursor.fetchall()
        # print(myresult)
        # Tenet=0
        for x in myresult:

             #print (x)


             # print(x[2])
             # print(i)
             arrayOfArrays[i].append(x[2])
                # objectsDetected2.append(x[2])
                # noOfOccurences2.append(x[3])
             arrayOfArraysFrequency[i].append(x[3])

        movieId+=1
        i += 1
        # print(movieId)

    print('arrayOfArraysFrequency: ',arrayOfArraysFrequency)
    print('arrayOfArrays: ',arrayOfArrays)

    # print(objectsDetected2)
    # print(noOfOccurences2)

    # mycursor.execute("SELECT * FROM processed WHERE `MovieID`="+str(movieId2))
    # myresult = mycursor.fetchall()
    # Tenet=0
    # for x in myresult:
    #     # print(x[2])
    #
    #         objectsDetected3.append(x[2])
    #         noOfOccurences3.append(x[3])
    #         arrayOfArrays[1].append(x[2])
    #         arrayOfArraysFrequency[1].append(x[3])
    #
    #
    # print('objectsDetected3: ',objectsDetected3)
    # print('noOfOccurences3: ',noOfOccurences3)

    # Total.append(objectsDetected2)
    mint = 0
    # for y in arrayOfArrays[mint]:
    #
    #     # Total.append(objectsDetected3[mint])
    #     mint+=1
    # print(mint)
    while True:
        if mint>=mainResult[0][0]:
            break
        for z in arrayOfArrays[mint]:
            for zzz in Total:
                if z == zzz:
                    same = True
            if same == False:
                Total.append(z)
            same = False
        mint+=1


    # print('Total= ',Total)
    tint=0
    # print(mainResult[0][0])
    # print('Total: ',len(Total))
    # print(Total)
    i = 0
    while True:


        if(i<=len(Total)):
            NoOfOccurencesTotal[tint].append(0)
        elif(i>len(Total)):
            i=0
            tint += 1

        i+=1
        if tint >=mainResult[0][0]:
                break
    #     NoOfOccurencesTotal2.append(0)
    i = 0
    # j = 0
    print("------------------------")

    print("Total: ", Total)
    # print(NoOfOccurencesTotal[2])

    print("------------------------")

    obj=0
    while obj<len(Total):
        moviesCount = 0
        while moviesCount<mainResult[0][0]:
            Founder=0
            value=0
            while Founder<len(arrayOfArrays[moviesCount]):
                if Total[obj]==arrayOfArrays[moviesCount][Founder]:
                    value=arrayOfArraysFrequency[moviesCount][Founder]
                    break

                Founder += 1
            sortedFreq[moviesCount].append(value)
            moviesCount+=1

        obj+=1


    print(sortedFreq)
    cosineSimilarity(sortedFreq)










read()
