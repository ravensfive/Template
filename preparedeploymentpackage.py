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
zipfile("InteractionControl.py")



