from tkinter import *
from tkinter import messagebox
import time
import random

tk = Tk()
app_running = True

size_of_field_x = 650
size_of_field_y = 550
print("choose the size of the field")
Razm = int(input())

size_x = size_y = Razm
move_x = size_of_field_x // size_x  # шаг по горизонтали
move_y = size_of_field_y // size_y  # шаг по вертикали
size_of_field_x = move_x * size_x #коррект размера вафельной разметки под размер поля
size_of_field_y = move_y * size_y 
size_font_x = 10
len_txt_x = 14*size_font_x
delta_otl_info_x = len_txt_x // move_x + 1
otl_info_x = move_x * delta_otl_info_x

otl_info_y = 40
ships = size_x // 2  # определяем максимальное кол-во кораблей
ship_len1 = size_x // 5  # длина первого типа корабля
ship_len2 = size_x // 4  # длина второго типа корабля
ship_len3 = size_x // 3  # длина второго типа корабля
ship_len4 = size_x // 2  # длина третьего типа корабля
enemy_ships1 = [[0 for i in range(size_x + 1)] for i in range(size_y + 1)]
enemy_ships2 = [[0 for i in range(size_x + 1)] for i in range(size_y + 1)]
list_ids = []  # список объектов canvas
# points1 - список точек в которые кликнули мышкой
points1 = [[-1 for i in range(size_x)] for i in range(size_y)]
points2 = [[-1 for i in range(size_x)] for i in range(size_y)]
# popadaniya - список попаданий по кораблям противника
popadaniya = [[0 for i in range(size_x)] for i in range(size_y)]
# ships_list - список кораблей игрока 1 и игрока 2
ships_list = []
# hod_igrovomu_polu_1 - если Истина - то ходит Admiral No. 2, иначе ходит Admiral No. 1
hod_igrovomu_polu_1 = False
add_to_label = ""
add_to_label2 = ""

def on_closing():
    global app_running
    if messagebox.askokcancel("exiting the game", "Do you want to quit the game??"):
        app_running = False
        tk.destroy()

tk.protocol("WM_DELETE_WINDOW", on_closing)
tk.title("Naval battle")
tk.resizable(0, 0)
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=size_of_field_x + otl_info_x + size_of_field_x, height=size_of_field_y + otl_info_y, bd=0,
                highlightthickness=0)
canvas.create_rectangle(0, 0, size_of_field_x, size_of_field_y, fill="SteelBlue1")
canvas.create_rectangle(size_of_field_x + otl_info_x, 0, size_of_field_x + otl_info_x + size_of_field_x, size_of_field_y,
                        fill="SteelBlue2")
canvas.pack()
tk.update()

def draw_table(offset_x=0):
    for i in range(0, size_x + 1):
        canvas.create_line(offset_x + move_x * i, 0, offset_x + move_x * i, size_of_field_y)
    for i in range(0, size_y + 1):
        canvas.create_line(offset_x, move_y * i, offset_x + size_of_field_x, move_y * i)

draw_table()
draw_table(size_of_field_x + otl_info_x)

t0 = Label(tk, text="Admiral No. 1", font=("Times New Roman", 16))
t0.place(x=size_of_field_x // 2 - t0.winfo_reqwidth() // 2, y=size_of_field_y + 3)
t1 = Label(tk, text="Admiral No. 2", font=("Times New Roman", 16))
t1.place(x=size_of_field_x + otl_info_x + size_of_field_x // 2 - t1.winfo_reqwidth() // 2, y=size_of_field_y + 3)

t0.configure(bg="tomato")
t0.configure(bg="#f0f0f0")

t3 = Label(tk, text="@@@@@@@", font=("Times New Roman", 16))
t3.place(x=size_of_field_x + otl_info_x//2 - t3.winfo_reqwidth() // 2, y= size_of_field_y)


def mark_igrok(igrok_mark_1):
    if igrok_mark_1:
        t0.configure(bg="orange")
        t0.configure(text="Admiral No. 1"+add_to_label2)
        t0.place(x=size_of_field_x // 2 - t0.winfo_reqwidth() // 2, y=size_of_field_y + 3)
        t1.configure(text="Admiral No. 2" + add_to_label)
        t1.place(x=size_of_field_x + otl_info_x + size_of_field_x // 2 - t1.winfo_reqwidth() // 2, y=size_of_field_y + 3)
        t1.configure(bg="#f0f0f0")
        t3.configure(text="Move Admiral No. 2"+add_to_label)
        t3.place(x=size_of_field_x + otl_info_x // 2 - t3.winfo_reqwidth() // 2, y=size_of_field_y)
    else:
        t1.configure(bg="orange")
        t0.configure(bg="#f0f0f0")
        t0.configure(text="Admiral No. 1")
        t0.place(x=size_of_field_x // 2 - t0.winfo_reqwidth() // 2, y=size_of_field_y + 3)
        t1.configure(text="Admiral No. 2" + add_to_label)
        t1.place(x=size_of_field_x + otl_info_x + size_of_field_x // 2 - t1.winfo_reqwidth() // 2, y=size_of_field_y + 3)
        t3.configure(text="Move Admiral No. 1")
        t3.place(x=size_of_field_x + otl_info_x // 2 - t3.winfo_reqwidth() // 2, y=size_of_field_y)
mark_igrok(hod_igrovomu_polu_1)


def button_show_enemy1(): 
    for i in range(0, size_x):
        for j in range(0, size_y):
            if enemy_ships1[j][i] > 0:
                color = "orange"

                _id = canvas.create_rectangle(i * move_x, j * move_y, i * move_x + move_x, j * move_y + move_y,
                                              fill=color)
                list_ids.append(_id)

def button_show_enemy2():
    for i in range(0, size_x):
        for j in range(0, size_y):
            if enemy_ships2[j][i] > 0:
                color = "orange"
                id = canvas.create_rectangle(size_of_field_x + otl_info_x + i * move_x, j * move_y,
                                              size_of_field_x + otl_info_x + i * move_x + move_x, j * move_y + move_y,
                                              fill=color)
                list_ids.append(id)

def button_begin_again():
    global list_ids
    global points1, points2
    global popadaniya
    global enemy_ships1, enemy_ships2
    for el in list_ids:
        canvas.delete(el)
    list_ids = []
    generate_ships_list()
    enemy_ships1 = generate_enemy_ships()
    enemy_ships2 = generate_enemy_ships()
    points1 = [[-1 for i in range(size_x)] for i in range(size_y)]
    points2 = [[-1 for i in range(size_x)] for i in range(size_y)]
    popadaniya = [[0 for i in range(size_x)] for i in range(size_y)]
    
knpk0 = Button(tk, text="show the ships \n Admiral No. 1", command=button_show_enemy1)
knpk0.place(x=size_of_field_x + otl_info_x // 2 - knpk0.winfo_reqwidth() // 2, y=10)

knpk1 = Button(tk, text="show the ships \n Admiral No. 2", command=button_show_enemy2)
knpk1.place(x=size_of_field_x + otl_info_x // 2 - knpk1.winfo_reqwidth() // 2, y=60)

knpk2 = Button(tk, text="start again", command=button_begin_again)
knpk2.place(x=size_of_field_x + otl_info_x // 2 - knpk2.winfo_reqwidth() // 2, y=110)

def draw_point(x, y):
    # Если значение равно 0, то рисуем эмодзи 🥛
    if enemy_ships1[y][x] == 0:
        color = "lightcyan"
        elem1 = canvas.create_text(x * move_x + move_x // 2, y * move_y + move_y // 2, 
                                 text='💦', font=(60, 60), fill=color)
                                 
        list_ids.append(elem1)
    
    # Если значение больше 0, то рисуем эмодзи 💥
    elif enemy_ships1[y][x] > 0:
        color = "white"
        elem1 = canvas.create_text(x * move_x + move_x // 2, y * move_y + move_y // 2, 
                                 text='💥', font=(80, 80), fill=color)
        color1 = "orange"
        elem2 = canvas.create_text(x * move_x + move_x // 2, y * move_y + move_y // 2, 
                                 text='💥', font=(60, 60), fill=color1)
        color2 = "red"
        elem3 = canvas.create_text(x * move_x + move_x // 2, y * move_y + move_y // 2, 
                                 text='💥', font=(35, 35), fill=color2)

        list_ids.append(elem1,elem2,elem3)

def draw_point2(x, y, offset_x=size_of_field_x + otl_info_x):
    # Если значение равно 0, то рисуем эмодзи 🥛
    if enemy_ships2[y][x] == 0:
        color = "lightcyan"
        elem1 = canvas.create_text(offset_x + x * move_x + move_x // 2, y * move_y + move_y // 2, 
                                 text='💦', font=(60, 60), fill=color)
        list_ids.append(elem1)
    
    # Если значение больше 0, то рисуем эмодзи 💥
    elif enemy_ships2[y][x] > 0:
        color = "white"
        elem1 = canvas.create_text(offset_x + x * move_x + move_x // 2, y * move_y + move_y // 2, 
                                 text='💥', font=(80, 80), fill=color)
        color1 = "orange"
        elem2 = canvas.create_text(offset_x + x * move_x + move_x // 2, y * move_y + move_y // 2, 
                                 text='💥', font=(60, 60), fill=color1)
        color2 = "red"
        elem3 = canvas.create_text(offset_x + x * move_x + move_x // 2, y * move_y + move_y // 2, 
                                 text='💥', font=(35, 35), fill=color2)
        list_ids.append(elem1, elem2, elem3)

def check_winner(x, y):
    win = False
    if enemy_ships1[y][x] > 0:
        popadaniya[y][x] = enemy_ships1[y][x]
    sum_enemy_ships1 = sum(sum(i) for i in zip(*enemy_ships1))
    sum_popadaniya = sum(sum(i) for i in zip(*popadaniya))
    if sum_enemy_ships1 == sum_popadaniya:
        win = True
    return win


def check_winner2():
    win = True
    for i in range(0, size_x):
        for j in range(0, size_y):
            if enemy_ships1[j][i] > 0:
                if points1[j][i] == -1:
                    win = False
    return win

def check_winner2_igrok_2():
    win = True
    for i in range(0, size_x):
        for j in range(0, size_y):
            if enemy_ships2[j][i] > 0:
                if points2[j][i] == -1:
                    win = False
    return win

def add_to_all(incident):
    global points1, points2, hod_igrovomu_polu_1
    _type = 0  # ЛКМ
    if incident.num == 3:
        _type = 1  # ПКМ
    mouse_x = canvas.winfo_pointerx() - canvas.winfo_rootx()
    mouse_y = canvas.winfo_pointery() - canvas.winfo_rooty()
    ip_x = mouse_x // move_x
    ip_y = mouse_y // move_y

    if ip_x < size_x and ip_y < size_y and hod_igrovomu_polu_1:
        if points1[ip_y][ip_x] == -1:
            points1[ip_y][ip_x] = _type
            hod_igrovomu_polu_1 = False
            draw_point(ip_x, ip_y)

            if check_winner2():
                hod_igrovomu_polu_1 = True
                winner = "Admiral's victory No. 2"
                winner_add = "All ships of the opponent of Player No. 1 are hit!!!"
                print(winner, winner_add)
                points1 = [[10 for i in range(size_x)] for i in range(size_y)]
                points2 = [[10 for i in range(size_x)] for i in range(size_y)]
                elem1 = canvas.create_rectangle(move_x*3, size_of_field_y // 2, size_of_field_x + otl_info_x + size_of_field_x-move_x*3,
                                                 size_of_field_y // 2+move_y+move_y // 2 + 60 + 30 + move_y // 2, fill="red")
                list_ids.append(elem1)
                elem2 = canvas.create_rectangle(move_x * 3+move_x//2, size_of_field_y // 2 +move_y//2,
                                              size_of_field_x + otl_info_x + size_of_field_x - move_x * 3 - move_x//2,
                                              size_of_field_y // 2+move_y+move_y // 2 + 60 + 30 + move_y // 2 - move_y//2, fill="white")
                list_ids.append(elem2)
                elem3 = canvas.create_text(size_of_field_x+otl_info_x//2, size_of_field_y // 2+move_y+move_y // 2, text=winner, font=("Times New Roman", 50), justify=CENTER)
                elem4 = canvas.create_text(size_of_field_x+otl_info_x//2, size_of_field_y // 2+move_y+move_y // 2 + 50, text=winner_add, font=("Times New Roman", 25), justify=CENTER)
                list_ids.append(elem3)
                list_ids.append(elem4)

    #орисовка второго игрового поля
    if ip_x >= size_x + delta_otl_info_x and ip_x <= size_x + size_x + delta_otl_info_x and ip_y < size_y and not hod_igrovomu_polu_1:

        if points2[ip_y][ip_x - size_x - delta_otl_info_x] == -1:
            points2[ip_y][ip_x - size_x - delta_otl_info_x] = _type
            hod_igrovomu_polu_1 = True
            draw_point2(ip_x - size_x - delta_otl_info_x, ip_y)

            if check_winner2_igrok_2():
                hod_igrovomu_polu_1 = False
                winner = "Admiral's victory No. 1"
                winner_add = "All ships of the opponent of Player No. 2 are hit!!!"
                print(winner, winner_add)
                points1 = [[10 for i in range(size_x)] for i in range(size_y)]
                points2 = [[10 for i in range(size_x)] for i in range(size_y)]
                elem1 = canvas.create_rectangle(move_x * 3, size_of_field_y // 2,
                                              size_of_field_x + otl_info_x + size_of_field_x - move_x * 3,
                                              size_of_field_y // 2 + move_y + move_y // 2 + 60 + 30 + move_y // 2,
                                              fill="blue")
                list_ids.append(elem1)
                elem2 = canvas.create_rectangle(move_x * 3 + move_x // 2, size_of_field_y // 2 + move_y // 2,
                                              size_of_field_x + otl_info_x + size_of_field_x - move_x * 3 - move_x // 2,
                                              size_of_field_y // 2 + move_y + move_y // 2 + 60 + 30 + move_y // 2 - move_y // 2,
                                              fill="yellow")
                list_ids.append(elem2)
                elem3 = canvas.create_text(size_of_field_x + otl_info_x // 2, size_of_field_y // 2 + move_y + move_y // 2,
                                         text=winner, font=("Times New Roman", 50), justify=CENTER)
                elem4 = canvas.create_text(size_of_field_x + otl_info_x // 2, size_of_field_y // 2 + move_y + move_y // 2 + 50,
                                         text=winner_add, font=("Times New Roman", 25), justify=CENTER)
                list_ids.append(elem3)
                list_ids.append(elem4)
    mark_igrok(hod_igrovomu_polu_1)

canvas.bind_all("<Button-1>", add_to_all)  # ЛКМ
canvas.bind_all("<Button-3>", add_to_all)  # ПКМ

def generate_ships_list():
    global ships_list
    ships_list = []
    # генерируем список случайных длин кораблей
    for i in range(0, ships):
        ships_list.append(random.choice([ship_len1, ship_len2, ship_len3, ship_len4]))

def generate_enemy_ships():
    global ships_list
    enemy_ships = []

    # подсчет суммарной длины кораблей
    sum_1_all_ships = sum(ships_list)
    sum_1_enemy = 0

    while sum_1_enemy != sum_1_all_ships:
        # обнуляем массив кораблей врага
        enemy_ships = [[0 for i in range(size_x + 1)] for i in
                       range(size_y + 1)]  # +1 для доп. линии справа и снизу, для успешных проверок генерации противника

        for i in range(0, ships):
            len = ships_list[i]
            horizont_vertikal = random.randrange(1, 3)  # 1- горизонтальное 2 - вертикальное

            primerno_x = random.randrange(0, size_x)
            if primerno_x + len > size_x:
                primerno_x = primerno_x - len

            primerno_y = random.randrange(0, size_y)
            if primerno_y + len > size_y:
                primerno_y = primerno_y - len

            if horizont_vertikal == 1:
                if primerno_x + len <= size_x:
                    for j in range(0, len):
                        try:
                            check_near_ships = 0
                            check_near_ships = enemy_ships[primerno_y][primerno_x - 1] + \
                                               enemy_ships[primerno_y][primerno_x + j] + \
                                               enemy_ships[primerno_y][primerno_x + j + 1] + \
                                               enemy_ships[primerno_y + 1][primerno_x + j + 1] + \
                                               enemy_ships[primerno_y - 1][primerno_x + j + 1] + \
                                               enemy_ships[primerno_y + 1][primerno_x + j] + \
                                               enemy_ships[primerno_y - 1][primerno_x + j]

                            if check_near_ships == 0:  # записываем в том случае, если нет ничего рядом
                                enemy_ships[primerno_y][primerno_x + j] = i + 1  # записываем номер корабля
                        except Exception:
                            pass
            if horizont_vertikal == 2:
                if primerno_y + len <= size_y:
                    for j in range(0, len):
                        try:
                            check_near_ships = 0
                            check_near_ships = enemy_ships[primerno_y - 1][primerno_x] + \
                                               enemy_ships[primerno_y + j][primerno_x] + \
                                               enemy_ships[primerno_y + j + 1][primerno_x] + \
                                               enemy_ships[primerno_y + j + 1][primerno_x + 1] + \
                                               enemy_ships[primerno_y + j + 1][primerno_x - 1] + \
                                               enemy_ships[primerno_y + j][primerno_x + 1] + \
                                               enemy_ships[primerno_y + j][primerno_x - 1]

                            if check_near_ships == 0:  # записываем в том случае, если нет ничего рядом
                                enemy_ships[primerno_y + j][primerno_x] = i + 1  # записываем номер корабля
                        except Exception:
                            pass

        # делаем подсчет единиц (подбитых кораблей)
        sum_1_enemy = 0
        for i in range(0, size_x):
            for j in range(0, size_y):
                if enemy_ships[j][i] > 0:
                    sum_1_enemy = sum_1_enemy + 1
    return enemy_ships


generate_ships_list()

enemy_ships1 = generate_enemy_ships()
enemy_ships2 = generate_enemy_ships()

while app_running:
    if app_running:
        tk.update_idletasks()
        tk.update()
    time.sleep(0.01)