"""
    saPY
    CCT 211
    Project 2
    Prof. Michael Nixon

    Nawal Abdulkadir, Tiana Guard, Pranay Nagi, & Scott Warren
    
    THIS IS THE MAIN .py FILE. This must be ran first.

    This project uses dependencies found within the /app directory.
    This also relies on the Google API.
    Additional libraries will need to be installed to run this app.
    
    Please read the README.txt for additional info.
"""

import os
import sys
import sqlite3
import tkinter as tk
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from tkinter import filedialog
from tkinter import messagebox
from googleapiclient.http import MediaFileUpload
from google.auth.crypt._python_rsa import RSAVerifier, RSASigner
from PIL import Image, ImageTk

import subprocess

# Run the script
subprocess.call(['python', 'app/log_in.py'])


creds = None
SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = 'app/security/credentials.json'

if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)

if not creds:
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title('saPY Launcher')
        self.geometry('1280x720')
        self.minsize(1280, 720)  # Set minimum size
        self.configure(bg='#1b2838')
        self.resizable(True, True)

        self.lift()
        self.attributes('-topmost', True)
        self.after_idle(self.attributes, '-topmost', False)

        ### Uncomment Below For Image Based Background
        #self.add_background()

        self.bind("<Configure>", self.on_window_resize)

        self.info = tk.Label(self, text='INFORMATION:\nsaPY is an Indie project sharing platform!\nUsers can upload new projects using the UPLOAD button below.\nUsers can view other users projects by pressing SHOW NEW TITLES!\nUsers can download anyones work by RIGHT CLICKING a project from the library list\non the left and clicking DOWNLOAD from the context menu.\nUsers may also leave REVIEWS and view USERS as friends by using their respective buttons!\n\nCreated for CCT211 by Nawal Abdulkadir, Tiana Guard, Pranay Nagi, & Scott Warren', font=('Arial', 12), fg='#b8c9d3', bg='#141e2a', highlightthickness=0)
        self.info.place(relx=0.327, rely=0.25, width=850, height=200)

        header_label = tk.Label(self, text='saPY INDIE Library', font=('Arial', 36, 'bold'), bg='#141e2a', fg='#b8c9d3', anchor="e", padx=10, pady=10)
        header_label.pack(fill='x')

        upload_btn = tk.Button(self, text='Upload Project to saPY Cloud Library', command=self.upload_file, bg='#2d425d', fg='#b8c9d3', activebackground='#2d425d', activeforeground='#b8c9d3')
        #upload_btn.pack(pady=10)
        upload_btn.place(relx=0.327, rely=0.9, width=850, height=50)

        list_btn = tk.Button(self, text='Show New Titles', command=self.list_files, bg='#2d425d', fg='#b8c9d3', activebackground='#2d425d', activeforeground='#b8c9d3')
        #list_btn.pack(pady=10)
        list_btn.place(x=420, y=100, width=150, height=50)

        self.files_lb = tk.Listbox(self, bg='#1b2838', fg='#b8c9d3', selectbackground='#2d425d', selectforeground='#b8c9d3')
        #self.files_lb.pack(pady=10)
        self.files_lb.place(x=10, y=100, width=400, height=600)

        self.status_label = tk.Label(self, text='Status: Awaiting Action', font=('Arial', 15, 'bold', 'italic'), bg='#141e2a', fg='#b8c9d3', padx=10, pady=10)
        self.status_label.place(relx=0.327, rely=0.8, width=850, height=60)

        review_btn = tk.Button(self, text='Write a Review', command=self.open_review, bg='#2d425d', fg='#b8c9d3', activebackground='#2d425d', activeforeground='#b8c9d3')
        #list_btn.pack(pady=10)
        review_btn.place(relx=0.327, rely=0.7, width=850, height=60)

        friend_btn = tk.Button(self, text='Open Friends List', command=self.open_friends, bg='#2d425d', fg='#b8c9d3', activebackground='#2d425d', activeforeground='#b8c9d3')
        #list_btn.pack(pady=10)
        friend_btn.place(relx=0.327, rely=0.6, width=200, height=60)

        self.files_lb.bind('<Button-3>', self.create_context_menu)

        self.username_label = tk.Label(self, text='Status: Awaiting Action', font=('Arial', 15, 'bold', 'italic'), anchor="w", fg='#b8c9d3', bg='#1b2838', highlightthickness=0)
        self.username_label.place(x=15, y=15, width=555, height=50)

        self.show_username()

        # Create top menu
        menu = tk.Menu(self)
        self.config(menu=menu)

        # Create File menu
        file_menu = tk.Menu(menu, tearoff=False)
        file_menu.add_command(label='Refresh List', command=self.list_files)
        file_menu.add_command(label='Upload', command=self.upload_file)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.exit)
        menu.add_cascade(label='File', menu=file_menu)

        # Create Social menu
        social_menu = tk.Menu(menu, tearoff=False)
        social_menu.add_command(label='Friends', command=self.open_friends)
        social_menu.add_command(label='Reviews', command=self.open_review)
        menu.add_cascade(label='Social', menu=social_menu)

    def on_window_resize(self, event):
        self.get_window_dimensions()

    def get_window_dimensions(self):
            # Get width and height
            self.width = self.winfo_width()
            self.height = self.winfo_height()

    def add_background(self):
        img = Image.open("img/saPY_bg.png")
        bg_img = ImageTk.PhotoImage(img)
        bg_label = tk.Label(self, image=bg_img)
        bg_label.place(relwidth=1, relheight=1)
        bg_label.image = bg_img
        img = img.resize((1280, 720), Image.ANTIALIAS)

    def create_context_menu(self, event):
        # Get the selected item from the listbox
        selection = self.files_lb.curselection()
        if len(selection) == 0:
            return
        selected_item = self.files_lb.get(selection[0])

        # Create the context menu
        context_menu = tk.Menu(self, tearoff=0)
        context_menu.add_command(label='Download', command=lambda: self.download_files(event))
        context_menu.post(event.x_root, event.y_root)

    def upload_file(self):
        folder_id = '1wxgIuKHCU0aUCDgDw0y6_gFXIyU9LRSA' # Replace with the ID of your Google Drive folder
        self.status_label.config(text=('Status: Select something to upload to saPY!'))
        file_path = filedialog.askopenfilename()
        file_name = os.path.basename(file_path)

        try:
            service = build('drive', 'v3', credentials=creds)

            file_metadata = {'name': file_name, 'parents': [folder_id]}
            media = MediaFileUpload(file_path, resumable=True)
            file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

            print(f'File ID: {file.get("id")} has been uploaded to Google Drive')
            self.status_label.config(text=(f'Status: {file_metadata.get("name")} has been uploaded to saPY Indie Servers!'))
        except HttpError as error:
            print(f'An error occurred: {error}')
            self.status_label.config(text=(f'Status: An error occurred: {error}'))
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
                self.status_label.config(text=('Status: No files found.'))
            else:
                print('Files:')
                self.status_label.config(text=('Status: Showing new releases from saPY servers!'))
                self.files_lb.delete(0, tk.END)

                # Create or connect to an existing sqlite3 database
                conn = sqlite3.connect('app/database/saPY_Warren.db')
                c = conn.cursor()

                # Create a table to store the file names and IDs
                c.execute('CREATE TABLE IF NOT EXISTS files (name TEXT, id TEXT)')

                for item in items:
                    print(f'{item["name"]} ({item["id"]})')
                    # Insert or update the file name and ID in the database
                    c.execute('INSERT OR REPLACE INTO files (name, id) VALUES (?, ?)', (item["name"], item["id"]))

                    # Add the file name to the listbox
                    self.files_lb.insert(tk.END, item["name"])

                # Commit the changes to the database and close the connection
                conn.commit()
                conn.close()

        except HttpError as error:
            print(f'An error occurred: {error}')
            self.status_label.config(text=(f'Status: An error occurred: {error}'))

    def download_files(self, event):
        # Get the selected item from the listbox
        selection = self.files_lb.curselection()
        if len(selection) == 0:
            return
        selected_item = self.files_lb.get(selection[0])

        self.status_label.config(text=(f'Status: {selected_item} is being downloaded from saPY!'))

        # Find the file ID in the database
        conn = sqlite3.connect('app/database/saPY_Warren.db')
        c = conn.cursor()
        c.execute('SELECT id FROM files WHERE name=?', (selected_item,))
        file_id = c.fetchone()[0]
        conn.close()

        # Download the file
        try:
            service = build('drive', 'v3', credentials=creds)
            request = service.files().get_media(fileId=file_id)
            file_path = filedialog.asksaveasfilename(defaultextension='', initialfile=selected_item)
            if file_path:
                with open(file_path, 'wb') as f:
                    f.write(request.execute())
                    print(f'File {selected_item} has been downloaded to {file_path}')
                    self.status_label.config(text=(f'Status: {selected_item} has been downloaded to {file_path}'))
        except HttpError as error:
            print(f'An error occurred: {error}')
            self.status_label.config(text=(f'Status: An error occurred: {error}'))

    def open_review(self):
        subprocess.Popen(["python", "app/review.py"])

    def open_friends(self):
        subprocess.Popen(["python", "app/Friendslist.py"])

    def show_username(self):
        conn = sqlite3.connect('app/database/user_date_saPY.db')
        cur = conn.cursor()
        cur.execute("SELECT username FROM usernames ORDER BY id DESC LIMIT 1")
        username = cur.fetchone()[0]
        self.username_label.config(text=f"Logged in as, {username}!")
        conn.close()

    def exit(self):
        sys.exit()


if __name__ == '__main__':
    app = App()
    app.mainloop()

"""
    saPY
    CCT 211
    Project 2
    Prof. Michael Nixon

    Nawal Abdulkadir, Tiana Guard, Pranay Nagi, & Scott Warren
    
    THIS IS THE MAIN .py FILE. This must be ran first.

    This project uses dependencies found within the /app directory.
    This also relies on the Google API.
    Additional libraries will need to be installed to run this app.
    
    Please read the README.txt for additional info.
"""

### This program is so smart, the comments practically wrote themselves! ###
