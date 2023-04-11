import sqlite3
import tkinter as tk
from tkinter import ttk


class FriendsApp:
    def __init__(self, parent):
        self.parent = parent
        self.parent.title("saPY Friends List")
        self.parent.geometry("300x550")
        self.parent.resizable(False, False)
        self.parent.configure(bg='#1b2838')

        self.parent.lift()
        self.parent.attributes('-topmost', True)
        self.parent.after_idle(self.parent.attributes, '-topmost', False)

        # Username List Label
        self.title_label = tk.Label(self.parent, text="Friends List", font=("Arial Bold", 15), padx=10, pady=10, bg='#1b2838', fg='#aeb2b8')
        self.title_label.grid(row=1, column=0, columnspan=2, sticky='w')

        # Recent Username Value
        self.recent_username_value = tk.Label(self.parent, text="", font=("Arial Bold", 15), padx=10, pady=10, bg='#1b2838', fg='#aeb2b8')
        self.recent_username_value.grid(row=0, column=0, sticky='w')

        # Treeview
        self.tree = ttk.Treeview(self.parent, columns=("Name"), height=20)
        self.tree.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.heading("Name", text="Friends Username:", anchor=tk.W)

        # Scrollbar
        #self.scrollbar = ttk.Scrollbar(self.parent, orient='vertical', command=self.tree.yview)
        #self.scrollbar.grid(row=2, column=1, sticky='ns')
        #self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Search Entry
        #self.search_entry = tk.Entry(self.parent, bg='#2c3849', fg='#aeb2b8', bd=0, highlightthickness=1, highlightbackground='#45a5f5', highlightcolor='#45a5f5', insertbackground='#aeb2b8')
        #self.search_entry.grid(row=3, column=0, padx=10, pady=10, sticky='ew')
        #self.search_entry.bind("<Return>", lambda x: self.search_friends())

        # Search Button
        #self.search_button = tk.Button(self.parent, text='Search', bd=0, bg='#45a5f5', activebackground='#45a5f5', command=self.search_friends)

        #self.search_button.grid(row=3, column=1, padx=10, pady=10, sticky='w')

        self.populate_tree()

    def populate_tree(self):
        self.tree.delete(*self.tree.get_children())
        conn = sqlite3.connect('app/database/user_date_saPY.db')
        cur = conn.cursor()
        cur.execute('SELECT * FROM usernames')
        rows = cur.fetchall()
        for row in rows:
            self.tree.insert('', 'end', text=row[0], values=(row[1],))
        cur.execute('SELECT username FROM usernames ORDER BY id DESC LIMIT 1')
        recent_username = cur.fetchone()
        self.recent_username_value.configure(text=recent_username[0])
        conn.close()

    def search_friends(self):
        self.tree.delete(*self.tree.get_children())
        conn = sqlite3.connect('app/database/user_date_saPY.db')
        cur = conn.cursor()
        search_name = self.search_entry.get()
        recent_username = self.recent_username_value.cget("text")
        cur.execute('SELECT DISTINCT friend FROM friends_list WHERE username=? AND friend LIKE ?', (recent_username, f'%{search_name}%'))
        rows = cur.fetchall()
        for row in rows:
            self.tree.insert('', 'end', text=row[0], values=("N/A",))
        conn.close()

        self.populate_tree()


if __name__ == '__main__':
    root = tk.Tk()
    FriendsApp(root)
    root.mainloop()
