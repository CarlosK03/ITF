import zipfile, sqlite3, os
from tqdm import tqdm
import piexif
import hashlib

# Defines paths for the zip file and the database folder
dbName = "X.db"
filePath = r"INSERT PHONE OS ZIP FILE PATH"
dbFolder = r"INSERT LOCATION FOR THE CREATED DB FILE AFTER CODE EXECUTION"
dbPath = os.path.join(dbFolder, dbName)

# Checks if the database folder exists; otherwise, creates it
if not os.path.exists(dbFolder):
    os.makedirs(dbFolder)

# Connects to or creates the database
conn = sqlite3.connect(dbPath)
cursor = conn.cursor()

# Creates a table in the database to store image information
cursor.execute('''CREATE TABLE IF NOT EXISTS image_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filelocation TEXT,
                    hash TEXT,
                    exif_data TEXT
                  )''')

# Function to extract and store information about images from a zip file
def extract_image_info(zip_path):
    # Opens the zip file
    with zipfile.ZipFile(zip_path, 'r') as z:
        # Iterates over each file in the zip archive
        for filelocation in tqdm(z.namelist(), desc="Processing images"):
            # Checks the file format
            if filelocation.lower().endswith(('.jpg', '.jpeg', '.tiff')):
                # Extracts the file to a temporary folder
                filepath = z.extract(filelocation, path="temp_images")
                # Retrieves EXIF data and hash for the image
                exif_data_str = get_readable_exif_data(filepath)
                file_hash = get_file_hash(filepath)
                # Checks if the hash already exists in the database
                cursor.execute("SELECT id FROM image_data WHERE hash = ?", (file_hash,))
                if cursor.fetchone():
                    # Hash already exists, ignores the file
                    os.remove(filepath)
                    continue
                # Hash does not exist, inserts new data
                os.remove(filepath)  # Deletes the extracted file
                exif_data_str = str(exif_data_str) if exif_data_str else "NO EXIF"
                cursor.execute("INSERT INTO image_data (filelocation, hash, exif_data) VALUES (?, ?, ?)",
                               (filelocation, file_hash, exif_data_str))

# Function to retrieve EXIF data from an image file
def get_readable_exif_data(filepath):
    try:
        exif_dict = piexif.load(filepath)
        readable_exif = {}

        # Converts EXIF data to a more readable format
        for ifd in exif_dict:
            if ifd == "thumbnail":
                continue  # Ignores the thumbnail
            for tag in exif_dict[ifd]:
                tag_name = piexif.TAGS[ifd][tag]["name"]
                tag_value = exif_dict[ifd][tag]
                
                # Converts binary data to a readable string if possible
                if isinstance(tag_value, bytes):
                    try:
                        tag_value = tag_value.decode('utf-8', 'ignore')
                    except UnicodeDecodeError:
                        tag_value = "<binary data>"
                
                readable_exif[tag_name] = tag_value

        # Returns the readable EXIF information as a string
        exif_str = "; ".join([f"{key}: {value}" for key, value in readable_exif.items()])
        return exif_str if exif_str else "No EXIF data found"
    except Exception as e:
        return "Error reading EXIF data"

'''
The function calculates a SHA-256 hash for a file. It reads the file in small chunks (blocks of 4096 bytes) for efficiency and updates the hash for each chunk.
lambda: f.read(4096) is a simple way to repeatedly read until the file is fully read.
This makes the computation fast and memory-efficient. After the entire file is read, the hash is returned as a hexadecimal string.
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
    
    # HTML file is created and written
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Image Information Report</title>
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
        <h1>Image Information Report</h1>
        <table border="1">
            <tr>
                <th>File Location</th>
                <th>Hash</th>
                <th>EXIF Data</th>
            </tr>
            {}
        </table>
    </body>
    </html>
    """
    # Creates table rows for each image
    rows = ""
    for filelocation, hash, exif_data in images:
        rows += "<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(filelocation, hash, exif_data)
    
    # Completes the HTML content
    html = html.format(rows)
    
    # Writes the HTML content to a file
    with open("image_data_report.html", "w", encoding="utf-8") as file:
        file.write(html)
    
    print("HTML report has been generated :D")

# Processes the zip archive to extract image information
extract_image_info(filePath)

# Saves changes and closes the database connection
conn.commit()
conn.close()

# Generates the HTML report from the database last because we want all data when the DB file is not locked
generate_html_report(dbPath)
