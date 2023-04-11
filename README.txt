"""
    saPY
    CCT 211 - UTM
    Project 2
    Prof. Michael Nixon


    Created by: Nawal Abdulkadir, Tiana Guard, Pranay Nagi, & Scott Warren
    
    THIS IS THE MAIN .py FILE. This must be ran first.

    This project uses dependencies found within the /app directory.
    This also relies on the Google API.
    Additional libraries will need to be installed to run this app. Instructions provided below:


To run the application, the following libraries need to be installed:

sqlite3
tkinter
google-auth
google-auth-oauthlib
google-auth-httplib2
google-api-python-client
Pillow

To install the above libraries, use the following PIP command:

pip install sqlite3 tkinter google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client Pillow

After installing the necessary libraries, run the application by executing the main_saPY_211.py file. Once the file is executed, the user will be prompted to create a saPY account before being granted access to all features of the program.

Dependencies are found within the /app folder, which contains 2 sql databases that are used in the /app/database directory.

Important Google security API keys are located in /app/security. These are required for the app to run.

There are backups of the main file in Backups.

All .py files found in /app will not run on their own, and only open if done through the main .py file in the top of the directory.

There are right-click context menus, and window embedded drop-down menus in the main page to access certain features. There are also regular GUI buttons for this aswell.

All CRUD features are used, as users can create information through registering as a user and writing reviews, read information by listing this in reviews, username displays, and friends/user lists, update information with refresh buttons and adding/updating the reviews list, and deleting information from the database by deleting all reviews from the Reviews page.

Information within the program describes itself as follows:

INFORMATION:
saPY is an Indie project sharing platform! Users can upload new projects using the UPLOAD button below. Users can view other users' projects by pressing SHOW NEW TITLES! Users can download anyone's work by RIGHT CLICKING a project from the library list on the left and clicking DOWNLOAD from the context menu. Users may also leave REVIEWS and view USERS as friends by using their respective buttons!

(Images remain unused for artistic reasons, but were experimented with as seen in the code)

"""

DIVISION OF LABOUR:

Nawal Abdulkadir created the friends list,

Tiana Guard & Pranay Nagi created the login page and reviews page,

& Scott Warren created the main page, SQL functionality, and combined all pages together

Github: https://github.com/CCT211/CCT211_saPY_A2

(C) 2023