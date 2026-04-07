import tkinter as tk
from PIL import ImageTk, Image as PILImage
from main import bot_turn, move_result, possible_move

def on_click(event):
    player_move = event.widget.name
    move_result(player_move, bot_turn())

root = tk.Tk()
root.geometry("800x300")
root.title("Игра Камень/Ножницы/Бумага")

img = PILImage.open('scissors.png')
scaled = img.resize((150, 150))
photo = ImageTk.PhotoImage(scaled)


label = tk.Label(root, image=photo)
label.image = photo
label.name = "scissors"
label.place(x=400, y=50)
label.configure(cursor="hand2")
label.bind("<Button-1>", on_click)

root.mainloop()