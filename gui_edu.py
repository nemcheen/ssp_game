import tkinter as tk
from PIL import ImageTk, Image as PILImage
from main import bot_turn, move_result, possible_move


# Функция вызываемая при нажатии на виджет. Вызывает ход игры
def on_click(event):
    player_move = event.widget.name
    move_result(player_move, bot_turn())

# Инициализация окна
root = tk.Tk()
root.geometry("800x300")
root.title("Игра Камень/Ножницы/Бумага")

# Обработка фото 
img = PILImage.open('scissors.png')
scaled = img.resize((100, 100))
photo = ImageTk.PhotoImage(scaled)

# Создание виджета картинки
label = tk.Label(root, image=photo)
label.image = photo
label.name = "scissors"
label.place(x=650, y=80)
label.configure(cursor="hand2")
label.bind("<Button-1>", on_click)

root.mainloop()