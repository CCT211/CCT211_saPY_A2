import os
import tkinter as tk
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from tkinter import filedialog
from googleapiclient.http import MediaFileUpload
from google.auth.crypt._python_rsa import RSAVerifier, RSASigner


creds = None
SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = 'credentials.json'

if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

if not creds:
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title('Google Drive Uploader')
        self.geometry('400x300')

        upload_btn = tk.Button(self, text='Upload File', command=self.upload_file)
        upload_btn.pack(pady=10)

        list_btn = tk.Button(self, text='List Files', command=self.list_files)
        list_btn.pack(pady=10)

        self.files_lb = tk.Listbox(self)

    def upload_file(self):
        folder_id = '1wxgIuKHCU0aUCDgDw0y6_gFXIyU9LRSA' # Replace with the ID of your Google Drive folder
        file_path = filedialog.askopenfilename()
        file_name = os.path.basename(file_path)

        try:
            service = build('drive', 'v3', credentials=creds)

            file_metadata = {'name': file_name, 'parents': [folder_id]}
            media = MediaFileUpload(file_path, resumable=True)
            file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

            print(f'File ID: {file.get("id")} has been uploaded to Google Drive')
        except HttpError as error:
            print(f'An error occurred: {error}')
            file = None

        return file

    def list_files(self):
        folder_id = '1wxgIuKHCU0aUCDgDw0y6_gFXIyU9LRSA' # Replace with the ID of your Google Drive folder

        try:
            service = build('drive', 'v3', credentials=creds)
            query = f"'{folder_id}' in parents and trashed = false"
            results = service.files().list(q=query, fields="nextPageToken, files(id, name)").execute()
            items = results.get('files', [])

            if not items:
                print('No files found.')
            else:
                print('Files:')
                self.files_lb.delete(0, tk.END)
                for item in items:
                    print(f'{item["name"]} ({item["id"]})')
                    self.files_lb.insert(tk.END, item["name"])
        except HttpError as error:
            print(f'An error occurred: {error}')
            items = None

        return items


app = App()
app.mainloop()
