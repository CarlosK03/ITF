import struct

data = struct.pack("c c h h i", b"V", b"T", 2, 3, 2024)

print(data)

print(data.hex(sep=" "))

for oneByte in data:
    print(f"{oneByte:0>8b}", end=" ")
    
data += (struct.pack("17s"), b"Digital FOrensics")

unpackedData = struct.unpack("c c h h i 17s", data)

print(unpackedData)

for value in unpackedData:
    print(value)
