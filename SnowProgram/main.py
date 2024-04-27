import random
from tkinter import *

def check_collision():
    basket_coords = canva.coords(basket)
    for snowflake in snowflakes:
        snowflake_coords = canva.coords(snowflake)
        if (basket_coords[0] - 100 <= snowflake_coords[0] <= basket_coords[0] + 125) and \
           (basket_coords[1] - 60 <= snowflake_coords[1] + 100):
            increase_score()
            canva.delete(snowflake)
            snowflakes.remove(snowflake)

def move_basket(event):
    key = event.keysym
    if key == "Left":
        canva.move(basket, -15, 0)
    elif key == "Right":
        canva.move(basket, 15, 0)

def increase_score():
    global score
    score += 1
    score_label.config(text=f'Score: {score}')

def move_snowflake(snowflake):
    x, y = canva.coords(snowflake)
    canva.move(snowflake, 0, 5)

    if y < 800:
        canva.after(50, move_snowflake, snowflake)
    else:
        canva.delete(snowflake)
        snowflakes.remove(snowflake)
        create_snowflake()

def create_snowflake():
    x = random.randint(0, 600)
    y = 0
    snowflake = canva.create_image(x, y, image=image)

    # Список наследования:
    snowflakes.append(snowflake)
    move_snowflake(snowflake)

def spawn_snowflake():
    create_snowflake()
    check_collision()
    window.after(1000, spawn_snowflake)

window = Tk()
window.title("Snow Program")
window.geometry("600x600")

canva = Canvas(window, width=600, height=800, bg="white")
canva.pack()

image = PhotoImage(file="snow.png")
buket = PhotoImage(file='buket.png')

basket = canva.create_image(400, 600, image=buket)

score = 0
score_label = Label(text=f'Score: {score}', font=("Arial", 16), bg="white")
score_label.place(x=10, y=10)

snowflakes = []

spawn_snowflake()

window.bind("<Left>", move_basket)
window.bind("<Right>", move_basket)

window.mainloop()
