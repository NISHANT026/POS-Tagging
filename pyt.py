import csv
import xml.etree.ElementTree as ET
import os
import numpy as np
from collections import defaultdict
worddict = {}
tagdict = {}
tagDictPerWord = {}

def parseXML():
    files = ["A1", "A2", "A3","A4","A5","A6","A7", "A8", "A9","AA","AB","AC","AD", "AH", "AJ","AK","AL","AM"]
 
    for x in files:
        path = 'Train-corpus/'+x

        for filename in os.listdir(path):
            if not filename.endswith('.xml'): continue
            fullname = os.path.join(path, filename)
   
            tree = ET.parse(fullname)

            root = tree.getroot()
            words = []
            for word in root.iter('w'):
                #wo=word.get('hw')
                wo = word.text
                wo = wo.lower()
                if wo[len(wo)-1] == " ":
                    wo = wo[:len(wo)-1]
                ta=word.get('c5')
                encoding=wo+"_"+ta

                if (ta.find('-') !=-1):
                    t1=ta[0:3]
                    t2=ta[-3:]
                    #print(encoding,t1,t2)
                    if not t1 in tagdict:
                        tagdict[t1]=1
                    else:
                        tagdict[t1]+=1
                    if not t2 in tagdict:
                        tagdict[t2]=1
                    else:
                        tagdict[t2]+=1

                    if not wo in tagDictPerWord:
                        tagDictPerWord[wo] = {t1: 1, t2: 1}
                    else:
                        if not t1 in tagDictPerWord[wo]:
                            tagDictPerWord[wo][t1] = 1
                        else:
                            tagDictPerWord[wo][t1] += 1
                        if not t2 in tagDictPerWord[wo]:
                            tagDictPerWord[wo][t2] = 1
                        else:
                            tagDictPerWord[wo][t2] += 1

                else:
                    if not wo in worddict:
                        worddict[wo]=1
                    else:
                        worddict[wo]+=1
                    if not ta in tagdict:
                        tagdict[ta]=1
                    else:
                        tagdict[ta]+=1

                    if not wo in tagDictPerWord:
                        tagDictPerWord[wo] = {ta: 1}
                    else:
                        if not ta in tagDictPerWord[wo]:
                            tagDictPerWord[wo][ta] = 1
                        else:
                            tagDictPerWord[wo][ta] += 1
        
        words.append(encoding)
        
def printTop10():
    print("Word")
    for x in range(10):
        Keymax = max(worddict, key=worddict.get)
        print(Keymax,worddict[Keymax])
        del worddict[Keymax] 
    
    print("\n") 
    print("Tag")
    for x in range(10): 
        Key = max(tagdict, key=tagdict.get)
        print(Key,tagdict[Key])
        del tagdict[Key]


def findMostProbTag(tagFreqMap):
    mostFreqTag = ''
    freq = 0
    for key, val in tagFreqMap.items():
        if val > freq:
            mostFreqTag = key
            freq = val

    return mostFreqTag


def runOnTestData():
    correct = 0
    total = 0
    files = ["AN", "AP", "AR","AS","AT","AY"]

    confusionmatrix=defaultdict(lambda:defaultdict(int))
    for x in files:
        path = 'Test-corpus/'+x

        #for filename in os.listdir(path):
         #if not filename.endswith('.xml'): continue
         #fullname = os.path.join(path, filename)
        for filename in os.listdir(path):
            if not filename.endswith('.xml'): continue
            fullname = os.path.join(path, filename)
    
            tree = ET.parse(fullname)

            root = tree.getroot()
            words = []
            mostPropTag = ''
            for word in root.iter('w'):
                #wo=word.get('hw')
                total += 1
                wo = word.text
                wo = wo.lower()
                if wo[len(wo)-1] == " ":
                    wo = wo[:len(wo)-1]
                ta=word.get('c5')

                if (ta.find('-') !=-1):
                    t1=ta[0:3]
                    t2=ta[-3:]
                    actual1=t1
                    actual2=t2 
                    if not wo in tagDictPerWord:
                        if ta.find("NN1") != -1:
                            correct += 1
                        predicted="NN1"
                        confusionmatrix[actual1][predicted]+=1
                        confusionmatrix[actual2][predicted]+=1

                           # print(correct)
                    else:
                        mostProbTag = findMostProbTag(tagDictPerWord[wo])
                        if t1 == mostProbTag: 
                            correct += 1
                        predicted=mostProbTag
                        confusionmatrix[actual1][predicted]+=1
                        if t2 == mostProbTag:
                            correct += 1
                        predicted=mostProbTag
                        confusionmatrix[actual2][predicted]+=1  

                else:
                    actual=ta
                    if not wo in tagDictPerWord:
                        if ta == "NN1":
                            correct += 1
                        predicted="NN1"
                        confusionmatrix[actual][predicted]+=1
                    else:
                        mostProbTag = findMostProbTag(tagDictPerWord[wo])
                        if ta == mostProbTag:
                            correct += 1
                        predicted=mostProbTag
                        confusionmatrix[actual][predicted]+=1	
    total_=0
    correct_=0
    accuracy_=0

    for i in  confusionmatrix:
        for j in confusionmatrix[i]:
            total_ += confusionmatrix[i][j]
        correct_ += confusionmatrix[i][i]
	#print("\n")
    prettymaxtrix=[]
    for tagi,freqi in tagdict.items(): 
        temp=[]
        for tagj,freqj in tagdict.items():
            temp.append(confusionmatrix[tagi][tagj])
        prettymaxtrix.append(temp)
    #print(prettymaxtrix)
 	
    accuracy_=correct_*100
    acc=correct*100
    print(acc/total)
    print(correct)
    print(total)
    #print(correct/total)
    print(prettymaxtrix)


def main():
    parseXML()
   # printTop10()
    runOnTestData()


main()
