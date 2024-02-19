import struct

data = struct.pack("c c h h i", b"V", b"T", 2, 3, 2024)

print(data)

# Correct usage of hex() without sep argument
print(' '.join(f"{byte:02x}" for byte in data))

for oneByte in data:
    print(f"{oneByte:0>8b}", end=" ")

# Correctly appending "Digital Forensics" to data
additional_data = struct.pack("17s", b"Digital Forensics")
data += additional_data

# Correctly printing the hex representation of data with spaces
print(' '.join(f"{byte:02x}" for byte in data))
