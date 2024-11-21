import tkinter as tk
import random

# Constants
GAME_WIDTH = 700
GAME_HEIGHT = 700
GAME_SPEED = 100
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = '#00ff00'  # Green
FOOD_COLOR = '#ff0000'   # Red
BACKGROUND_COLOR = '#000000'  # Black

class Snake:
    def __init__(self):
        self.body_parts = BODY_PARTS
        self.coordinates = [[0, 0] for _ in range(BODY_PARTS)]
        self.squares = []

        for i in range(BODY_PARTS):
            x, y = self.coordinates[i]
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tags='snake')
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, GAME_WIDTH // SPACE_SIZE - 1) * SPACE_SIZE
        y = random.randint(0, GAME_HEIGHT // SPACE_SIZE - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tags='food')

def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == 'up':
        y -= SPACE_SIZE
    elif direction == 'down':
        y += SPACE_SIZE
    elif direction == 'left':
        x -= SPACE_SIZE
    elif direction == 'right':
        x += SPACE_SIZE

    snake.coordinates.insert(0, [x, y])
    snake.squares.insert(0, canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tags='snake'))

    if x == food.coordinates[0] and y == food.coordinates[1]:
        eat_food(snake, food)
    else:
        delete_last_body_part(snake)

    if check_collisions(snake):
        game_over()
    else:
        window.after(GAME_SPEED, next_turn, snake, food)

def eat_food(snake, food):
    global score
    score += 1
    label.config(text=f"Score: {score}")
    canvas.delete('food')
    food = Food()

def delete_last_body_part(snake):
    x, y = snake.coordinates[-1]
    canvas.delete(snake.squares[-1])
    snake.coordinates.pop()
    snake.squares.pop()

def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def game_over():
    canvas.delete('all')
    canvas.create_text(GAME_WIDTH // 2, GAME_HEIGHT // 2, text='Game Over', font=('Arial', 30), fill='red')

def change_direction(new_direction):
    global direction
    if new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction
    elif new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction

def on_close():
    window.destroy()

# Initialize the game window
window = tk.Tk()
window.title("Snake Game")
window.geometry(f"{GAME_WIDTH}x{GAME_HEIGHT}")
window.resizable(False, False)
window.protocol("WM_DELETE_WINDOW", on_close)

# Initialize game variables
score = 0
direction = 'down'

# Create the game canvas
canvas = tk.Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Create the score label
label = tk.Label(window, text=f"Score: {score}", font=("Arial", 20))
label.pack()

# Create initial snake and food objects
snake = Snake()
food = Food()

# Bind arrow keys to change direction
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

# Start the game loop
next_turn(snake, food)

# Run the game
window.mainloop()
