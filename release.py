import os
import json
import hashlib
import zipfile

# Configuration
vendor = "PC-Native"
arch = "pc"
version = "0.0.1"
base_url = "https://github.com/jabezwinston/arduino-pc-native/"  # Public URL where .zip will be hosted
output_dir = "__release"

# Derived paths
hardware_path = "cores"
archive_basename = f"{arch}-v{version}"
zip_path = os.path.join(output_dir, archive_basename + ".zip")

# Step 1: Create empty folder structure
os.makedirs(output_dir, exist_ok=True)
os.makedirs(os.path.join(output_dir, archive_basename), exist_ok=True)

# Step 2: Create zip file with all contents under pc-{version}/
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    # Include cores/ folder and its contents under pc-{version}/cores/
    for foldername, subfolders, filenames in os.walk(hardware_path):
        for filename in filenames:
            filepath = os.path.join(foldername, filename)
            # Get relative path inside cores/
            rel_path = os.path.relpath(filepath, start=".")  # relative to current directory
            arcname = os.path.join(archive_basename, rel_path)  # e.g., pc-1.0.0/cores/...
            zipf.write(filepath, arcname)


    for file in [ "boards.txt", "platform.txt", "programmers.txt"]:
        if os.path.exists(file):
            zipf.write(file, os.path.join(archive_basename, file))

# Step 3: Generate SHA-256 checksum
def sha256sum(filename):
    h = hashlib.sha256()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

checksum = sha256sum(zip_path)
size = os.path.getsize(zip_path)

json_data = {
    "packages": [
        {
            "name": vendor,
            "maintainer": "Jabez Winston",
            "websiteURL": base_url,
            "email": "jabezwinston@gmail.com",
            "help": {
                "online": "https://jabezwinston.github.io/"
            },
            "platforms": [
                {
                    "name": f"{vendor}",
                    "architecture": arch,
                    "version": version,
                    "category": "Contributed",
                    "url": base_url + f"releases/download/v{version}/" + os.path.basename(zip_path),
                    "archiveFileName": os.path.basename(zip_path),
                    "checksum": f"SHA-256:{checksum}",
                    "size": size,
                    "boards": [
                        {"name": "PC simulator"},
                    ],
                    "toolsDependencies": []
                }
            ],
            "tools": []
        }
    ]
}

# Step 5: Write package_index.json
json_path = os.path.join(output_dir, f"package_{vendor.lower()}_index.json")
with open(json_path, "w") as f:
    json.dump(json_data, f, indent=4)

print("✅ Arduino board package (ZIP) created successfully.")
print(f"📦 Archive: {zip_path}")
print(f"📄 JSON: {json_path}")
print(f"🔐 SHA-256: {checksum}")
