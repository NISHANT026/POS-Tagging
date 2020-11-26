import csv
import xml.etree.ElementTree as ET
import os
import numpy as np
from collections import defaultdict
import multiprocessing
import time
import pickle


worddict = {}
tagdict = {}
totalTags = 0

tagDictPerWord = {}

tagIds = {}
tagIdsRev = {}

initialProb = {}
transitionProb = {}
emissionProb = {}


def updateTagdict(ta, t2 = ''):
    global tagdict
    if not ta in tagdict:
        tagdict[ta]=1
    else:
        tagdict[ta]+=1
    if t2 != '':
        if not t2 in tagdict:
            tagdict[t2]=1
        else:
            tagdict[t2]+=1


def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


def calculateTransitionProb():
    global transitionProb
    for tag in transitionProb:
        total = 0
        for nextTag in transitionProb[tag]:
            total += transitionProb[tag][nextTag]
        for nextTag in transitionProb[tag]:
            transitionProb[tag][nextTag] = transitionProb[tag][nextTag]/total


def calculateEmissionProb():
    global emissionProb
    for word in tagDictPerWord:
        total = 0
        emissionProb[word] = {}
        for tag in tagDictPerWord[word]:
            total += tagDictPerWord[word][tag]
        for tag in tagDictPerWord[word]:
            emissionProb[word][tag] = tagDictPerWord[word][tag]/total


def calculateInitialProb():
    global initialProb
    for key in tagdict.keys():
        initialProb[key] = tagdict[key]#/totalTags
        #TODO: try for prob and freq!
            

def updateWorddict(wo):
    global worddict
    if not wo in worddict:
        worddict[wo]=1
    else:
        worddict[wo]+=1


def updateTagDictPerWord(wo, ta, t2 = ''):
    global tagDictPerWord
    if not wo in tagDictPerWord:
        tagDictPerWord[wo] = {ta: 1}
    else:
        if not ta in tagDictPerWord[wo]:
            tagDictPerWord[wo][ta] = 1
        else:
            tagDictPerWord[wo][ta] += 1
    if t2 != '':
        if not t2 in tagDictPerWord[wo]:
            tagDictPerWord[wo][t2] = 1
        else:
            tagDictPerWord[wo][t2] += 1


def updateTransitionFreq(prevTag, ta, prevTag2 = '', t2 = ''):
    global transitionProb
    if prevTag != '':
        if not prevTag in transitionProb:
            transitionProb[prevTag] = {ta: 1}
        else:
            if not ta in transitionProb[prevTag]:
                transitionProb[prevTag][ta] = 1
            else:
                transitionProb[prevTag][ta] += 1

            if t2 != '':
                if not t2 in transitionProb[prevTag]:
                    transitionProb[prevTag][t2] = 1
                else:
                    transitionProb[prevTag][t2] += 1
    if prevTag2 != '':
        if not prevTag2 in transitionProb:
            transitionProb[prevTag2] = {ta: 1}
        else:
            if not ta in transitionProb[prevTag2]:
                transitionProb[prevTag2][ta] = 1
            else:
                transitionProb[prevTag2][ta] += 1

            if t2 != '':
                if not t2 in transitionProb[prevTag2]:
                    transitionProb[prevTag2][t2] = 1
                else:
                    transitionProb[prevTag2][t2] += 1


def parseXML():
    global tagdict, worddict, tagDictPerWord, initialProb, transitionProb, emissionProb
    try:
        tagdict = load_obj("tagdict")
        worddict = load_obj("worddict")
        tagDictPerWord = load_obj("tagDictPerWord")
        transitionProb = load_obj("transitionProb")
        emissionProb = load_obj("emissionProb")
        initialProb = load_obj("initialProb")
    except:
        files = ["A1", "A2", "A3","A4","A5","A6","A7", "A8", "A9","AA","AB","AC","AD", "AH", "AJ","AK","AL","AM"]
        global totalTags
        for x in files:
            path = 'Train-corpus/'+x

            for filename in os.listdir(path):
                if not filename.endswith('.xml'): continue
                fullname = os.path.join(path, filename)
    
                tree = ET.parse(fullname)
                prevTag = ''
                prevTag2 = ''
                root = tree.getroot()
                for element in root.iter():
                    if element.tag == "w":
                        word = element
                        wo = word.text
                        wo = wo.lower()
                        if wo[len(wo)-1] == " ":
                            wo = wo[:len(wo)-1]
                        ta=word.get('c5')

                        updateWorddict(wo)

                        if (ta.find('-') !=-1):
                            t1=ta[0:3]
                            t2=ta[-3:]

                            updateTagdict(t1, t2)
                            totalTags += 2

                            updateTagDictPerWord(wo, t1, t2)

                            updateTransitionFreq(prevTag, t1, prevTag2, t2)
                            prevTag = t1
                            prevTag2 = t2
        
                        else:
                            updateTagdict(ta)
                            totalTags += 1

                            updateTagDictPerWord(wo, ta)                        

                            updateTransitionFreq(prevTag, ta, prevTag2)
                            prevTag = ta
                            prevTag2 = ''

                    elif element.tag == 'c':
                        if element.text.strip() == '.':
                            prevTag = ''
                            prevTag2 = ''

        calculateEmissionProb()
        calculateTransitionProb()
        calculateInitialProb()

        save_obj(tagdict, "tagdict")
        save_obj(worddict, "worddict")
        save_obj(tagDictPerWord, "tagDictPerWord")
        save_obj(emissionProb, "emissionProb")
        save_obj(transitionProb, "transitionProb")
        save_obj(initialProb, "initialProb")


def setTagIds():
    global tagIds
    tagId = 0
    if tagIds == {}:
        for key in tagdict.keys():
            tagIds[key] = tagId
            tagIdsRev[tagId] = key
            tagId += 1


def getEmissionProb(word, tag):
    global emissionProb
    #TODO: recheck for new word case
    if word not in emissionProb:
        return initialProb[tag]
    else:
        if tag not in emissionProb[word]:
            return 0
        else:
            return emissionProb[word][tag]


def getTransitionProb(prevTag, tag):
    global transitionProb
    if tag not in transitionProb[prevTag]:
        return 0
    else:
        return transitionProb[prevTag][tag]


def HMMViterbi(sentence):
    tagSeq = []

    viterbiMatrix = [[0 for t in range(len(sentence))] for n in range(len(tagdict.keys()))]
    backPointer = [[0 for t in range(len(sentence))] for n in range(len(tagdict.keys()))]
    
    for tag in tagdict.keys():
        backPointer[tagIds[tag]][0] = 0
        viterbiMatrix[tagIds[tag]][0] = initialProb[tag] * getEmissionProb(sentence[0], tag)
    for t in range(1, len(sentence)):
        for tag in tagdict.keys():
            maxViterbi = 0
            maxTag = ''
            for prevTag in tagdict.keys():
                val = viterbiMatrix[tagIds[prevTag]][t-1] * getTransitionProb(prevTag, tag) * getEmissionProb(sentence[t], tag)

                if val > maxViterbi:
                    maxViterbi = val
                    maxTag = prevTag
            viterbiMatrix[tagIds[tag]][t] = maxViterbi
            if maxTag != '': 
                backPointer[tagIds[tag]][t] = tagIds[maxTag]
            else:
                backPointer[tagIds[tag]][t] = -1
    maxViterbi = 0
    maxTag = ''

    for tag in tagdict.keys():
        val = viterbiMatrix[tagIds[tag]][len(sentence)-1]
        if val > maxViterbi:
            maxViterbi = val
            maxTag = tag
    bestPathProb = maxViterbi
    bestPathPointer = tagIds[maxTag]

    tagSeq = []
    for i in range(len(sentence)):
        tagSeq.append(tagIdsRev[bestPathPointer])
        bestPathPointer = backPointer[bestPathPointer][len(sentence)-1-i]

    tagSeq.reverse()
    return tagSeq


def viterbiParallelCall(map):
    sentence = map["sentence"] 
    actualTagSeq = map["actualTagSeq"]
    total = 0
    correct = 0
    try:
        predictedTagSeq = HMMViterbi(sentence)
        for i in range(len(predictedTagSeq)):
            total += 1
            if actualTagSeq[i].find(predictedTagSeq[i]) != -1:
                correct +=1
        return total, correct
    except:
        return 0,0


def runHMMonTestData():
    correct = 0
    total = 0
    files = ["AN", "AP", "AR","AS","AT","AY"]
    errors = 0

    for x in files:
        path = 'Test-corpus/'+x

        for filename in os.listdir(path):
            if not filename.endswith('.xml'): continue
            fullname = os.path.join(path, filename)
    
            tree = ET.parse(fullname)

            root = tree.getroot()
            maps = []
            sentence = []
            actualTagSeq = []
            for element in root.iter():

                if element.tag == 'w':
                    word = element
                    wo = word.text
                    wo = wo.lower().strip()
                    ta=word.get('c5')

                    sentence.append(wo)
                    actualTagSeq.append(ta)

                elif element.tag == 'c': 
                    if element.text != None:
                        if element.text.strip() == '.':
                            maps.append({"sentence" : sentence, "actualTagSeq" : actualTagSeq})
                            sentence = []
                            actualTagSeq = []
                
    pool = multiprocessing.Pool() 
    outputs_async = pool.map_async(viterbiParallelCall, maps)
    outputs = outputs_async.get()
    for i in range(len(outputs)):
        total += outputs[i][0]
        correct += outputs[i][1]
                    
    print(correct/total*100)



def main():
    parseXML()
    setTagIds()

    runHMMonTestData()
    # HMMViterbi(['rishi', 'is', 'happy'])


main()
