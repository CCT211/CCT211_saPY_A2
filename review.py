import sqlite3
from tkinter import *


class Preview:
    def __init__(self, window):
        self.frame = Frame(window, width=600, height=400, bg="#171a21")
        self.frame.grid()
        self.frame.place(anchor='center', x=100, y=150)

        self.review_scrollbar = Scrollbar(window)
        self.review_scrollbar.place(x=400, y=320, height=80)

        self.review_text = Text(window, width=50, height=10, font=("Helvetica", 14), fg="#f2f2f2", bg="#2C2F33", bd=0, yscrollcommand=self.review_scrollbar.set)
        self.review_text.place(x=50, y=225)
        self.review_scrollbar.config(command=self.review_text.yview)

        self.user_review = Text(window, width=50, height=5, font=("Helvetica", 14), fg="#1b2838", bg="#66c0f4", bd=0)
        self.user_review.place(x=50, y=50)

        self.post = Button(window, text="Post Review", command=self.post_review, bg="#66c0f4", activebackground="#4d94db", bd=0, font=("Helvetica", 16), fg="#f2f2f2")
        self.post.place(x=670, y=400)

        self.delete_button = Button(window, text="Delete All Reviews", command=self.delete_reviews, bg="red", activebackground="#4d94db", bd=0, font=("Helvetica", 16), fg="#f2f2f2")
        self.delete_button.place(x=670, y=350)

        self.reviews = Label(window, text="User Reviews", font=("Helvetica", 18), fg="#f2f2f2", bg="#171a21")
        self.reviews.place(x=50, y=190)

        self.username_label = Label(window, text="Username", font=("Helvetica", 14), fg="#f2f2f2", bg="#171a21")
        self.username_label.place(x=50, y=10)

        self.show_reviews()
        self.show_username()

    def post_review(self):
        review = self.user_review.get("1.0", END).strip()
        if review:
            conn = sqlite3.connect('user_date_saPY.db')
            cur = conn.cursor()
            cur.execute("SELECT username FROM usernames ORDER BY id DESC LIMIT 1")
            username = cur.fetchone()[0]
            review_with_username = f"Username: {username}\n{review}"
            cur.execute("INSERT INTO reviews (review) VALUES (?)", (review_with_username,))
            conn.commit()
            conn.close()
            self.user_review.delete("1.0", END)
            self.show_reviews()

    def delete_reviews(self):
        conn = sqlite3.connect('user_date_saPY.db')
        cur = conn.cursor()
        cur.execute("DELETE FROM reviews")
        conn.commit()
        conn.close()
        self.show_reviews()

    def show_reviews(self):
        conn = sqlite3.connect('user_date_saPY.db')
        cur = conn.cursor()
        cur.execute("SELECT review FROM reviews ORDER BY id DESC")
        reviews = cur.fetchall()
        review_text = "\n\n".join([f"{i}. {review[0]}" for i, review in enumerate(reviews, 1)])
        self.review_text.config(state=NORMAL)
        self.review_text.delete("1.0", END)
        self.review_text.insert(END, review_text)
        self.review_text.config(state=DISABLED)
        conn.close()

    def show_username(self):
        conn = sqlite3.connect('user_date_saPY.db')
        cur = conn.cursor()
        cur.execute("SELECT username FROM usernames ORDER BY id DESC LIMIT 1")
        username = cur.fetchone()[0]
        self.username_label.config(text=f"Welcome, {username}!" + " Write a review below:")
        conn.close()


def main():
    window = Tk()
    window.geometry("900x500")
    window.title("User Reviews")

    window.lift()
    window.attributes('-topmost', True)
    window.after_idle(window.attributes, '-topmost', False)

    window.config(bg="#171a21")
    app = Preview(window)
    window.mainloop()


if __name__ == "__main__":
    main()
