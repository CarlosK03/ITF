'''
Senast gjort:


'''
import zipfile, sqlite3, csv, io, os, gzip, blackboxprotobuf

# Definiera sökvägarna för zip-filen och databasmappen
filePath = r"K:/TheProjectAIF/ITF/S21.zip"
dbFolder = r"K:/TheProjectAIF/ITF/dbFolder"
dbName = "extracted_data.db"

openedZipFile = zipfile.ZipFile(filePath, mode="r")

# Se till att dbFolder finns och om den ej finns skapar den
if not os.path.exists(dbFolder):
    os.makedirs(dbFolder)

# Fullständig sökväg för databasen
dbPath = os.path.join(dbFolder, dbName)

# Anslut till eller skapa SQLite-databasen
conn = sqlite3.connect(dbPath)
cursor = conn.cursor()

# Skapa en tabell
cursor.execute('''CREATE TABLE IF NOT EXISTS my_table (
                    id INTEGER PRIMARY KEY,
                    column1 TEXT,
                    column2 TEXT
                  )''')

# Öppna zip-filen
with opendZipFile as z:
    for filename in z.namelist():
        if filename.endswith('.csv'):  # Bearbeta CSV-filer
            with z.open(filename) as f:
                print(f"Bearbetar fil: {filename}")
                # Slå in filpekaren i en TextIOWrapper för att läsa text
                text_stream = io.TextIOWrapper(f, encoding='utf-8')
                reader = csv.reader(text_stream)
                for row in reader:
                    # Infoga varje rad i databasen
                    cursor.execute('INSERT INTO my_table (column1, column2) VALUES (?, ?)', row)

# Åtaga ändringar och stäng databasanslutningen
conn.commit()
conn.close()

print("Data importerades dags att dissikera :)")
