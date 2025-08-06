from azure.storage.fileshare import ShareFileClient
from azure.storage.fileshare import ShareServiceClient
import os

# Source account credentials
SUBSCRIPTION_ID = ""
RESOURCE_GROUP = "fileprocess-rg1"
STORAGE_ACCOUNT_NAME = "fileprocessorsk01"
STORAGE_ACCOUNT_KEY = ""
SHARE_NAME = "test-share2"
SOURCE_DIR = "processed"
DEST_DIR = "folder1/processed"


def get_service_client():
    return ShareServiceClient(
        account_url=f"https://{STORAGE_ACCOUNT_NAME}.file.core.windows.net/",
        credential=STORAGE_ACCOUNT_KEY
    )

def move_html_files():
    service_client = get_service_client()
    share_client = service_client.get_share_client(SHARE_NAME)
    
    source_dir_client = share_client.get_directory_client(SOURCE_DIR)
    dest_dir_client = share_client.get_directory_client(DEST_DIR)

    # Create destination directory if not exists
    try:
        dest_dir_client.create_directory()
        print(f"✅ Created destination folder: {DEST_DIR}")
    except:
        print(f"ℹ️ Destination folder {DEST_DIR} already exists.")

    # List files in source directory
    for file in source_dir_client.list_directories_and_files():
        if not file["is_directory"] and file["name"].endswith(".html"):
            file_name = file["name"]
            print(f"📄 Moving file: {file_name}")

            # Get file client
            source_file = source_dir_client.get_file_client(file_name)
            dest_file = dest_dir_client.get_file_client(file_name)

            # Download file
            data = source_file.download_file().readall()

            # Upload to destination
            dest_file.upload_file(data)
            print(f"✅ Uploaded to {DEST_DIR}/{file_name}")

            # Delete from source
            source_file.delete_file()
            print(f"🗑️ Deleted from {SOURCE_DIR}/{file_name}")

if __name__ == "__main__":
    move_html_files()
