import zipfile

#extractionPath = "Users/TheKi/ITF"

extractionPath = "OneDrive_4_2-19-2024.zip"

openedZipfile = zipfile.ZipFile(extractionPath, mode="r")

for filename in openedZipfile.namelist():
    print("File: ", filename)
    
    
for filename in openedZipfile.namelist():
    if "bingo" in filename:
        print("Found:", filename)
        print("File contents:")
        print(openedZipfile.read(filename).decode("utf-8"))