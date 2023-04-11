#Friendslist 
import sqlite3
import sys
import tkinter as tk

#Create a window 
window = tk.Tk()
#title
window.title("Friends")
#alter the size 
window.geometry("350x900") 
#changing the colour 
window.title("Find Your Friend")
window.configure(bg='gray65')

# Make a widget that you can label
label = tk.Label(window, text="Find Your Friend", bg='gray65')

#Make an entry field for your widget 
entry = tk.Entry(window,bg='gray65')

title_label = tk.Label(window, text="SayinCraftsStudio", font=("Arial Bold", 15), padx=20, bg='gray65')

# make the first button 
button = tk.Button(window, text="Search", bg='black')

# Use grid to organize 
title_label.grid(row=0, column=0, columnspan=2, sticky='ew')
label.grid(row=1, column=0, pady=20)
entry.grid(row=1, column=1, pady=20)
button.grid(row=2, column=0, columnspan=2, pady=20)


# Define a function to populate the Treeview widget
def view_tree():
    # Clear the tree view
    tree.delete(*tree.view())
    # Generate some random data to populate the Treeview
    for i in range(10):
        name = 'Person {}'.format(i+1)
        age = random.randint(18, 50)
        username= random.choice(['Prenawal', 'SayinCrafts', 'Pranay_Nagi', 'Cutecat', 'ScottWarren'])
        country = random.choice(['Somalia', 'Canada', 'Mexico', 'India'])
        tree.insert('', 'end', text=i+1, values=(name, age, username, country))

# make the button connect to the treeview
button.configure(command= view_tree)


# Start the tkinter event loop
window.mainloop()

