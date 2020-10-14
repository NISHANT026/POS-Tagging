import csv
import xml.etree.ElementTree as ET
import os

def loadFile(fileName):
    print('a')
worddict =	{}
tagdict =	{}

def parseXML():
 files = ["A1", "A2", "A3","A4","A5","A6","A7", "A8", "A9","AA","AB","AC","AD", "AH", "AJ","AK","AL","AM"]
 
 for x in files:
   path = '../Train-corups/'+x

   for filename in os.listdir(path):
    if not filename.endswith('.xml'): continue
    fullname = os.path.join(path, filename)
    #print("\n")
    #print(filename)
    tree = ET.parse(fullname)
    # tree = ET.parse(xmlFile)
    root = tree.getroot()
    words = []
    for word in root.iter('w'):
        wo=word.get('hw')
        wo = word.text
        if(wo[len(wo)-1] == ' ') or (wo[len(wo)-1] == '\n'):
            wo = wo[:len(wo)-1]
        wo = wo.lower()
        #print(word.text)
        #print(len(word.text))
        ta=word.get('c5')
        ta1 = ta
        ta2 = None
        if len(ta)>3:
            ta1 = ta[:3]
            ta2 = ta[4:]
        else:
            ta2 = None
        encoding=wo+"_"+ta
       # print(wo)
        if not wo in worddict:
         worddict[wo]=1
        else:
         worddict[wo]+=1
        if not ta1 in tagdict:
         tagdict[ta1]=1
        else:
         tagdict[ta1]+=1
        if ta2 != None:
            if not ta2 in tagdict:
                tagdict[ta2]=1
            else:
                tagdict[ta2]+=1
        # encoding = word.get('hw') + " " + word.get('c5')
        # Word[wo]+=1
        #Tag[ta]+=1
        words.append(encoding)
        #print(encoding)
parseXML()
#print(worddict)
#print(tagdict)
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


 

