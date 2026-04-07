import tkinter as tk
from PIL import Image, ImageTk, Image as PILImage
from main import bot_turn, player_turn, move_result, main_game, possible_move, game_score


def create_move_label(root, img_path, x, y, name):
    """Создаёт лейбл с картинкой и биндит клик"""
    img = PILImage.open(img_path)
    scaled = img.resize((100, 100), PILImage.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(scaled)
    
    label = tk.Label(root, image=photo, bg="gray")
    label.name = name
    label.image = photo  # не дать GC удалить
    label.place(x=x, y=y)
    
    label.bind("<Button-1>", on_click)  # клик для всех
    label.configure(cursor="hand2")
    return label


def on_click(event):
    name = event.widget.name
    move_result(name, bot_turn())


root = tk.Tk()
root.configure(bg="gray")
root.geometry("850x600")

create_move_label(root, "scissors.png", 700, 50, "scissors")
create_move_label(root, "stone.png", 600, 50, "stone")
create_move_label(root, "paper.png", 500, 50, "paper")


root.mainloop()