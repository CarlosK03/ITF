'''Skapade denna Py-fil i syfte till att lista ut vilka kodningar som används i filerna i S21.zip'''
'''Denna används ej längre då jag implementerad logiken i SamsungFetcha.py'''

# import zipfile
# import chardet

# def detect_encodings(zip_path):
#     with zipfile.ZipFile(zip_path, 'r') as z:
#         encodings = {}  # Använder en dict för att spara kodningar och motsvarande filer
#         for filename in z.namelist():
#             if filename.endswith(('.csv', '.log', '.txt')):
#                 with z.open(filename, 'r') as file:
#                     content = file.read(4096)  # Läser bara de första 4096 bytes
#                     result = chardet.detect(content)
#                     encoding = result['encoding']
#                     if encoding:
#                         if encoding not in encodings:
#                             encodings[encoding] = [filename]
#                         else:
#                             encodings[encoding].append(filename)
#         # Skriver ut kodningarna och motsvarande filer
#         for encoding, files in encodings.items():
#             print(f"Detected encoding: {encoding}")
#             for file in files:
#                 print(f"  - {file}")

# zip_path = 'K:/TheProjectAIF/ITF/S21.zip'
# detect_encodings(zip_path)
