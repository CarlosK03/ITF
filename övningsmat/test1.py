import zipfile
import os
import sqlite3  # Correct module name for accessing SQLite databases
import gzip
import blackboxprotobuf  # Assuming blackboxprotobuf has been successfully installed


filePath = "C:/Users/TheKi/Downloads/Telefon2-GalaxyS21/CellebriteCTF23SharonGalaxyS21.zip"
tempFolder = "./temp"

openZIP = zipfile.ZipFile(filePath, mode="r")

for filename in openZIP.namelist():
    if "NoteStore.sqlite" in filename:
        print("NotesStore found: ", filename)
        localFileName = filename.rsplit("/", 1)[-1]
        print("Saving file: ", localFileName)
        with open(os.path.join(tempFolder, localFileName), 'wb') as localFile:
            localFile.write(openZIP.read(filename))
            
sqliteDatabase = os.path.join(tempFolder, "NoteStore.sqlite")

sqliteConnection=sqlite3.connect(sqliteDatabase)

sqliteCursor = sqliteConnection.cursor()

sqliteQ = "SELECT ZDATA FROM ZICNOTEDATA;"

sqliteCursor.execute(sqliteQ)

sqliteResult = sqliteCursor.fetchall()
print(sqliteResult)

sqliteBLOB1 = sqliteResult[0][0]

print(sqliteBLOB1)

decompressedBLOB = gzip.decompress(sqliteBLOB1)

print(decompressedBLOB)

decodedDecompressedProtobufBLOB = blackboxprotobuf.decode_message(decompressedBLOB)
print(decodedDecompressedProtobufBLOB)

        