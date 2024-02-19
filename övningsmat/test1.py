import zipfile
import os
import sqlite3  # Correct module name for accessing SQLite databases
import gzip
import blackboxprotobuf  # Assuming blackboxprotobuf has been successfully installed


filePath = ""
tempFolder = "./temp"

openZIP = zipfile.ZipFile(filePath, mode="r")

for filename in openZIP.namelist():
    if "NoteStore.sqlite" in filename:
        print("NotesStore found: ", filename)
        localFileName = filename.rsplit("/", 1)[-1]