import tkinter as tk
from random import randint
from PIL import ImageTk, Image as PILImage
from main import bot_turn, move_result, possible_move


BOT_CHOSE_DURATION = 700
ATTACK_START_DELAY, ATTACK_DURATION = 850, 250
EXPLOSION_DELAY, EXPLOSION_DARATION = 1150, 500
WINNER_ATTACK_START_DELAY, WINNER_ATTACK_DURATION = 1600, 250
HIDE_DURATION = 2500

# Функция вызываемая при нажатии на виджет. Вызывает ход игры
def on_click(event):
    player_move = event.widget.name
    choosed = label_hide(root,
               list_obj_labels=list_obj_labels,
               name_label_to_show=player_move,
               duration=HIDE_DURATION
               )
    bot_move = bot_chose_animation(bot_label=bot_label, duration=BOT_CHOSE_DURATION)
    attack(choosed, start_delay=ATTACK_START_DELAY, duration=ATTACK_DURATION)
    attack(bot_label, start_delay=ATTACK_START_DELAY, duration=ATTACK_DURATION)
    explosion_animation(explosion, duration=EXPLOSION_DARATION, start_delay=EXPLOSION_DELAY)
    print(f'player move: {player_move}, bot move: {bot_move}')
    winner = move_result(player_move, bot_move)
    attack_to_side(bot_label, choosed, winner=winner, start_delay=WINNER_ATTACK_START_DELAY, duration=WINNER_ATTACK_DURATION)
    down_health(bot_health, player_health, who_wins=winner)

def get_and_crop_img_obj(img_path, width=100, height=100):
    img = PILImage.open(img_path)
    scaled = img.resize((width, height))
    img_obj = ImageTk.PhotoImage(scaled)
    return img_obj    

def create_widget(root, 
                  img_path, 
                  x, y, 
                  name: str, 
                  clickable=True, 
                  default_img_path=None,
                  default_unvisible=False,
                  width=100,
                  height=100): 
    # добавим еще поле с дефолтной картинкой и добавим параметр в функцию
    """ root - основное окно / img_path - путь к картинке
        x, y - координаты для позициоирования картинки
        name - имя виджета, для отслеживание на что мы нажали"""
    
    photo_obj = get_and_crop_img_obj(img_path, width=width, height=height)
    label = tk.Label(root, image=photo_obj)
    if default_img_path is not None:
        default_photo_obj = get_and_crop_img_obj(default_img_path)
        label.default_image = default_photo_obj
    label.image = photo_obj
    label.name = name
    label.x = x # !!
    label.y = y # !!!
    label.place(x=x, y=y)
    if default_unvisible:
        label.place_forget()
    if clickable: 
        label.configure(cursor="hand2")
        label.bind("<Button-1>", on_click)
    return label

def bot_chose_animation(bot_label, duration=700):
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
            step_delay = duration // bot_move_number
            root.after(step_delay, step)
    
    step()
    return bot_chose

def one_item_hide(item, start_delay=0):
    def wrapper(item):
        item.place_forget()
    item.after(start_delay, wrapper, item)

def label_hide(root, list_obj_labels, name_label_to_show, duration=2000):
    """ Скрываем остальные лейблы предметов кроме того что выбрал игрок """
    unhided = None
    for item in list_obj_labels:
        if item.name == '?':
            continue
        if item.name != name_label_to_show:
            item.place_forget()
        else:
            unhided = item
      # через delay_ms снова показываем все
    root.after(duration, all_label_show, list_obj_labels) # obj.after(delay, func_name, *args)
    return unhided

def all_label_show(list_obj_labels):
    """ Показываем все виджеты  возвращаем дефолтную картинку бот вилжету"""
    for item in list_obj_labels:
        if item.name == '?':
            item.configure(image=item.default_image)
            item.image = item.default_image
        item.place(x=item.x, y=item.y)
        

def attack(item,
           duration=300, 
           frames=10,
           target_x=(800 // 2),
           target_y=(300 // 2),
           start_delay=850):
    """ Анимация атаки предмета. Летит в центр! """
    current_x = item_x = item.winfo_x()
    current_y = item_y = item.winfo_y()
    item_width = item.winfo_width()
    item_height = item.winfo_height()
    path_x = (item_x - target_x) + item_width // 2 
    path_y = (item_y - target_y) + item_height // 2 
    step_x = -path_x // frames
    step_y = -path_y // frames
    step_delay = duration // frames
    cross_middle = False
    def step():
        nonlocal path_x, path_y, current_x, current_y, cross_middle
        if path_x * (path_x + step_x) <= 0 or path_y * (path_y + step_y) <= 0:
            cross_middle = True
        path_x += step_x
        path_y += step_y
        current_x += step_x
        current_y += step_y
        item.place(x=current_x, y=current_y)
        if not cross_middle:
            root.after(step_delay, step)
    root.after(start_delay, step)

def attack_to_side(bot_label,
                   player_label,
                   winner: str,
                   start_delay=WINNER_ATTACK_START_DELAY,
                   duration=WINNER_ATTACK_DURATION):
    """ Отправляет виджет к стороне противника или ничего если draw"""
    win_item = None
    if winner == 'bot':
        attack(bot_label, 
               duration=duration, 
               target_x=800, 
               start_delay=start_delay)
        one_item_hide(player_label, start_delay=start_delay)
        win_item = bot_label
    elif winner == 'player':
        attack(player_label,
               duration=duration, 
               target_x=0, 
               start_delay=start_delay)
        one_item_hide(bot_label, start_delay=start_delay)
        win_item = player_label
    else:
        one_item_hide(player_label, start_delay=start_delay)
        one_item_hide(bot_label, start_delay=start_delay)

    return win_item

def explosion_animation(item, duration=500, start_delay=1100):
    def wrapper(item):
        item.place(x=item.x, y=item.y)
        root.after(duration, item.place_forget)
    root.after(start_delay, wrapper, item)

def create_healthbar(root,
                     x,
                     y,
                     width,
                     height,
                     out_color='red',
                     inner_color='green',):
    
    outer = tk.Frame(root, bg=out_color, width=width, height=height)
    outer.place(x=x, y=y)
    outer.update_idletasks()
    inner = tk.Frame(root, bg=inner_color, width=width, height=height)
    inner.place(x = x, y = y)
    inner.update_idletasks()

    return inner

def down_health(inner_bot, inner_player, who_wins='draw'):
    
    if who_wins == 'bot':
        inner = inner_player
    elif who_wins == 'player':
        inner = inner_bot
    else:
        return
    
    current_width = inner.winfo_width()
    current_x = inner.winfo_x()
    new_width = max(int(current_width - 10), 0)
    inner.config(width=new_width)
    if who_wins == 'bot':
        new_x = max(current_x + 10, 0)
        inner.place(x=new_x)


# Инициализация окна
root = tk.Tk()
root.geometry("800x300")
root.title("Игра Камень/Ножницы/Бумага")

bot_label = create_widget(root=root,
              img_path="question-mark.png",
              x=100,
              y=80,
              name="?",
              clickable=False,
              default_img_path="question-mark.png")

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
explosion = create_widget(root,
                          img_path='explosion.png',
                          x = 300,
                          y = 50,
                          name='explosion',
                          default_unvisible=True,
                          width=200,
                          height=200)

bot_health = create_healthbar(root, x=20, y=20, width=300, height=20)
player_health = create_healthbar(root, x=490, y=20, width=300, height=20)

list_obj_labels = [scissors, stone, paper, bot_label]


root.mainloop()