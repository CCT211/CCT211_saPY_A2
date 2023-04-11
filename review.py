from tkinter import *
from PIL import ImageTk, Image


class Preview:
    def __init__(self, window):
        self.frame = Frame(window, width=600, height=400)
        self.frame.grid()
        self.frame.place(anchor='center', x=100, y=150)

        # Create an object of tkinter ImageTk
        #self.img = ImageTk.PhotoImage(Image.open("img/saPY_bg.png"))

        # Create a Label Widget to display the text or Image
       #self.img_lbl = Label(self.frame, image=self.img)
        #self.img_lbl.grid()

        self.username = Label(window, text="test", font=('Arial', 25), bg='black')
        self.username.place(x=250, y=20)

        self.friends_tab = Label(window, text="Friends", font=('Arial', 25), bg='black')
        self.friends_tab.place(x=150, y=20)

        self.home_tab = Label(window, text="Home", font=('Arial', 25), bg='black')
        self.home_tab.place(x=50, y=20)

        self.title = Label(window, text="Title")
        self.title.place(x=150, y=150)

        self.description = Label(window, text="Description")
        self.description.place(x=50, y=200)

        self.reviews = Label(window, text="Reviews")
        self.reviews.place(x=50, y=350)

        self.user_review = Text(window, width=50, height=50)
        self.user_review.place(x=300, y=400)

        self.user_rating = Label(window)
        self.user_rating.place(x=50, y=400)

        self.post = Button(window, text="Post")
        self.post.place(x=675, y=475)

    def Review(self):
        self.user_rating.config(text=self.user_review)


def main():
    window = Tk()
    window.geometry("800x500")
    app = Preview(window)
    window.mainloop()


if __name__ == "__main__":
    main()
