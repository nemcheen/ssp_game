import tkinter as tk
from PIL import ImageTk, Image as PILImage
from main import bot_turn, move_result, possible_move


# Функция вызываемая при нажатии на виджет. Вызывает ход игры
def on_click(event):
    player_move = event.widget.name
    move_result(player_move, bot_turn())

def create_widget(root, img_path, x, y, name: str): 
    """ root - основное окно / img_path - путь к картинке
        x, y - координаты для позициоирования картинки
        name - имя виджета, для отслеживание на что мы нажали"""
    
    img = PILImage.open(img_path)
    scaled = img.resize((100, 100))
    photo = ImageTk.PhotoImage(scaled)

    label = tk.Label(root, image=photo)
    label.image = photo
    label.name = name
    label.place(x=x, y=y)
    label.configure(cursor="hand2")
    label.bind("<Button-1>", on_click)
    return label

def bot_chose_animation():
    """ Анимация выбора хода ботом. """
    pass  

# Инициализация окна
root = tk.Tk()
root.geometry("800x300")
root.title("Игра Камень/Ножницы/Бумага")

# Вызовы функций для размещение всех трех картинок

create_widget(root=root,
              img_path="scissors.png",
              x=680,
              y=80,
              name="scissors")
create_widget(root=root,
              img_path="stone.png",
              x=580,
              y=80,
              name="stone")
create_widget(root=root,
              img_path="paper.png",
              x=480,
              y=80,
              name="paper")


root.mainloop()