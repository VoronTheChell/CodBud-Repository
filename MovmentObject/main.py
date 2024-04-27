from tkinter import *
from tkinter import messagebox

def move(event):
    key = event.keysym

    home_coord = canvas.coords(home)
    ball_coord = canvas.coords(ball)

    if ball_coord[0] >= home_coord[0] + 5 and 115 <= ball_coord[1] + 8 <= 150:
        messagebox.showinfo("YOU WIN!", "Шарик Влад, теперь дома!!")
        window.destroy()

    if key == "Up":
        canvas.move(ball, 0, -10)
    if key == "Down":
        canvas.move(ball, 0, 10)
    if key == "Left":
        canvas.move(ball, -10, 0)
    if key == "Right":
        canvas.move(ball, 10, 0)

window = Tk()
window.geometry("600x600")

canvas = Canvas(window, width=600, height=600, bg='lightblue')
canvas.pack()

ball = canvas.create_oval(350, 350, 400, 400, fill='red')
home = canvas.create_rectangle(400, 150, 600, 200, fill="brown")

window.bind("<KeyPress>", move)

window.mainloop()