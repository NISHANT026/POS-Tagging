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
   path = 'Train-corpus/'+x

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
        ta=word.get('c5')
        encoding=wo+"_"+ta
       # print(wo)
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
        else:
            if not wo in worddict:
             worddict[wo]=1
            else:
             worddict[wo]+=1
            if not ta in tagdict:
             tagdict[ta]=1
            else:
             tagdict[ta]+=1
        # encoding = word.get('hw') + " " + word.get('c5')
        # Word[wo]+=1
        #Tag[ta]+=1
        words.append(encoding)
      #  print(ta)
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

#print(worddict["that"])
 
