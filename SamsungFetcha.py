import zipfile, sqlite3, csv, io, os, gzip, blackboxprotobuf, chardet
from tqdm import tqdm
import piexif
import hashlib

# Definiera sökvägarna för zip-filen och databasmappen
dbName = "Galaxy_Autopsy_Report.db"
filePath = r"K:/TheProjectAIF/ITF/S21.zip"
dbFolder = r"K:/TheProjectAIF/ITF/dbFolder"
dbPath = os.path.join(dbFolder, dbName)

# Kontrollera om databasmappen finns, skapa annars
if not os.path.exists(dbFolder):
    os.makedirs(dbFolder)

# Anslut till eller skapa databasen
conn = sqlite3.connect(dbPath)
cursor = conn.cursor()

# Skapa tabellen för att lagra filinformation
cursor.execute('''CREATE TABLE IF NOT EXISTS image_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filelocation TEXT,
                    hash TEXT,
                    exif_data TEXT
                  )''')

# duplicates_count = 0
# no_exif_count = 0
# juicy_count = 0

# Funktion för att extrahera och lagra bildinformation
def extract_image_info(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as z:
        for filelocation in tqdm(z.namelist(), desc="Bearbetar bilder"):
            if filelocation.lower().endswith(('.jpg', '.jpeg', '.tiff')):
                filepath = z.extract(filelocation, path="temp_images")
                exif_data = get_exif_data(filepath)
                file_hash = get_file_hash(filepath)
                # Check if the hash already exists in the database
                cursor.execute("SELECT id FROM image_data WHERE hash = ?", (file_hash,))
                if cursor.fetchone():
                    # Hash exists, skip this file
                    os.remove(filepath)
                    continue  # Move to the next file
                # Hash does not exist, proceed with inserting new data
                os.remove(filepath)  # Radera den extraherade filen
                exif_data_str = str(exif_data) if exif_data else "NO EXIF"
                cursor.execute("INSERT INTO image_data (filelocation, hash, exif_data) VALUES (?, ?, ?)",
                               (filelocation, file_hash, exif_data_str))

                
# Funktion för att hämta EXIF-data från en bildfil
def get_exif_data(filepath):
    try:
        exif_dict = piexif.load(filepath)
        # Check if EXIF data is effectively empty
        if exif_dict and all(not v for v in exif_dict.values()):
            return None  # Treat as no EXIF data
        return exif_dict if exif_dict else None
    except Exception as e:
        return None

# Funktion för att beräkna hash för en fil
def get_file_hash(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

# Kör funktionen för att bearbeta zip-arkivet
extract_image_info(filePath)

# Spara ändringarna och stäng databasanslutningen
conn.commit()
conn.close()

# print(f"Resultat av OS ZIP-filens obduktion är nu tillgänglig :)")
# print(f"Antal värdelösa dubbletter: {duplicates_count}")
# print(f"Antal filer utan smak dvs EXIF: {no_exif_count}")
# print(f"Antal Juicy filer: {juicy_count}")
