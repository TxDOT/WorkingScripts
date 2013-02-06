
import csv
import os

Directory = #Insert File Path Here
fileList = []
dirList = os.listdir(Directory)
for files in dirList:
    if files.endswith('NEW.csv'):
        fileList.append(files)

for fname in fileList:
    print fname
    csvOld = Directory + fname
    with open(csvOld,'rb') as csvfile:
        newFile = csvOld.strip('_NEW.csv') + '.csv'
        FILE1 = open(newFile,"w")
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            string = str(row)
            newString = string.replace("None"," ")
            for element in newString:
                FILE1.write(element.strip('[]"\''))
            FILE1.write("\n")
    FILE1.close()
