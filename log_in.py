from tkinter import *
import sqlite3
import os
import sys

root = Tk()
root.geometry("500x450")
root.title("saPY Registration")

# set up the main frame
main_frame = Frame(root, bg="#1b2838")
main_frame.pack(expand=True, fill=BOTH)

# set up the login frame
login_frame = Frame(main_frame, bg="#2c3e50")
login_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

# set up the title label
Title_Label = Label(login_frame, text="saPY", bg="#2c3e50", fg="white", font=("Helvetica", 25))
Title_Label.pack(pady=10)

# set up the title label
Title_Label = Label(login_frame, text="Please enter your information", bg="#2c3e50", fg="white", font=("Helvetica", 16))
Title_Label.pack(pady=20, padx=10)

# set up the username and password labels and inputs
Username = Label(login_frame, text="Username/Email", bg="#2c3e50", fg="white", font=("Helvetica", 12))
Username.pack(pady=5)
Username_input = Entry(login_frame, bd=2, font=("Helvetica", 12))
Username_input.pack(pady=5)

Password = Label(login_frame, text="Password", bg="#2c3e50", fg="white", font=("Helvetica", 12))
Password.pack(pady=5)
Password_input = Entry(login_frame, bd=2, show="*", font=("Helvetica", 12))
Password_input.pack(pady=5)

# create a connection to the database
with sqlite3.connect('user_date_saPY.db') as conn:
    # create a cursor object to execute SQL queries
    cur = conn.cursor()

    # create tables if they don't exist
    cur.execute('''CREATE TABLE IF NOT EXISTS usernames (username TEXT)''')
    cur.execute('''CREATE TABLE IF NOT EXISTS passwords (password TEXT)''')

    # ====LOGIN FUNCTION====
    def login():
        username, password = (Username_input.get(), Password_input.get())
        if username == "" or password == "":
            B["text"] = "Invalid"
            B["fg"] = 'red'
        else:
            # check if username already exists in the database
            cur.execute('''SELECT * FROM usernames WHERE username=?''', (username,))
            if cur.fetchone():
                # username exists, login fails
                B["text"] = "Registration Failed"
                B["fg"] = 'red'
            else:
                # insert username and password into the database
                cur.execute('''INSERT INTO usernames (username) VALUES (?)''', (username,))
                cur.execute('''INSERT INTO passwords (password) VALUES (?)''', (password,))
                conn.commit()

                # set button colors and text
                B["fg"] = "white"
                B["text"] = "Welcome"
                #B2["fg"] = "white"
                #B2["bg"] = "#3498db"
                # set up the next button

                B2.pack(pady=10)

        def exit():
            conn.close()
            root.close()
            #sys.exit()

    # set up the login button
    B = Button(login_frame, text="Register", fg="white", bg="#2980b9", bd=0, font=("Helvetica", 12), command=login)
    B.pack(pady=10)

    B2 = Button(login_frame, text="Continue to saPY!", fg="white", bg="#3498db", bd=0, font=("Helvetica", 12), command=exit)


root.mainloop()

# close the connection to the database
#conn.close()

