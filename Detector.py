'''Created this Python file with the purpose of figuring out the encodings used in the files within S21.zip.  
This is no longer used as I have implemented the logic in SamsungFetcha.py.'''

# import zipfile
# import chardet

# def detect_encodings(zip_path):
#     with zipfile.ZipFile(zip_path, 'r') as z:
#         encodings = {}  # Använder en dict för att spara kodningar och motsvarande filer
#         for filelocation in z.namelist():
#             if filelocation.endswith(('.csv', '.log', '.txt')):
#                 with z.open(filelocation, 'r') as file:
#                     content = file.read(4096)  # Läser bara de första 4096 bytes
#                     result = chardet.detect(content)
#                     encoding = result['encoding']
#                     if encoding:
#                         if encoding not in encodings:
#                             encodings[encoding] = [filelocation]
#                         else:
#                             encodings[encoding].append(filelocation)
#         # Skriver ut kodningarna och motsvarande filer
#         for encoding, files in encodings.items():
#             print(f"Detected encoding: {encoding}")
#             for file in files:
#                 print(f"  - {file}")

# zip_path = 'K:/TheProjectAIF/ITF/S21.zip'
# detect_encodings(zip_path)
