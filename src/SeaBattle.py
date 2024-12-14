from tkinter import *
from tkinter import messagebox
import time
import random

tk = Tk()
app_running = True
size_of_field_x = 650
size_of_field_y = 550
size_x = size_y = 10
move_x = size_of_field_x // size_x  # шаг по горизонтали
move_y = size_of_field_y // size_y  # шаг по вертикали
# коррект размера вафельной разметки под размер поля
size_of_field_x = move_x * size_x
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
# hit - список попаданий по кораблям противника
hit = [[0 for i in range(size_x)] for i in range(size_y)]
# ships_list - список кораблей игрока 1 и игрока 2
ships_list = []
# hod_igrovomu_polu_1 - если Истина - то ходит Admiral No. 2, иначе ходит Admiral No. 1
hod_igrovomu_polu_1 = False
add_to_label = ""
add_to_label2 = ""


def on_closing():
    """Остановка приложения при закрытии окна.

    Эта функция вызывается при попытке закрыть главное окно приложения.
    Она отображает диалоговое окно с вопросом о подтверждении выхода из игры. 
    Если пользователь подтверждает выход, приложение завершает свою работу.

    :return: None
    """
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
canvas.create_rectangle(0, 0, size_of_field_x,
                        size_of_field_y, fill="SteelBlue1")
canvas.create_rectangle(size_of_field_x + otl_info_x, 0, size_of_field_x + otl_info_x + size_of_field_x, size_of_field_y,
                        fill="SteelBlue2")
canvas.pack()
tk.update()


def draw_table(offset_x=0):
    """Отображение сетки игрового поля.

    Рисует сетку на игровом поле с указанным смещением по оси X.

    :param int offset_x: Смещение по оси X (по умолчанию 0)
    :return: None
    """
    for i in range(0, size_x + 1):
        canvas.create_line(offset_x + move_x * i, 0,
                           offset_x + move_x * i, size_of_field_y)
    for i in range(0, size_y + 1):
        canvas.create_line(offset_x, move_y * i, offset_x +
                           size_of_field_x, move_y * i)


draw_table()
draw_table(size_of_field_x + otl_info_x)

t0 = Label(tk, text="Admiral No. 1", font=("Times New Roman", 16))
t0.place(x=size_of_field_x // 2 - t0.winfo_reqwidth() //
         2, y=size_of_field_y + 3)
t1 = Label(tk, text="Admiral No. 2", font=("Times New Roman", 16))
t1.place(x=size_of_field_x + otl_info_x + size_of_field_x //
         2 - t1.winfo_reqwidth() // 2, y=size_of_field_y + 3)

t0.configure(bg="tomato")
t0.configure(bg="#f0f0f0")

t3 = Label(tk, text="@@@@@@@", font=("Times New Roman", 16))
t3.place(x=size_of_field_x + otl_info_x//2 -
         t3.winfo_reqwidth() // 2, y=size_of_field_y)


def mark_igrok(igrok_mark_1):
    """Маркер текущего хода игрока.

    Функция изменяет внешний вид меток в зависимости от того, 
    чей сейчас ход. Если `igrok_mark_1` равен `True`, 
    то метка `t0` подсвечивается оранжевым цветом,
    а метка `t1` становится серого цвета. Если `False`, то наоборот.
    :param bool igrok_mark_1: Флаг, показывающий, чей сейчас ход
    :return: None
    """
    if igrok_mark_1:
        t0.configure(bg="orange")
        t0.configure(text="Admiral No. 1"+add_to_label2)
        t0.place(x=size_of_field_x // 2 - t0.winfo_reqwidth() //
                 2, y=size_of_field_y + 3)
        t1.configure(text="Admiral No. 2" + add_to_label)
        t1.place(x=size_of_field_x + otl_info_x + size_of_field_x //
                 2 - t1.winfo_reqwidth() // 2, y=size_of_field_y + 3)
        t1.configure(bg="#f0f0f0")
        t3.configure(text="Move Admiral No. 2"+add_to_label)
        t3.place(x=size_of_field_x + otl_info_x // 2 -
                 t3.winfo_reqwidth() // 2, y=size_of_field_y)
    else:
        t1.configure(bg="orange")
        t0.configure(bg="#f0f0f0")
        t0.configure(text="Admiral No. 1")
        t0.place(x=size_of_field_x // 2 - t0.winfo_reqwidth() //
                 2, y=size_of_field_y + 3)
        t1.configure(text="Admiral No. 2" + add_to_label)
        t1.place(x=size_of_field_x + otl_info_x + size_of_field_x //
                 2 - t1.winfo_reqwidth() // 2, y=size_of_field_y + 3)
        t3.configure(text="Move Admiral No. 1")
        t3.place(x=size_of_field_x + otl_info_x // 2 -
                 t3.winfo_reqwidth() // 2, y=size_of_field_y)


mark_igrok(hod_igrovomu_polu_1)


def button_show_enemy1():
    """Показать корабли первого игрока.

    Функция показывает расположение кораблей первого игрока на игровом поле.

    :return: None
    """
    for i in range(0, size_x):
        for j in range(0, size_y):
            if enemy_ships1[j][i] > 0:
                color = "orange"
                _id = canvas.create_rectangle(i * move_x, j * move_y, i * move_x + move_x, j * move_y + move_y,
                                              fill=color)
                list_ids.append(_id)


def button_show_enemy2():
    """Показать корабли второго игрока.

    Функция показывает расположение кораблей второго игрока на игровом поле.

    :return: None
    """
    for i in range(0, size_x):
        for j in range(0, size_y):
            if enemy_ships2[j][i] > 0:
                color = "orange"
                id = canvas.create_rectangle(size_of_field_x + otl_info_x + i * move_x, j * move_y,
                                             size_of_field_x + otl_info_x + i * move_x + move_x, j * move_y + move_y,
                                             fill=color)
                list_ids.append(id)


def button_begin_again():
    """Начало новой игры.

    Функция очищает игровое поле, генерирует новые корабли и сбрасывает все игровые данные для начала новой партии.

    :return: None
    """
    global list_ids
    global points1, points2
    global hit
    global enemy_ships1, enemy_ships2

    for el in list_ids:
        canvas.delete(el)
    list_ids = []
    generate_ships_list()
    enemy_ships1 = generate_enemy_ships()
    enemy_ships2 = generate_enemy_ships()
    points1 = [[-1 for i in range(size_x)] for i in range(size_y)]
    points2 = [[-1 for i in range(size_x)] for i in range(size_y)]
    hit = [[0 for i in range(size_x)]
           for i in range(size_y)]  # Сброс списка попаданий


knpk0 = Button(tk, text="show the ships \n Admiral No. 1",
               command=button_show_enemy1)
knpk0.place(x=size_of_field_x + otl_info_x //
            2 - knpk0.winfo_reqwidth() // 2, y=10)

knpk1 = Button(tk, text="show the ships \n Admiral No. 2",
               command=button_show_enemy2)
knpk1.place(x=size_of_field_x + otl_info_x //
            2 - knpk1.winfo_reqwidth() // 2, y=60)

knpk2 = Button(tk, text="start again", command=button_begin_again)
knpk2.place(x=size_of_field_x + otl_info_x // 2 -
            knpk2.winfo_reqwidth() // 2, y=110)


def draw_point(x, y):
    """Рисует символ на игровом поле в зависимости от значения в массиве `enemy_ships1`.

    Если значение в массиве `enemy_ships1` равно 0, то рисует эмодзи "🌀". Если значение больше 0, то рисует эмодзи "💥".

    :param int x: Координата X.
    :param int y: Координата Y.
    :return: None
    """
    if enemy_ships1[y][x] == 0:
        color = "lightcyan"
        elem1 = canvas.create_text(x * move_x + move_x // 2, y * move_y + move_y // 2,
                                   text='🌀', font=(60, 60), fill=color)

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

        list_ids.append(elem1, elem2, elem3)


def draw_point2(x, y, offset_x=size_of_field_x + otl_info_x):
    """Рисует символ на игровом поле в зависимости от значения в массиве `enemy_ships2`.

    Если значение в массиве `enemy_ships2` равно 0, то рисует эмодзи "🌀". Если значение больше 0, то рисует эмодзи "💥".

    :param int x: Координата X.
    :param int y: Координата Y.
    :param int offset_x: Смещение по оси X.
    :return: None
    """
    if enemy_ships2[y][x] == 0:
        color = "lightcyan"
        elem1 = canvas.create_text(offset_x + x * move_x + move_x // 2, y * move_y + move_y // 2,
                                   text='🌀', font=(60, 60), fill=color)
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
    """Проверяет, выиграл ли первый игрок.

    Если значение в массиве `enemy_ships1` больше нуля, то записывает в массив `hit` значение из массива `enemy_ships1`.

    Затем сравнивает сумму элементов в массиве `enemy_ships1` с суммой элементов в массиве `hit`. Если суммы равны, возвращает `True`, что означает, что первый игрок выиграл.

    :param int x: Координата X.
    :param int y: Координата Y.
    :return: Логический результат, который указывает, выиграл ли первый игрок.
    """
    win = False
    if enemy_ships1[y][x] > 0:
        hit[y][x] = enemy_ships1[y][x]
    sum_enemy_ships1 = sum(sum(i) for i in zip(*enemy_ships1))
    sum_hit = sum(sum(i) for i in zip(*hit))
    if sum_enemy_ships1 == sum_hit:
        win = True
    return win


def check_winner2():
    """Проверяет, выиграл ли второй игрок (игрок №2).

    Проходит через все элементы массива `enemy_ships2`, проверяет наличие незаполненных элементов (значение равно -1). Если такие элементы обнаружены, функция возвращает `False`, что означает, что второй игрок еще не выиграл. Если все элементы заполнены, функция возвращает `True`, что означает, что второй игрок выиграл.

    **Параметры**:
     - `i` и `j` — индексы в двумерной матрице `enemy_ships2`, соответствующие координатам по осям `x` и `y`.

    **Возвращение значения**:
      - `win` — логическое значение, которое указывает на статус победы второго игрока. Если `win` равно `True`, это означает, что второй игрок выиграл. Если `win` равно `False`, это означает, что второй игрок еще не выиграл.
    """
    win = True
    for i in range(0, size_x):
        for j in range(0, size_y):
            if enemy_ships1[j][i] > 0:
                if points1[j][i] == -1:
                    win = False
    return win


def check_winner2_igrok_2():
    """Проверяет, выиграл ли второй игрок (игрок №2).

    Проходит через все элементы массива `enemy_ships2`, проверяет наличие незаполненных элементов (значение равно -1). Если такие элементы обнаружены, функция возвращает `False`, что означает, что второй игрок еще не выиграл. Если все элементы заполнены, функция возвращает `True`, что означает, что второй игрок выиграл.

    **Параметры**:
     - `i` и `j` — индексы в двумерной матрице `enemy_ships2`, соответствующие координатам по осям `x` и `y`.

    **Возвращение значения**:
      - `win` — логическое значение, которое указывает на статус победы второго игрока.
      """
    win = True
    for i in range(0, size_x):
        for j in range(0, size_y):
            if enemy_ships2[j][i] > 0:
                if points2[j][i] == -1:
                    win = False
    return win


def add_to_all(incident):
    """Добавляет выстрелы к игровому полю. 

    Функция обрабатывает событие выстрела (левая или правая кнопка мыши) 
    и добавляет его к соответствующему игровому полю. 
    Если все корабли противника уничтожены, объявляется победитель и игра сбрасывается. 

    :param incident: Событие выстрела (левая или правая кнопка мыши). 
    """
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
                elem2 = canvas.create_rectangle(move_x * 3+move_x//2, size_of_field_y // 2 + move_y//2,
                                                size_of_field_x + otl_info_x + size_of_field_x - move_x * 3 - move_x//2,
                                                size_of_field_y // 2+move_y+move_y // 2 + 60 + 30 + move_y // 2 - move_y//2, fill="white")
                list_ids.append(elem2)
                elem3 = canvas.create_text(size_of_field_x+otl_info_x//2, size_of_field_y // 2 +
                                           move_y+move_y // 2, text=winner, font=("Times New Roman", 50), justify=CENTER)
                elem4 = canvas.create_text(size_of_field_x+otl_info_x//2, size_of_field_y // 2+move_y +
                                           move_y // 2 + 50, text=winner_add, font=("Times New Roman", 25), justify=CENTER)
                list_ids.append(elem3)
                list_ids.append(elem4)

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
                                                fill="red")
                list_ids.append(elem1)
                elem2 = canvas.create_rectangle(move_x * 3 + move_x // 2, size_of_field_y // 2 + move_y // 2,
                                                size_of_field_x + otl_info_x + size_of_field_x - move_x * 3 - move_x // 2,
                                                size_of_field_y // 2 + move_y + move_y // 2 +
                                                60 + 30 + move_y // 2 - move_y // 2,
                                                fill="white")
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
    """Генерирует список случайных длин кораблей. 

    Эта функция создает список случайных чисел, представляющих длину кораблей. 
    Длина каждого корабля выбирается случайно из списка возможных значений. 

    :return: None 

    """
    global ships_list
    ships_list = []
    # генерируем список случайных длин кораблей
    for i in range(0, ships):
        ships_list.append(random.choice(
            [ship_len1, ship_len2, ship_len3, ship_len4]))


def generate_enemy_ships():
    """Генерирует расположение кораблей противника. 

    Эта функция пытается сгенерировать случайное размещение кораблей противника на поле. 
    Если сумма всех единиц (подбитых кораблей) совпадает с общей суммой длин кораблей, 
    то возвращается сгенерированное поле. 

    :return: Список, представляющий расположение кораблей противника. 

    """
    global ships_list
    enemy_ships = []

    # подсчет суммарной длины кораблей
    sum_1_all_ships = sum(ships_list)
    sum_1_enemy = 0

    while sum_1_enemy != sum_1_all_ships:
        # обнуляем массив кораблей врага
        enemy_ships = [[0 for i in range(size_x + 1)] for i in
                       # +1 для доп. линии справа и снизу, для успешных проверок генерации противника
                       range(size_y + 1)]

        for i in range(0, ships):
            len = ships_list[i]
            # 1- горизонтальное 2 - вертикальное
            horizont_vertikal = random.randrange(1, 3)

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
                                # записываем номер корабля
                                enemy_ships[primerno_y][primerno_x + j] = i + 1
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
                                # записываем номер корабля
                                enemy_ships[primerno_y + j][primerno_x] = i + 1
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
