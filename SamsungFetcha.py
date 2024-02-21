import zipfile, sqlite3, csv, io, os, gzip, blackboxprotobuf, chardet

# Definiera sökvägarna för zip-filen och databasmappen
dbName = "extracted_data.db"
filePath = r"K:/TheProjectAIF/ITF/S21.zip"
dbFolder = r"K:/TheProjectAIF/ITF/dbFolder"
dbPath = os.path.join(dbFolder, dbName)

#Definerar en variabel som innehåller de filtyper vi är intresserade av
relevant_extensions = (
    '.log', '.txt', '.csv',  # Loggfiler och textfiler
)
#Variabel som defineras med att den öppnar S21.zip för läsning
openedZipFile = zipfile.ZipFile(filePath, mode="r")

# Se till att dbFolder finns och om den ej finns skapar den
if not os.path.exists(dbFolder):
    os.makedirs(dbFolder)

# Anslut till eller skapa SQLite-databasen
conn = sqlite3.connect(dbPath)
cursor = conn.cursor()

# Skapa en tabell
cursor.execute('''CREATE TABLE IF NOT EXISTS my_table (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data TEXT
                  )''')


# Öppna zip-filen och bearbeta filerna
def decode_and_print_file_contents(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as z:
        for filename in z.namelist():
            if filename.endswith(('.csv', '.log', '.txt')):
                with z.open(filename, 'r') as file:
                    # Läs bara de första 4096 bytes för att gissa kodningen
                    content_sample = file.read(4096)
                    result = chardet.detect(content_sample)
                    encoding = result['encoding']

                    # Återställ pekaren till början av filen för att läsa hela filen
                    file.seek(0)
                    content_full = file.read()

                    # Dekoda innehållet med den upptäckta kodningen eller använd UTF-8 som fallback
                    try:
                        content_str = content_full.decode(encoding) if encoding else content_full.decode('utf-8')
                        print(f"File: {filename}, Encoding: {encoding}\nContent:\n{content_str}\n")
                    except UnicodeDecodeError:
                        print(f"Could not decode {filename} with encoding {encoding}. Trying 'utf-8-sig' or 'ISO-8859-1'.")
                        try:
                            content_str = content_full.decode('utf-8-sig')
                        except UnicodeDecodeError:
                            content_str = content_full.decode('ISO-8859-1')
                        print(f"File: {filename}, Encoding: 'utf-8-sig' or 'ISO-8859-1' used as fallback.\nContent:\n{content_str}\n")


# Åtaga ändringar och stäng databasanslutningen
conn.commit()
conn.close()

print("Data importerades dags att dissikera :)")
