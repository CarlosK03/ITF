'''
Innuti dbFolder skapas db filen om den redan existerar där så måste vi radera den för att skapa en ny i koden.
'''
import zipfile, sqlite3, os
from tqdm import tqdm
import piexif
import hashlib

# Definiera sökvägar för zip-filen och databasmappen
dbName = "Galaxy_Autopsy_Report.db"
filePath = r"K:/TheProjectAIF/ITF/S21.zip"
dbFolder = r"K:/TheProjectAIF/ITF/dbFolder"
dbPath = os.path.join(dbFolder, dbName)

# Kontrollera om databasmappen finns; skapa annars
if not os.path.exists(dbFolder):
    os.makedirs(dbFolder)

# Anslut till eller skapa databasen
conn = sqlite3.connect(dbPath)
cursor = conn.cursor()

# Skapa en tabell i databasen för att lagra bildinformation
cursor.execute('''CREATE TABLE IF NOT EXISTS image_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filelocation TEXT,
                    hash TEXT,
                    exif_data TEXT
                  )''')

# Funktion för att extrahera och lagra information om bilder från en zip-fil
def extract_image_info(zip_path):
    # Öppna zip-filen
    with zipfile.ZipFile(zip_path, 'r') as z:
        # Iterera över varje fil i zip-arkivet
        for filelocation in tqdm(z.namelist(), desc="Bearbetar bilder"):
            # Kontrollerar filformat
            if filelocation.lower().endswith(('.jpg', '.jpeg', '.tiff')):
                # Extraherar filen till en temporär mapp
                filepath = z.extract(filelocation, path="temp_images")
                # Hämtar EXIF-data och hash för bilden
                exif_data_str = get_readable_exif_data(filepath)
                file_hash = get_file_hash(filepath)
                # Kontrollerar om hashen redan finns i databasen
                cursor.execute("SELECT id FROM image_data WHERE hash = ?", (file_hash,))
                if cursor.fetchone():
                    # Hash finns redan, ignorerar filen
                    os.remove(filepath)
                    continue
                # Hash finns inte, infogar ny data
                os.remove(filepath)  # Radera den extraherade filen
                exif_data_str = str(exif_data_str) if exif_data_str else "NO EXIF"
                cursor.execute("INSERT INTO image_data (filelocation, hash, exif_data) VALUES (?, ?, ?)",
                               (filelocation, file_hash, exif_data_str))

# Funktion för att hämta EXIF-data från en bildfil
def get_readable_exif_data(filepath):
    try:
        exif_dict = piexif.load(filepath)
        readable_exif = {}

        # Konverterar EXIF-data till en mer läsbar form
        for ifd in exif_dict:
            if ifd == "thumbnail":
                continue  # Ignorera miniatyrbilden
            for tag in exif_dict[ifd]:
                tag_name = piexif.TAGS[ifd][tag]["name"]
                tag_value = exif_dict[ifd][tag]
                
                # Konvertera binära data till läsbar sträng om möjligt
                if isinstance(tag_value, bytes):
                    try:
                        tag_value = tag_value.decode('utf-8', 'ignore')
                    except UnicodeDecodeError:
                        tag_value = "<binär data>"
                
                readable_exif[tag_name] = tag_value

        # Returnera den läsbara EXIF-informationen som en sträng
        exif_str = "; ".join([f"{key}: {value}" for key, value in readable_exif.items()])
        return exif_str if exif_str else "Ingen EXIF-data funnen"
    except Exception as e:
        return "Fel vid läsning av EXIF-data"

'''
Funktionen beräknar SHA-256-hash för en fil. Den läser filen i små delar (block om 4096 byte) för effektivitet och uppdaterar hashet för varje del.
lambda: f.read(4096) är ett enkelt sätt att upprepa läsningen tills filen är helt läst.
Detta gör beräkningen snabb och minneseffektiv. Efter att hela filen lästs, returneras hashet som en hexadecimal sträng.
'''
def get_file_hash(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def generate_html_report(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT filelocation, hash, exif_data FROM image_data")
    images = cursor.fetchall()
    
    # HTML fil skapas och skrivs
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bildinformationsrapport</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #333; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ text-align: left; padding: 8px; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        th {{ background-color: #4CAF50; color: white; }}
    </style>

    </head>
    <body>
        <h1>Bildinformationsrapport</h1>
        <table border="1">
            <tr>
                <th>Filplats</th>
                <th>Hash</th>
                <th>EXIF Data</th>
            </tr>
            {}
        </table>
    </body>
    </html>
    """
    # Skapar tabellrader för varje bild
    rows = ""
    for filelocation, hash, exif_data in images:
        rows += "<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(filelocation, hash, exif_data)
    
    # Slutför HTML-innehållet
    html = html.format(rows)
    
    # Skriver HTML-innehåll till en fil
    with open("image_data_report.html", "w", encoding="utf-8") as file:
        file.write(html)
    
    print("HTML-Autopsin har genererats :D")

# Bearbeta zip-arkivet för att extrahera bildinformation
extract_image_info(filePath)

# Spara ändringar och stäng databasanslutningen
conn.commit()
conn.close()

# Generera HTML-rapporten från databasen sist p.ga att vi vill ha all data när db filen inte är låst
generate_html_report(dbPath)