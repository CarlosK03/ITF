import zipfile

#extractionPath = "Users/TheKi/ITF"

extractionPath = "OneDrive_4_2-19-2024.zip"

openedZipfile = zipfile.ZipFile(extractionPath, mode="r")

for filelocation in openedZipfile.namelist():
    print("File: ", filelocation)
    
    
for filelocation in openedZipfile.namelist():
    if "bingo" in filelocation:
        print("Found:", filelocation)
        print("File contents:")
        print(openedZipfile.read(filelocation).decode("utf-8"))