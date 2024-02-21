import zipfile
import os
import sqlite3  
import gzip
import blackboxprotobuf  


filePath = r"K:/TheProjectAIF/ITF/S21.zip"
dbFolder = "./temp"

#openZIP = zipfile.ZipFile(filePath, mode="r")
openedZipfile = zipfile.ZipFile(filePath, mode="r")

for filelocation in openedZipfile.namelist():
    print("File: ", filelocation)

#for filelocation in openZIP.namelist():
#    if "NoteStore.sqlite" in filelocation:
#        print("NotesStore found: ", filelocation)
#        localfilelocation = filelocation.rsplit("/", 1)[-1]
#        print("Saving file: ", localfilelocation)
#        with open(os.path.join(dbFolder, localfilelocation), 'wb') as localFile:
#            localFile.write(openZIP.read(filelocation))
            
#sqliteDatabase = os.path.join(dbFolder, "NoteStore.sqlite")

#sqliteConnection=sqlite3.connect(sqliteDatabase)

#sqliteCursor = sqliteConnection.cursor()

#sqliteQ = "SELECT ZDATA FROM ZICNOTEDATA;"

#sqliteCursor.execute(sqliteQ)

#sqliteResult = sqliteCursor.fetchall()
#print(sqliteResult)

#sqliteBLOB1 = sqliteResult[0][0]

#print(sqliteBLOB1)

#decompressedBLOB = gzip.decompress(sqliteBLOB1)

#print(decompressedBLOB)

#decodedDecompressedProtobufBLOB = blackboxprotobuf.decode_message(decompressedBLOB)
#print(decodedDecompressedProtobufBLOB[0]["2"]["3"]["2"].decode("utf-8"))

        