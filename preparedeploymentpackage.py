# import packages
import zipfile
import os
from zipfile import ZipFile

# delete zip from drive
def deletezip():
    os.remove("twtd.zip")
    print("Zip File Deleted")

#deletezip()

# zip up file into a zip archive, ready for Lambda Upload
def zipfile(file):
  
   zipf = ZipFile("twtd.zip","a")
   zipf.write(file)

   zipf.close()

   print(file + " zipped")

# calls for individuals files - these need to be listed as files 

#zipfile("InteractionControl.py")

def listfiles():
    # get current file list
    filelist = os.listdir("/Users/stevengooday/Desktop/Alexa/TWTD")
    # for each file in the list 
    for file in filelist:
        # test if the file is directory, if it is loop that directory
        if os.path.isdir(file) == True:
                filelist2 = os.listdir("/Users/stevengooday/Desktop/Alexa/TWTD")
                zipfile(file)     
            

# loop around all file
# listfiles()
def traverseDirectory():
    rootDir = '/Users/stevengooday/Desktop/Alexa/TWTD'
    for dirName, subdirList, fileList in os.walk(rootDir, topdown=False):
        for fname in fileList:
            print('\t%s' % fname)
            zipfile(fname)
traverseDirectory()