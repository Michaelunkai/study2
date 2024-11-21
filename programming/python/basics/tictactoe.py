import tkinter as tk
import random

def next_turn(row, column):
    global player
    if buttons[row][column]['text'] == '':
        buttons[row][column]['text'] = player
        if not check_winner():
            player = players[1] if player == players[0] else players[0]
            label.config(text=f"{player}'s turn")

def check_winner():
    # Check horizontal win conditions
    for row in range(3):
        if buttons[row][0]['text'] == buttons[row][1]['text'] == buttons[row][2]['text'] != '':
            highlight_buttons(row, 0, row, 1, row, 2)
            label.config(text=f"{buttons[row][0]['text']} wins!")
            return True

    # Check vertical win conditions
    for column in range(3):
        if buttons[0][column]['text'] == buttons[1][column]['text'] == buttons[2][column]['text'] != '':
            highlight_buttons(0, column, 1, column, 2, column)
            label.config(text=f"{buttons[0][column]['text']} wins!")
            return True

    # Check diagonal win conditions
    if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != '':
        highlight_buttons(0, 0, 1, 1, 2, 2)
        label.config(text=f"{buttons[0][0]['text']} wins!")
        return True
    elif buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text'] != '':
        highlight_buttons(0, 2, 1, 1, 2, 0)
        label.config(text=f"{buttons[0][2]['text']} wins!")
        return True

    return False

def empty_spaces():
    spaces = 9
    for row in range(3):
        for column in range(3):
            if buttons[row][column]['text'] != '':
                spaces -= 1
    return spaces > 0

def new_game():
    global player
    player = random.choice(players)
    label.config(text=f"{player}'s turn")

    for row in range(3):
        for column in range(3):
            buttons[row][column]['text'] = ''
            buttons[row][column]['bg'] = '#f0f0f0'  # Default button color

def highlight_buttons(row1, col1, row2, col2, row3, col3):
    buttons[row1][col1]['bg'] = buttons[row2][col2]['bg'] = buttons[row3][col3]['bg'] = 'green'

window = tk.Tk()
window.title("Tic-Tac-Toe")

players = ['X', 'O']
player = random.choice(players)

buttons = [[0 for _ in range(3)] for _ in range(3)]

label = tk.Label(window, text=f"{player}'s turn")
label.pack(side=tk.TOP)

reset_button = tk.Button(window, text="Restart", font=("Arial", 20), command=new_game)
reset_button.pack(side=tk.TOP)

frame = tk.Frame(window)
frame.pack()

for row in range(3):
    for column in range(3):
        buttons[row][column] = tk.Button(frame, text='', font=("Arial", 5), width=5, height=2,
                                         command=lambda row=row, column=column: next_turn(row, column))
        buttons[row][column].grid(row=row, column=column)

window.mainloop()
