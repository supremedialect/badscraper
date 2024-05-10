import os
import requests
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Function to authenticate with Google Drive API
def authenticate():
    SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('drive', 'v3', credentials=creds)

# Function to search for images with a given keyword in Google Drive
def search_images(service, keyword):
    query = f"name contains '{keyword}' and mimeType contains 'image/'"
    results = service.files().list(q=query).execute()
    images = results.get('files', [])

    return images

# Function to download images from URLs
def download_images(images):
    for image in images:
        url = image['webContentLink']
        filename = image['name']
        response = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {filename}")

def main():
    # Authenticate with Google Drive API
    service = authenticate()

    # Get user input for keyword
    keyword = input("Enter the keyword to search for: ")

    # Search for images in Google Drive
    images = search_images(service, keyword)

    if images:
        # Download images
        download_images(images)
        print("Images downloaded successfully!")
    else:
        print("No images found with the given keyword.")

if __name__ == "__main__":
    main()
