#Mobile Recommendation System 

#Requirements:Python, eel, browser
#NOTE: You need chrome browser if you want to run this project
# If you dont use chrome then specify your browser according to eel docs.

import eel
import json
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

@eel.expose
def recieveDataToPython(jsToPy):
    #this function is acessible from js
    # print("Hellow,Function called from js")
    print(jsToPy)
    # print(jsToPy['ram'])
    # 0) Get user data and make a df
    data={
    "Name":['User Req name'],
    "Rating":[jsToPy['rating']],
    "Price Rs":[jsToPy['budget']],
    "RAM Gb":[jsToPy['ram']],
    "ROM Gb":[jsToPy['rom']],
    "Expandable GB":[' '],
    "Size Cm":[' '],
    "Size Inch":[jsToPy['size']],
    "R1 Cam MP":[jsToPy['camera']],
    "R2 Cam MP":[' '],
    "R3 Cam MP":[' '],
    "R4 Cam MP":[' '],
    "Battery Mah":[jsToPy['battery']],
    "Processor":' ',
    "Image":' '
    }
    userDf=pd.DataFrame(data)
    #1)Read the dataset
    df=pd.read_csv('mainDataset.csv',encoding= 'unicode_escape')
    # print (df.columns)

    # 1.1)Append the dataframe
    df=userDf.append(df,ignore_index = True)
   

    #2)Select Features
    # features=['Price Rs','Rating','RAM Gb','ROM Gb','Size Inch','R1 Cam MP','Battery Mah']

    # 3)Create a column which will contain all these feat
    def combineFeatures(row):
        return str(row['Price Rs'])+" "+str(row['RAM Gb'])+" "+str(row['ROM Gb'])+" "+str(row['Size Inch'])+" "+str(row['R1 Cam MP'])+" "+str(row['Battery Mah'])
    # this will create a seperate colm of combined features
    df["combinedFeatures"]=df.apply(combineFeatures,axis=1)
    # print (df['combinedFeatures'].head())


    # 4) Now find the index which is more similar to our requirement
    # now use cosine similarity
    # create an object of countVectorizer
    cv=CountVectorizer()
    countMatrix=cv.fit_transform(df['combinedFeatures'])
    # print (countMatrix).toarray()
    similar=cosine_similarity(countMatrix)
    similarPhones=list(enumerate(similar[0]))
    # print (similarPhones)

    # 5)Now sort the entries acc to similarity scores
    sortedSimilarPhones=sorted(similarPhones,key=lambda x:x[1], reverse=True)
    # print (sortedSimilarPhones)
    # Now print the most similar 5 phones
  
    x=0
    pyToJs={}
    for phone in sortedSimilarPhones:
        if (df[df.index==phone[0]]['Name'].values[0]=='User Req name'):
            pass
        else:
            pyToJs[df[df.index==phone[0]]['Name'].values[0]]={
            'size':str(df[df.index==phone[0]]['Size Inch'].values[0]),
            'ram':str(df[df.index==phone[0]]['RAM Gb'].values[0]),
            'rom':str(df[df.index==phone[0]]['ROM Gb'].values[0]),
            'camera':df[df.index==phone[0]]['R1 Cam MP'].values[0],
            'budget':df[df.index==phone[0]]['Price Rs'].values[0],
            'processor':df[df.index==phone[0]]['Processor'].values[0],
            'rating':df[df.index==phone[0]]['Rating'].values[0],
            'image':df[df.index==phone[0]]['Image'].values[0],
            'battery':str(df[df.index==phone[0]]['Battery Mah'].values[0]),    
            }
        #   
        x=x+1
        if(x==10):
            break
 # new code ends 
      # send back to frontend

    eel.recieveBackToJs(pyToJs) 
eel.init("GUI")
eel.start('index.html',size=(1000,700),port=8090)
