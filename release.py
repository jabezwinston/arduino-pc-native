import os
import json
import hashlib
import zipfile
import sys
import re
import requests

# Configuration
vendor = "PC-Native"
arch = "pc"
version = "0.0.2"
base_url = "https://github.com/jabezwinston/arduino-pc-native/"  # Public URL where .zip will be hosted
output_dir = "__release"

def get_version_from_tag():
    """Extract version from git tag or environment variable"""
    # Check if running in GitHub Actions
    if os.getenv('GITHUB_REF'):
        # Extract version from tag like refs/tags/v1.0.0
        ref = os.getenv('GITHUB_REF')
        match = re.search(r'refs/tags/v(.+)', ref)
        if match:
            return match.group(1)
    
    # Fallback to environment variable or default
    return os.getenv('VERSION', version)

def fetch_existing_package_index():
    """Fetch existing package index from the URL"""
    package_index_url = base_url + "releases/latest/download/package_pc-native_index.json"
    
    try:
        print(f"📥 Fetching existing package index from: {package_index_url}")
        response = requests.get(package_index_url, timeout=10)
        response.raise_for_status()
        
        existing_data = response.json()
        print("✅ Successfully fetched existing package index")
        return existing_data
        
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Could not fetch existing package index: {e}")
        print("📝 Creating new package index structure")
        return None
    except json.JSONDecodeError as e:
        print(f"⚠️  Invalid JSON in existing package index: {e}")
        print("📝 Creating new package index structure")
        return None

def update_package_index(new_platform_data):
    """Update the package index JSON with new platform data"""
    package_index_path = os.path.join(output_dir, f"package_{vendor.lower()}_index.json")
    
    # Try to fetch existing package index from URL first
    package_data = fetch_existing_package_index()
    
    # If fetch failed, try to load from local file
    if package_data is None:
        if os.path.exists(package_index_path):
            print("📁 Loading existing package index from local file")
            with open(package_index_path, 'r') as f:
                package_data = json.load(f)
        else:
            print("📝 Creating new package index structure")
            # Create new package index structure
            package_data = {
                "packages": [
                    {
                        "name": vendor,
                        "maintainer": "Jabez Winston",
                        "websiteURL": base_url,
                        "email": "jabezwinston@gmail.com",
                        "help": {
                            "online": "https://jabezwinston.github.io/"
                        },
                        "platforms": [],
                        "tools": []
                    }
                ]
            }
    
    # Find existing platform with same architecture and version
    package = package_data["packages"][0]
    existing_platform_index = None
    
    for i, platform in enumerate(package["platforms"]):
        if platform["architecture"] == arch and platform["version"] == new_platform_data["version"]:
            existing_platform_index = i
            break
    
    # Update existing version or prepend new version
    if existing_platform_index is not None:
        print(f"🔄 Updating existing platform {arch} v{new_platform_data['version']}")
        package["platforms"][existing_platform_index] = new_platform_data
    else:
        print(f"➕ Prepending new platform {arch} v{new_platform_data['version']}")
        # Insert at the beginning to keep newest versions first
        package["platforms"].insert(0, new_platform_data)
    
    # Write updated package index
    with open(package_index_path, 'w') as f:
        json.dump(package_data, f, indent=4)
    
    print(f"💾 Package index saved to: {package_index_path}")
    return package_index_path

def create_release():
    """Main function to create the release package"""
    global version
    version = get_version_from_tag()
    
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

        # Include variants/ folder and its contents under pc-{version}/variants/
        variants_path = "variants"
        if os.path.exists(variants_path):
            for foldername, subfolders, filenames in os.walk(variants_path):
                for filename in filenames:
                    filepath = os.path.join(foldername, filename)
                    # Get relative path inside variants/
                    rel_path = os.path.relpath(filepath, start=".")  # relative to current directory
                    arcname = os.path.join(archive_basename, rel_path)  # e.g., pc-1.0.0/variants/...
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

    # Step 4: Create platform data
    platform_data = {
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

    # Step 5: Update package index
    package_index_path = update_package_index(platform_data)

    print("✅ Arduino board package (ZIP) created successfully.")
    print(f"📦 Archive: {zip_path}")
    print(f"📄 JSON: {package_index_path}")
    print(f"🔐 SHA-256: {checksum}")
    print(f"📋 Version: {version}")

def update_package_index_only():
    """Function to update only the package index without creating new zip"""
    global version
    version = get_version_from_tag()
    
    # Check if zip file exists
    archive_basename = f"{arch}-v{version}"
    zip_path = os.path.join(output_dir, archive_basename + ".zip")
    
    if not os.path.exists(zip_path):
        print(f"❌ Error: Zip file {zip_path} not found. Run create_release() first.")
        return False
    
    # Generate checksum and size for existing zip
    def sha256sum(filename):
        h = hashlib.sha256()
        with open(filename, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()

    checksum = sha256sum(zip_path)
    size = os.path.getsize(zip_path)

    # Create platform data
    platform_data = {
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

    # Update package index
    package_index_path = update_package_index(platform_data)
    
    print("✅ Package index updated successfully.")
    print(f"📄 JSON: {package_index_path}")
    print(f"🔐 SHA-256: {checksum}")
    print(f"📋 Version: {version}")
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "update-index":
        update_package_index_only()
    else:
        create_release()
