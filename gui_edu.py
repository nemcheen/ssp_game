import tkinter as tk
from random import randint
import time
from PIL import ImageTk, Image as PILImage
from main import bot_turn, move_result, possible_move


# Функция вызываемая при нажатии на виджет. Вызывает ход игры
def on_click(event):
    player_move = event.widget.name
    choosed = label_hide(root,
               list_obj_labels=list_obj_labels,
               name_label_to_show=player_move,
               )
    bot_move = bot_chose_animation(bot_label=bot_label)
    attack(choosed)
    print(f'player move: {player_move}, bot move: {bot_move}')
    move_result(player_move, bot_move)


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
        nonlocal current_step
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


def label_hide(root, list_obj_labels, name_label_to_show, delay=2000):
    """ Скрываем остальные лейблы предметов кроме того что выбрал игрок """
    unhided = None
    for item in list_obj_labels:
        if item.name != name_label_to_show:
            item.place_forget()
        else:
            unhided = item
    
      # через delay_ms снова показываем все
    root.after(delay, all_label_show, list_obj_labels, root) # obj.after(delay, func_name, *args)
    return unhided

def all_label_show(list_obj_labels, root):
    """ Показываем все виджеты """
    for item in list_obj_labels:
        item.place(x=item.x, y=item.y)

def attack(item, 
           delay=500, 
           frames=10, 
           root_width=800, 
           root_height=300):
    """ Анимация атаки предмета. Летит в центр! """
    current_x = item_x = item.winfo_x()
    current_y = item_y = item.winfo_y()
    item_width = item.winfo_width()
    item_height = item.winfo_height()
    path_x = (item_x - root_width // 2) + item_width // 2 
    path_y = (item_y - root_height // 2) + item_height // 2 
    step_x = -path_x // frames
    step_y = -path_y // frames
    step_delay = delay // frames
    print(current_y, path_y, step_y)
    cross_middle = False
    def step():
        nonlocal path_x, path_y, current_x, current_y, cross_middle
        print(current_y, path_y, step_y)
        if path_x * (path_x + step_x) <= 0 or path_y * (path_y + step_y) <= 0:
            cross_middle = True
        path_x += step_x
        path_y += step_y
        current_x += step_x
        current_y += step_y
        item.place(x=current_x, y=current_y)
        if not cross_middle:
            item.after(step_delay, step)
    step()
      

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