import tkinter as tk
import random

class BouncingBall:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_oval(0, 0, 20, 20, fill=color)
        self.canvas.move(self.id, random.randint(0, 380), random.randint(0, 380))
        self.x_speed = random.randint(1, 5)
        self.y_speed = random.randint(1, 5)

    def move(self):
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0 or pos[2] >= 400:
            self.x_speed = -self.x_speed
        if pos[1] <= 0 or pos[3] >= 400:
            self.y_speed = -self.y_speed
        self.canvas.move(self.id, self.x_speed, self.y_speed)

def create_bouncing_balls(canvas, num_balls): # функция создания шариков
    colors = ["red", "orange", "yellow", "green", "blue", "indigo", "violet",
              "pink", "brown", "gray", "purple", "cyan", "magenta", "lime", "teal"]

    balls = []
    for _ in range(num_balls):
        color = random.choice(colors)
        colors.remove(color)
        ball = BouncingBall(canvas, color)
        balls.append(ball)

    return balls

def animate_balls(balls):
    for ball in balls:
        ball.move()

    root.after(50, lambda: animate_balls(balls))

root = tk.Tk()
root.title("Bouncing Balls Party")

canvas = tk.Canvas(root, width=400, height=400, bg="blue")
canvas.pack()

# Создаем 15 прыгающих шаров различных цветов
balls = create_bouncing_balls(canvas, 15)

# Анимируем движение шаров
animate_balls(balls)

root.mainloop()