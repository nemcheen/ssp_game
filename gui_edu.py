import tkinter as tk
from random import randint
import time
from PIL import ImageTk, Image as PILImage
from main import bot_turn, move_result, possible_move


# Функция вызываемая при нажатии на виджет. Вызывает ход игры
def on_click(event):
    player_move = event.widget.name
    label_hide(list_obj_labels=list_obj_labels,
               name_label_to_show=player_move)
    bot_move = bot_chose_animation(bot_label=bot_label)
    print(f'player move: {player_move}, bot move: {bot_move}')
    move_result(player_move, bot_move)
    all_label_show(list_obj_labels=list_obj_labels)


def create_widget(root, img_path, x, y, name: str, clickable=True): 
    """ root - основное окно / img_path - путь к картинке
        x, y - координаты для позициоирования картинки
        name - имя виджета, для отслеживание на что мы нажали"""
    
    img = PILImage.open(img_path)
    scaled = img.resize((100, 100))
    photo = ImageTk.PhotoImage(scaled)

    label = tk.Label(root, image=photo)
    label.image = photo
    label.name = name
    label.x = x # !!
    label.y = y # !!!
    label.place(x=x, y=y)
    if clickable: 
        label.configure(cursor="hand2")
        label.bind("<Button-1>", on_click)
    return label

def bot_chose_animation(bot_label, total_delay=700):
    """ Анимация выбора хода ботом. """
    image_paths = ('scissors.png', 'stone.png', 'paper.png')
    images = []
    for path in image_paths:
        img = PILImage.open(path).resize((100, 100))
        images.append(ImageTk.PhotoImage(img))
    bot_move_number = randint(9, 11)
    current_step = 0
    bot_chose = image_paths[bot_move_number % 3].split('.')[0]
    
    def step():
        nonlocal bot_chose, current_step
        idx = current_step % 3
        image = images[idx]
        bot_label.configure(image=image)
        bot_label.image = image
        current_step += 1
        if current_step <= bot_move_number:  # Включая финал
            step_delay = total_delay // bot_move_number
            bot_label.after(step_delay, step)
    
    step()
    return bot_chose


def label_hide(list_obj_labels, name_label_to_show):
    """ Скрываем остальные лейблы предметов кроме того что выбрал игрок """
    for item in list_obj_labels:
        if item.name != name_label_to_show:
            item.place_forget()

def all_label_show(list_obj_labels):
    """ Показываем все виджеты """
    for item in list_obj_labels:
        item.place() # Чтобы в виджеты не накладывались стопкой друг на друга нужно ставить их на свои места
                    # для этого измени функцию размещения лейбла create_widget() чтобы она сохраняла координаты в отдельное поле


# Инициализация окна
root = tk.Tk()
root.geometry("800x300")
root.title("Игра Камень/Ножницы/Бумага")

bot_label = create_widget(root=root,
              img_path="question-mark.png",
              x=100,
              y=80,
              name="?",
              clickable=False)

scissors = create_widget(root=root,
              img_path="scissors.png",
              x=680,
              y=80,
              name="scissors")
stone = create_widget(root=root,
              img_path="stone.png",
              x=580,
              y=80,
              name="stone")
paper = create_widget(root=root,
              img_path="paper.png",
              x=480,
              y=80,
              name="paper")

list_obj_labels = [scissors, stone, paper]


root.mainloop()