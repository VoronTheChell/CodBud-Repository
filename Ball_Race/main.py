import random
from tkinter import *
from tkinter import messagebox

def start():
    for ball in balls:
        step = random.randint(1, 20)
        canva.move(ball, step, 0)
        if canva.coords(ball)[2] >= 500:
            winner_color = canva.itemcget(ball, 'fill')
            messagebox.showinfo("Win!", f"Is winner is {winner_color} ball!")
            return
    canva.after(50, start)

def restart():
    for ball in balls:
        canva.coords(ball, * startpositions[ball])

window = Tk()
window.geometry("500x500")

canva = Canvas(width=500, height=500, bg="Lightgreen")
canva.pack()

balls = [
    canva.create_oval(50, 50, 100, 100, fill = 'red'),
    canva.create_oval(50, 150, 100, 200, fill = 'green'),
    canva.create_oval(50, 250, 100, 300, fill = 'blue'),
    canva.create_oval(50, 350, 100, 400, fill='purple')
]

startpositions = {ball: canva.coords(ball) for ball in balls}

btn_start = Button(text="Start!", font="Arial 15", command=start)
btn_start.place(x=400, y=10)

btn_restart = Button(text="Restart Race", font="Arial 15", command=restart)
btn_restart.place(x=250, y=10)

window.mainloop()