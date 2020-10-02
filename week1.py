import csv
import xml.etree.ElementTree as ET

def loadFile(fileName):
    print('a')

def parseXML(xmlFile):
    tree = ET.parse(xmlFile)
    root = tree.getroot()
    words = []
    for word in root.iter('w'):
        encoding = word.get('hw') + "_" + word.get('c5')
        words.append(encoding)
        print(encoding)


parseXML("../Test-corpus/AP/AP1.xml")


