# Description: This file contains utility functions to interact with Azure Blob Storage.
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

def get_blob_service_client(blob_account_url, blob_credential):
    return BlobServiceClient(blob_account_url, blob_credential)

def list_blobs(blob_service_client, blob_container_name):
    container_client = blob_service_client.get_container_client(blob_container_name)
    return container_client.list_blobs()

def read_blob_content(client, container_name, blob_name):
    try:
        blob_client = client.get_blob_client(container=container_name, blob=blob_name)
        blob_content = blob_client.download_blob().readall()
        # Assuming the blob content is text. Adjust decoding as necessary.
        return blob_content.decode('utf-8')
    except Exception as e:
        print(f"Failed to read blob content: {e}")
        return None
