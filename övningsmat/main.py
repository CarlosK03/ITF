import zipfile

#extractionPath = "x"

extractionPath = "x"

openedZipfile = zipfile.ZipFile(extractionPath, mode="r")

for filelocation in openedZipfile.namelist():
    print("File: ", filelocation)
    
    
for filelocation in openedZipfile.namelist():
    if "bingo" in filelocation:
        print("Found:", filelocation)
        print("File contents:")
        print(openedZipfile.read(filelocation).decode("utf-8"))
