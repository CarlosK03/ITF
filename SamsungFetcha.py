'''
Senast gjort:


'''
import zipfile, sqlite3, csv, io, os, gzip, blackboxprotobuf, chardet

# Definiera sökvägarna för zip-filen och databasmappen
dbName = "extracted_data.db"
filePath = r"K:/TheProjectAIF/ITF/S21.zip"
dbFolder = r"K:/TheProjectAIF/ITF/dbFolder"
dbPath = os.path.join(dbFolder, dbName)

#Definerar en variabel som innehåller de filtyper vi är intresserade av
relevant_extensions = (
    '.log', '.txt', '.csv',  # Loggfiler och textfiler
    # '.db', '.sqlite',  # Databaser för webbhistorik, cookies, etc.
    # '.pdf', '.txt',  # Dokumentfiler
    # '.jpg', '.jpeg', '.png', '.gif', '.bmp',  # Bildfiler
    # '.pb'  # Och andra specifika filtyper du är intresserad av
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


# Öppna zip-filen
# Öppna zip-filen och bearbeta filerna
with openedZipFile as z:
    for filename in z.namelist():
        if filename.endswith(relevant_extensions):
            print(f"Bearbetar fil: {filename}")
            if filename.endswith('.csv'):
                with z.open(filename) as f:
                    # Slå in filpekaren i en TextIOWrapper för att läsa text
                    text_stream = io.TextIOWrapper(f, encoding='utf-8')
                    reader = csv.reader(text_stream)
                    for row in reader:
                        # Konvertera raden (listan) till en sträng
                        row_str = ', '.join(row)
                        # Infoga den konverterade strängen i databasen
                        cursor.execute('INSERT INTO my_table (data) VALUES (?)', [row_str])
            elif filename.endswith('.log') or filename.endswith('.txt'):
                with z.open(filename) as f:
                    # Läs innehållet i filen
                    content = f.read()
                    # Konvertera innehållet till en sträng
                    content_str = content.decode('utf-8')
                    # Infoga den konverterade strängen i databasen
                    cursor.execute('INSERT INTO my_table (data) VALUES (?)', [content_str])

        #    print("File: ", filename)
        # if filename.endswith('.csv'):  # Bearbeta CSV-filer
        #     with z.open(filename) as f:
        #         print(f"Bearbetar fil: {filename}")
        #         # Slå in filpekaren i en TextIOWrapper för att läsa text
        #         text_stream = io.TextIOWrapper(f, encoding='utf-8')
        #         reader = csv.reader(text_stream)
        #         for row in reader:
        #             # Infoga varje rad i databasen
        #             cursor.execute('INSERT INTO my_table (column1, column2) VALUES (?, ?)', row)

# Åtaga ändringar och stäng databasanslutningen
conn.commit()
conn.close()

print("Data importerades dags att dissikera :)")
