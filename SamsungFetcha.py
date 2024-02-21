import zipfile, sqlite3, csv, io, os, gzip, blackboxprotobuf, chardet
from tqdm import tqdm

# Definiera sökvägarna för zip-filen och databasmappen
dbName = "Galaxy_Autopsy_Report.db"
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
cursor.execute('''CREATE TABLE IF NOT EXISTS file_contents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filelocation TEXT,
                    content TEXT,
                    size INTEGER
                  )''')



# Öppna zip-filen och bearbeta filerna
def decode_and_insert_file_contents(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as z:
        for filelocation in tqdm(z.namelist()):
            if filelocation.endswith(('.csv', '.log', '.txt')):
                with z.open(filelocation, 'r') as file:
                    # Läs bara de första 4096 bytes för att gissa kodningen i syfte till att effektivisera processen då de är stora mängder data som granskas annars
                    content_sample = file.read(4096)
                    if not content_sample: # Skippar filer utan innehåll
                        continue
                    result = chardet.detect(content_sample)
                    encoding = result['encoding']

                    # Återställ pekaren till början av filen för att läsa hela filen
                    file.seek(0)
                    content_full = file.read()

                    # Dekoda innehållet med den upptäckta kodningen eller använd UTF-8 som fallback
                    try:
                        content_str = content_full.decode(encoding) if encoding else content_full.decode('utf-8')
                        size = len(content_full)
                        cursor.execute("INSERT INTO file_contents (filelocation, content, size) VALUES (?, ?, ?)", (filelocation, content_str, size)) # Insert the decoded content into the database
                        #print(f"File: {filelocation}, Encoding: {encoding}\nContent:\n{content_str}\n") #Optional kommentera bort den här raden om du inte vill se innehållet spammas i terimnalen
                        

                        
                    except UnicodeDecodeError:
                        #print(f"Could not decode {filelocation} with encoding {encoding}. Trying 'utf-8-sig' or 'ISO-8859-1'.") #Optional kommentera bort den här raden om du inte vill se innehållet spammas i terimnalen
                        
                        try:
                            content_str = content_full.decode('utf-8-sig')
                            size = len(content_full)
                            cursor.execute("INSERT INTO file_contents (filelocation, content, size) VALUES (?, ?, ?)", (filelocation, content_str, size))
                        except UnicodeDecodeError:
                            content_str = content_full.decode('ISO-8859-1')
                            size = len(content_full)
                            cursor.execute("INSERT INTO file_contents (filelocation, content, size) VALUES (?, ?, ?)", (filelocation, content_str, size))
                        #print(f"File: {filelocation}, Encoding: 'utf-8-sig' or 'ISO-8859-1' used as fallback.\nContent:\n{content_str}\n") #Optional kommentera bort den här raden om du inte vill se innehållet spammas i terimnalen
                        



decode_and_insert_file_contents(filePath)



# Åtaga ändringar och stäng databasanslutningen
conn.commit()
conn.close()

print("Result of the OS ZIP file autopsy is now availible :)")
