import datetime
import sqlite3
import subprocess
import webbrowser
from tkinter import messagebox
from tkinter import *
from tkinter.ttk import *

class connect_db:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connector = sqlite3.connect(self.db_name)
        self.cursor = self.connector.cursor()

    def execute_sql(self, sql_txt):
        try:
            self.sql_txt = sql_txt
            return self.cursor.execute(self.sql_txt)
        except:
            messagebox.showerror("Ошибка!", "Нет возможности в получении данных с базы данных!")

    def close_db(self):
        self.connector.commit()
        self.cursor.close()
        self.connector.close()

class my_window:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("900x400")
        self.window.title("Мастерская кота Феликса! - Вы ломаете, мы чиним!")

        self.window.iconbitmap(default="image/logo.ico")

        self.old_name = ""
        self.price = 0
        self.price2 = 0
        self.sum = 0

        self.kol_tovar_sklad = 0

        self.kupleno_kol = 0
        self.prodano_kol = 0
        self.ostatok_kol = 0

        self.kupleno_sum = 0
        self.prodano_sum = 0
        self.ostatok_sum = 0

        self.popular_tovar = "None"
        self.UNpopular_tovar = "None"

        self.create_frames()
        self.secret()
        self.secret2()
        self.secret3()

        self.window.mainloop()

    def secret(self):
        self.canva = Canvas(self.frame1, width=900, height=200, bg="lightblue", highlightthickness=0)
        self.canva.place(x=0, y=250)

        self.img_m = PhotoImage(file="image/magazin.png")
        self.img_del = PhotoImage(file="image/delivery.png")
        self.img_tovar = PhotoImage(file="image/tovar.png")

        self.image_magazin = self.canva.create_image(800, 60, image=self.img_m)
        self.image_delivery = self.canva.create_image(60, 60, image=self.img_del, state="hidden")
        self.image_tovar = self.canva.create_image(750, 100, image=self.img_tovar, state="hidden")

        self.canva.tag_bind(self.image_magazin, "<Button-1>", lambda  event: self.secret_move())

    def secret_move(self):
        self.canva.itemconfig(self.image_delivery, state="normal")
        self.canva.itemconfig(self.image_tovar, state="hidden")
        self.x, self.y = self.canva.coords(self.image_delivery)

        if self.x < 800:
            self.canva.move(self.image_delivery, 10, 0)
            self.canva.after(20, self.secret_move)
        else:
            self.canva.itemconfig(self.image_delivery, state="hidden")
            self.canva.coords(self.image_delivery, 60, 60)
            self.canva.itemconfig(self.image_tovar, state="normal")

            otvet = messagebox.askyesno("Доставлен фулл!", "Не желаете ли вы открыть фулл?")

            if otvet:
                webbrowser.open('https://vk.com/video549005895_456239047', new=2)



    def secret2(self):
        self.canva2 = Canvas(self.frame2, width=250, height=400, bg="lightblue", highlightthickness=0)
        self.canva2.place(x=650, y=0)

        self.img_cat = PhotoImage(file="image/cat.png")
        self.cat = self.canva2.create_image(100, 300, image=self.img_cat)
        self.canva2.tag_bind(self.cat, "<Button-1>", lambda event: self.secret_move2())

    def secret_move2(self):
        otvet = messagebox.askyesno("МЯУ!", "Открыть посхалку?")

        if otvet:
            webbrowser.open('https://www.youtube.com/watch?v=jIQ6UV2onyI', new=2)


    def secret3(self):
        self.canva3 = Canvas(self.frame3, width=250, height=300, bg="lightblue", highlightthickness=0)
        self.canva3.place(x=650, y=100)

        self.click = False

        self.img_secret = PhotoImage(file="image/cat.png")
        self.scott = self.canva3.create_image(250, 280, image=self.img_secret)
        self.canva3.tag_bind(self.cat, "<Button-1>", lambda event: self.secret_move3())

    def secret_move3(self):
        self.x3, self.y3 = self.canva3.coords(self.scott)
        if not self.click:
            if self.x3 > 200 and self.y3 > 200:
                self.canva3.move(self.scott, -5, -5)
                self.canva3.after(20, self.secret_move3())
            else:
                self.click = True
        else:
            self.move_back()

    def move_back(self):
        self.x3, self.y3 = self.canva3.coords(self.scott)
        if self.x3 < 250 or self.y3 < 300:
            self.canva3.move(self.scott, 5, 5)
            self.canva3.after(20, self.move_back())
        else:
            self.click = False

    def update_tables(self, table):
        # очистка таблицы
        for row in table.get_children():
            table.delete(row)

        # подключение к БД
        self.new_connect = connect_db("magazin.db")

        # получение денных для таблицы "Товары"
        if table == self.table_tov:
            self.sql = self.new_connect.execute_sql(f"SELECT * from tovar")
            for row in self.sql:
                self.db_name = row[1]
                self.db_price = row[2]
                self.table_tov.insert("", END, values=[self.db_name, self.db_price])

        # получение данных для таблицы "Купить"
        elif table == self.table_buy:
            self.sql = self.new_connect.execute_sql(f"SELECT T.name, T.price, TB.kol, TB.sum from tovar_buy TB "
                                                    f"INNER JOIN tovar T "
                                                    f"on TB.id_tovar = T.id")

            for row in self.sql:
                self.db_name = row[0]
                self.db_price = row[1]
                self.db_kol = row[2]
                self.db_sum = row[3]

                self.table_buy.insert("", END,
                                      values=[self.db_name, self.db_price, self.db_kol, self.db_sum])

        # получение данных для таблицы "Продать"
        elif table == self.table_sell:
            self.sql = self.new_connect.execute_sql(f"SELECT T.name, T.price, TS.kol, TS.sum "
                                                    f"from tovar_sell TS "
                                                    f"INNER JOIN tovar T "
                                                    f"on TS.id_tovar = T.id")

            for row in self.sql:
                self.db_name = row[0]
                self.db_price = row[1]
                self.db_kol = row[2]
                self.db_sum = row[3]
                self.table_sell.insert("", END, values=[self.db_name, self.db_price, self.db_kol, self.db_sum])

        self.new_connect.close_db()

    def create_frames(self):
        # создаем набор вкладок
        self.notebook = Notebook()

        # добавляем стиль
        style = Style()
        # Настройка цвета фона внутри вкладки
        style.configure("TFrame", background = "lightblue")
        self.notebook.pack(expand=True, fill=BOTH)

        # создание фреймов
        self.frame1 = Frame(self.notebook)
        self.frame2 = Frame(self.notebook)
        self.frame3 = Frame(self.notebook)
        self.frame4 = Frame(self.notebook)

        self.frame1.pack(fill=BOTH, expand=True)
        self.frame2.pack(fill=BOTH, expand=True)
        self.frame3.pack(fill=BOTH, expand=True)
        self.frame4.pack(fill=BOTH, expand=True)

        # добавляем фреймы в качестве вкладок
        self.notebook.add(self.frame1, text="Товары")
        self.notebook.add(self.frame2, text="Купить")
        self.notebook.add(self.frame3, text="Продать")
        self.notebook.add(self.frame4, text="Информация")

        self.frame_tovar()
        self.frame_buy()
        self.frame_sell()
        self.frame_info()

    def sort_name(self, col, reverse, table):
        data = [(table.set(child, col), child) for child in table.get_children('')]
        data.sort(reverse=reverse)
        for index, (val, child) in enumerate(data):
            table.move(child, '', index)
        table.heading(col, command=lambda: self.sort_name(col, not reverse, table))

    def sort_number(self, col, reverse, table):
        data = [(float(table.set(child, col)), child) for child in table.get_children('')]
        data.sort(reverse=reverse)
        for index, (var, child) in enumerate(data):
            table.move(child, '', index)
        table.heading(col, command=lambda: self.sort_number(col, not reverse, table))

    def frame_tovar(self):
        # все это, это код таблицы
        self.table_tov = Treeview(self.frame1, columns=["tovar", "price"], show="headings")
        self.table_tov.heading("tovar", text="Товар", command=lambda: self.sort_name("tovar", False, self.table_tov))
        self.table_tov.heading("price", text="Цена для закупки", command=lambda: self.sort_number("price", False, self.table_tov))

        self.table_tov.column("tovar", width=150, anchor="c")
        self.table_tov.column("price", width=150, anchor="c")
        self.table_tov.place(x=10, y=10)

        # надписи и поля
        self.tovar_name = StringVar()
        self.lb_name = Label(self.frame1, text="Наименование товара:", font="Arial 12", background="lightblue")
        self.lb_name.place(x=350, y=20)

        self.entry_name = Entry(self.frame1, textvariable=self.tovar_name, font="Arial 12")
        self.entry_name.place(x=350, y=60)

        self.tovar_price = DoubleVar()
        self.lb_name = Label(self.frame1, text="Цена товара:", font="Arial 12", background="lightblue")
        self.lb_name.place(x=350, y=100)

        self.entry_price = Entry(self.frame1, textvariable=self.tovar_price, font="Arial 12")
        self.entry_price.place(x=350, y=140)

        # кнопки
        self.btn_new_tovar = Button(self.frame1, text="Добавить новый товар", command=self.create_tovar)
        self.btn_new_tovar.place(x=600, y=60)

        self.btn_del_tovar = Button(self.frame1, text="Удалить товар", command=self.del_tovar)
        self.btn_del_tovar.place(x=600, y=100)

        self.btn_update_tovar = Button(self.frame1, text="Изменить товар", command=self.update_tovar)
        self.btn_update_tovar.place(x=600, y=140)

        # заполнение таблицы
        self.update_tables(self.table_tov)

        # выбор отдной строки
        self.table_tov.bind("<<TreeviewSelect>>", lambda event:self.select_tovar(self.tovar_name, self.tovar_price))


    def select_tovar(self, tovar_name, tovar_price):
        for row in self.table_tov.selection():
            tovar_name.set(self.table_tov.item(row)["values"][0])
            tovar_price.set(self.table_tov.item(row)["values"][1])

            self.old_name = self.table_tov.item(row)["values"][0]

    def del_tovar(self):
        self.new_connect = connect_db("magazin.db")
        if self.tovar_name.get() != "":
            self.check = self.new_connect.execute_sql(f"SELECT * from tovar WHERE name = '{self.tovar_name.get()}'")
            if len(self.check.fetchall()) == 0:
                messagebox.showerror("Ошибка!", "Такого товара не существует!")
            else:
                otvet = messagebox.askyesno("Внимание!", "Товар будет удален. Вы уверены?")
                if otvet:
                    self.sql = self.new_connect.execute_sql(f"DELETE from tovar WHERE name = '{self.tovar_name.get()}'")
                    self.new_connect.close_db()
                    self.update_tables(self.table_tov)

        else:
            messagebox.showerror("Ошибка!", "Товар не выбран!")

    def create_tovar(self):
        if self.tovar_name.get() != "" and self.tovar_price.get() != "":
            self.new_connect = connect_db("magazin.db")

            self.replay = self.new_connect.execute_sql(f"SELECT * from tovar WHERE name = '{self.tovar_name.get()}'")
            if len(self.replay.fetchall()) > 0:
                messagebox.showerror("Ошибка!", "Такой товар уже существует!")

            else:
                self.new_connect.execute_sql(f"INSERT into tovar (name, price) "
                                             f"VALUES ('{self.tovar_name.get()}',"
                                             f"{self.tovar_price.get()})")

            self.new_connect.close_db()
            self.update_tables(self.table_tov)

        else:
            messagebox.showerror("Ошибка!", "Запомните все поля!")

    def update_tovar(self):
        self.new_connect = connect_db("magazin.db")

        if self.tovar_name.get() != "":
            self.check = self.new_connect.execute_sql(f"SELECT * FROM tovar WHERE name = '{self.old_name}'")

            if len(self.check.fetchall()) == 0:
                messagebox.showerror("Ошибка!", "Такого товара не существует!")

            else:
                self.replay = self.new_connect.execute_sql(f"SELECT * from tovar WHERE "
                                                           f"name = '{self.tovar_name.get()}'"
                                                           f"and price = '{self.tovar_price.get()}'")

                if len(self.replay.fetchall()) > 0:
                    messagebox.showerror("Ошибка!", "Такой товар уже существует!")

                else:
                    otvet = messagebox.askyesno("Внимание!", "Товар будет изменен. Вы уверены?")

                    if otvet:
                        self.new_connect.execute_sql(f"UPDATE tovar SET name = '{self.tovar_name.get()}', "
                                                     f"price = '{self.tovar_price.get()}' WHERE name = '{self.old_name}'")
                        self.new_connect.close_db()
                        self.update_tables(self.table_tov)

    def combobox_tovar(self):
        self.new_connect = connect_db("magazin.db")
        self.sql = self.new_connect.execute_sql(f"SELECT * from tovar "
                                                f"WHERE name = '{self.buy_tovar.get()}'")

        for row in self.sql:
            self.price=row[2]

        self.new_connect.close_db()
        self.lb_price.configure(text=f"Цена: {self.price} руб.")
        self.set_sum()

    def buy(self):
        if self.buy_tovar.get()!="" and self.sum > 0:
            print(self.price)

            # найти id товара
            self.new_connect = connect_db("magazin.db")
            self.sql = self.new_connect.execute_sql(f"SELECT * from tovar WHERE name = '{self.buy_tovar.get()}' ")
            for row in self.sql:
                self.id_tovar = row[0]
                self.new_connect.execute_sql(f"INSERT into tovar_buy (id_tovar, price, kol, sum) "
                                             f"VALUES ({self.id_tovar}, {self.price}, "
                                             f"{self.tovar_kol.get()}, {self.sum} ) ")

            self.new_connect.close_db()
            self.update_tables(self.table_buy)
        else:
            messagebox.showerror("Ошибка!", "Вы не выбрали товар или не ввели количество!")

    def frame_buy(self):
        self.table_buy = Treeview(self.frame2, columns=["tovar", "price", "kol", "sum"], show="headings")

        self.table_buy.heading("tovar", text="Товар")
        self.table_buy.heading("price", text="Цена")
        self.table_buy.heading("kol", text="Колличество")
        self.table_buy.heading("sum", text="Сумма")

        self.table_buy.column("tovar", width=150, anchor="c")
        self.table_buy.column("price", width=150, anchor="c")
        self.table_buy.column("kol", width=150, anchor="c")
        self.table_buy.column("sum", width=150, anchor="c")
        self.table_buy.place(x = 10, y = 10)

        self.update_tables(self.table_buy)

        # формирование списка товаров
        self.tovar_list = []
        self.new_connect = connect_db("magazin.db")
        self.sql = self.new_connect.execute_sql(f"SELECT * from tovar")

        for row in self.sql:
            self.tovar_list.append(row[1])
        self.new_connect.close_db()

        # надпись выпадающих списков для выбора товара
        self.lb_name = Label(self.frame2, text = "Выберите товар:", font="Arial 12", background="lightblue")
        self.lb_name.place(x = 10, y = 250)

        self.buy_tovar = Combobox(self.frame2, values=self.tovar_list, state="readonly")
        self.buy_tovar.place(x = 10, y = 300)

        self.buy_tovar.bind("<<ComboboxSelected>>", lambda  event: self.combobox_tovar())

        # создание надписи и поля для ввода количества товара
        self.tovar_kol = IntVar()
        self.lb_kol = Label(self.frame2, text = "Введите количество:", font="Arial 12", background="lightblue")
        self.buy_kol = Entry(self.frame2, textvariable=self.tovar_kol)
        self.buy_kol.place(x=200, y=300, width=100)
        self.buy_kol.bind("<KeyRelease>", lambda  event: self.set_sum())

        # создание надписи для отображения цены товара
        self.lb_price = Label(self.frame2, text="Цена 0 руб.", font="Arial 12", background="lightblue")
        self.lb_price.place(x=10, y=340)

        # создание надписи для отображения итоговой суммы
        self.lb_sum = Label(self.frame2, text="Итого: 0 руб.", font="Arial  12", background="lightblue")
        self.lb_sum.place(x=200, y=340)

        # кнопка для совершения "покупки"
        self.btn_send_buy = Button(self.frame2, text="Купить", command = self.buy)
        self.btn_send_buy.place(x=400, y=300)

        # кнопка увеличение количества товара
        self.btn_up = Button(self.frame2, text="+", command=self.kol_up)
        self.btn_up.place(x=300, y=300, width=25, height=23)

        # кнопка уменьшения количества товара
        self.btn_down = Button(self.frame2, text="-", command=self.kol_down)
        self.btn_down.place(x=325, y=300, width=25, height=23)

    def kol_up(self):
        self.tovar_kol.set(self.tovar_kol.get() + 1)
        self.set_sum()

    def kol_down(self):
        if self.tovar_kol.get() > 0:
            self.tovar_kol.set(self.tovar_kol.get() - 1)
        self.set_sum()

    def set_sum(self):
        if self.tovar_kol.get() < 0:
            messagebox.showerror("Ошибка", "Количество не может быть отрицательным!")
            self.tovar_kol.set(0)

        self.sum = self.tovar_kol.get() * self.price
        self.lb_sum.configure(text = f"Сумма: {self.sum} руб. ")


    def frame_sell(self):
        self.table_sell = Treeview(self.frame3, columns=["tovar", "price", "kol", "sum"], show="headings")
        self.table_sell.heading("tovar", text="Товар", command=lambda: self.sort_name("tovar", False, self.table_sell))
        self.table_sell.heading("price", text="Цена", command=lambda: self.sort_name("price", False, self.table_sell))
        self.table_sell.heading("kol", text="Количество", command=lambda: self.sort_name("kol", False, self.table_sell))
        self.table_sell.heading("sum", text="Сумма", command=lambda: self.sort_name("sum", False, self.table_sell))

        self.table_sell.column("tovar", width=150, anchor="c")
        self.table_sell.column("price", width=150, anchor="c")
        self.table_sell.column("kol", width=150, anchor="c")
        self.table_sell.column("sum", width=150, anchor="c")
        self.table_sell.place(x=10, y=10)

        self.update_tables(self.table_sell)

        # формирование списка товаров
        self.tovar_sell_list = []
        self.new_connect = connect_db("magazin.db")
        self.sql = self.new_connect.execute_sql(f"SELECT * from tovar")

        for row in self.sql:
            self.tovar_sell_list.append(row[1])
        self.new_connect.close_db()

        # надпись и выпадающего список для выбора товара
        self.lb_name = Label(self.frame3, text="Выберите товар:", font="Arial 12", background="lightblue")
        self.lb_name.place(x=10, y=250)
        self.sell_tovar = Combobox(self.frame3, values=self.tovar_sell_list, state="readonly")
        self.sell_tovar.place(x=10, y=300)

        self.sell_tovar.bind("<<ComboboxSelected>>", lambda event: self.combobox_tovar_sell())

        # надпись и выпадающего список для выбора наценки
        self.lb_price2 = Label(self.frame3, text="Установите наценку:", font="Arial 12", background="lightblue")
        self.lb_price2.place(x=170, y=250)
        self.price2_tovar = Combobox(self.frame3, values=["10%", "15%", "20%", "25%", "30%"], state="readonly")
        self.price2_tovar.current(0)
        self.price2_tovar.place(x=170, y=300, width=50)

        self.price2_tovar.bind("<<ComboboxSelected>>", lambda event: self.combobox_tovar_sell())

        # создание надписи и поля для ввода количества товара
        self.sell_tovar_kol = IntVar()
        self.lb_kol = Label(self.frame3, text="Введите количество:", font="Arial 12", background="lightblue")
        self.lb_kol.place(x=350, y=250)
        self.sell_kol = Entry(self.frame3, textvariable=self.sell_tovar_kol)
        self.sell_kol.place(x=350, y=300, width=100)
        self.sell_kol.bind("<<KeyRelease>>", lambda event: self.sell_sum())

        # кнопка увеличение количества товара
        self.btn_sell_up = Button(self.frame3, text="+", command=self.kol_sell_up)
        self.btn_sell_up.place(x=450, y=300, width=25, height=23)

        #кнопка уменьшения колличества товара
        self.btn_sell_down = Button(self.frame3, text="-", command=self.kol_sell_down)
        self.btn_sell_down.place(x=475, y=300, width=25, height=23)

        # создание надписи для отображения цены товара
        self.lb_sell_price = Label(self.frame3, text="Цена: 0 руб.", font="Arial 12", background="lightblue")
        self.lb_sell_price.place(x=10, y=340)

        # создание надписи для отображения итоговой суммы
        self.lb_sell_sum = Label(self.frame3, text="Итого: 0 руб.", font="Arial 12", background="lightblue")
        self.lb_sell_sum.place(x=350, y=340)

        # надпись для вывода информации о количестве товара
        self.lb_kol_info = Label(self.frame3, text="Товаров на складе: 0", font="Arial 12", background="lightblue")
        self.lb_kol_info.place(x=650, y=50)

        # кнопка для совершения "покупки"
        self.btn_send_sell = Button(self.frame3, text="Продать", command=self.sell)
        self.btn_send_sell.place(x=550, y=300)

    def combobox_tovar_sell(self):
        self.price2 = int(self.price2_tovar.get().replace('%', ''))
        self.new_connect = connect_db("magazin.db")
        self.sql = self.new_connect.execute_sql(f"SELECT * from tovar "
                                                f"WHERE name = '{self.sell_tovar.get()}'")

        for row in self.sql:
            self.new_price = row[2]+row[2]*self.price2/100
        self.new_connect.close_db()

        self.lb_sell_price.configure(text=f"Цена: {self.new_price} руб.")
        self.sell_sum()
        self.sklad()

    def set_price2(self):
        pass

    def kol_sell_up(self):
        self.sell_tovar_kol.set(self.sell_tovar_kol.get() + 1)
        self.sell_sum()

    def kol_sell_down(self):
        if self.sell_tovar_kol.get() > 0:
            self.sell_tovar_kol.set(self.sell_tovar_kol.get() - 1)
            self.sell_sum()

    def sell_sum(self):
        if self.sell_tovar_kol.get() < 0:
            messagebox.showerror("Ошибка", "Количество не может быть отрицательным!")
            self.sell_tovar_kol.set(0)
        self.itog = self.sell_tovar_kol.get() * self.new_price
        self.lb_sell_sum.configure(text=f"Сумма: {self.itog} руб.")

    def sell(self):
        if self.sell_tovar.get() != "" and self.itog > 0:
            if self.kol_tovar_sklad >= self.sell_tovar_kol.get():
                #
                self.new_connect = connect_db("magazin.db")
                self.sql = self.new_connect.execute_sql(f"SELECT * from tovar WHERE name = '{self.sell_tovar.get()}'")

                for row in self.sql:
                    self.id_tovar = row[0]
                    self.new_connect.execute_sql(f"INSERT into tovar_sell (id_tovar, price, kol, sum) "
                                                 f"VALUES ({self.id_tovar}, {self.new_price}, "
                                                 f"{self.sell_tovar_kol.get()}, {self.itog}) ")
                    self.new_connect.close_db()
                    self.update_tables(self.table_sell)
                    self.sklad()

            else:
                messagebox.showerror("Ошибка!", "На складе не хватает товара!")

        else:
            messagebox.showerror("Ошибка!", "Вы не выбрали товар или не ввели количество!")

    def sklad(self):
        self.new_connect = connect_db("magazin.db")
        self.sql = self.new_connect.execute_sql(f"SELECT * from (SELECT T.name, sum(TB.kol) kol_tov "
                                                f"from tovar_buy TB INNER JOIN tovar T "
                                                f"on TB.id_tovar = T.id GROUP by name) "
                                                f"WHERE name = '{self.sell_tovar.get()}' ")

        row = self.sql.fetchone() #

        if row is None:
            self.kol_tovar_buy = 0

        else:
            self.kol_tovar_buy = row[1]

        self.sql = self.new_connect.execute_sql(f"SELECT * from (SELECT T.name, sum(TB.kol) kol_tov "
                                                f"from tovar_sell TB INNER JOIN tovar T "
                                                f"on TB.id_tovar = T.id GROUP by name) "
                                                f"WHERE name = '{self.sell_tovar.get()}' ")

        row = self.sql.fetchone() #
        self.new_connect.close_db()
        if row is None:
            self.kol_tovar_sell = 0
        else:
            self.kol_tovar_sell = row[1]

        self.kol_tovar_sklad = self.kol_tovar_buy - self.kol_tovar_sell
        self.lb_kol_info.configure(text=f"Товаров на складе: {self.kol_tovar_sklad}")

    def frame_info(self):
        # информация о товарах
        self.tovar_group = LabelFrame(self.frame4, text="Колличество товара")
        self.tovar_group.place(x=10, y=10, width=400)

        # надпись "товаров приобретено"
        self.lb_kupleno_kol = Label(self.tovar_group, text=f"Товаров приобретено: {self.kupleno_kol} шт.", font="Arial 16")
        self.lb_kupleno_kol.grid(row=0, column=0, padx=10, pady=10)

        # надписть "товаров продано"
        self.lb_prodano_kol = Label(self.tovar_group, text=f"Товаров продано: {self.prodano_kol} шт.", font="Arial 16")
        self.lb_prodano_kol.grid(row=1, column=0, padx=10, pady=10)

        # надпись "всего товаров на складе"
        self.lb_ostatok_kol = Label(self.tovar_group, text=f"Всего товаров на складе: {self.ostatok_kol} шт.", font="Arial 16")
        self.lb_ostatok_kol.grid(row=2, column=0, padx=10, pady=10)

        #----------------------------------------------------------------------------------------------------------------------------------

        # информация о балансе
        self.balans_group = LabelFrame(self.frame4, text="Баланс")
        self.balans_group.place(x=10, y=200, width=400)

        # надпись "товаров приобретено"
        self.lb_kupleno_sum = Label(self.balans_group, text=f"Потрачено на закупку: {self.kupleno_sum} руб.", font="Arial 16")
        self.lb_kupleno_sum.grid(row=0, column=0, padx=10, pady=10)

        # надпись "товаров продано"
        self.lb_prodano_sum = Label(self.balans_group, text=f"Получено с продажи: {self.prodano_sum} руб.", font="Arial 16")
        self.lb_prodano_sum.grid(row=1, column=0, padx=10, pady=10)

        # надпись "Всего товаров на складе"
        self.lb_ostatok_sum = Label(self.balans_group, text=f"Прибыль: {self.ostatok_sum} шт.", font="Arial 16")
        self.lb_ostatok_sum.grid(row=2, column=0, padx=10, pady=10)

        # ----------------------------------------------------------------------------------------------------------------------------------

        # информация о товарах
        self.info_tovar_group = LabelFrame(self.frame4, text="Информация о товарах")
        self.info_tovar_group.place(x=420, y=10, width=500)

        # надпись "самый популярный товар"
        self.lb_pop_tovar = Label(self.info_tovar_group, text=f"Самый популярный товар: {self.popular_tovar}", font="Arial 14")
        self.lb_pop_tovar.grid(row=0, column=0, padx=10, pady=10)

        # надпис "самый не популярный товар"
        self.lb_unpop_tovar = Label(self.info_tovar_group, text=f"Самый не популярный товар: {self.UNpopular_tovar}", font="Arial 14")
        self.lb_unpop_tovar.grid(row=1, column=0, padx=10, pady=10)

        # ----------------------------------------------------------------------------------------------------------------------------------

        # кнопка для обновления данных
        self.btn_send_sell = Button(self.frame4, text="Обновить данные", command=self.update_info)
        self.btn_send_sell.place(x=420, y=250)

        # получнение текущей даты и времени
        self.date_now = datetime.datetime.now()

        # получение только даты
        self.date = self.date_now.date()

        # получение только часов и минут
        self.time = self.date_now.strftime("%H:%M:%S")

        self.lb_dt_update = Label(self.frame4, text="Время последнего обновления:" + "\n" +
                                  f"Дата: {self.date}" +
                                  f" Время {self.time}", font="Arial 14", background="lightblue")
        self.lb_dt_update.place(x=420, y=200)

        self.btn_open_calculator = Button(self.frame4, text="Калькулятор", command=self.open_calculator)
        self.btn_open_calculator.place(x=420, y=150)

        self.info_kol_tovar()
        self.info_balance()
        self.info_tovar()


    def info_kol_tovar(self):
        self.new_connect = connect_db("magazin.db")

        # товаров куплено
        self.sql = self.new_connect.execute_sql(f"SELECT sum(kol) from tovar_buy")
        row = self.sql.fetchone() # получаем только одну строку результата
        if row is None:
            self.prodano_kol = 0
        else:
            self.prodano_kol = row[0]
        self.lb_prodano_kol.configure(text=f"Товаров продано: {self.prodano_kol} шт.")

        # остаток товаров
        self.ostatok_kol = self.kupleno_kol - self.prodano_kol
        self.lb_ostatok_kol.configure(text=f"Всего товаров на складе: {self.ostatok_kol} шт.")

        self.new_connect.close_db()

    def info_balance(self):
        self.new_connect = connect_db("magazin.db")

        # товаров куплено
        self.sql = self.new_connect.execute_sql(f"SELECT sum(sum) from tovar_buy")
        row = self.sql.fetchone() # получаем только одну строку результата
        if row is None:
            self.prodano_sum = 0
        else:
            self.prodano_sum = row[0]
        self.lb_prodano_sum.configure(text=f"Получено с продажи: {self.prodano_sum} руб.")

        # остаток товаров
        self.ostatok_sum = self.prodano_sum - self.kupleno_sum
        self.lb_ostatok_sum.configure(text=f"Прибыль: {self.ostatok_sum} руб.")

        self.new_connect.close_db()

    def info_tovar(self):
        self.new_connect = connect_db("magazin.db")

        self.sql = self.new_connect.execute_sql(f"SELECT T.name, max(TS.SK) from tovar T inner join "
                                                f"(SELECT id_tovar, sum(kol) SK from tovar_sell group by id_tovar) "
                                                f"TS on T.id = TS.id_tovar")

        row = self.sql.fetchone() # получаем только одну строку результата
        if row is None:
            self.UNpopular_tovar = 0
        else:
            self.UNpopular_tovar = row[0]
        self.lb_unpop_tovar.configure(text=f"Самый не популярный товар: {self.UNpopular_tovar}")

        self.new_connect.close_db()

    def update_info(self):
        # получение текущей даты и времени
        self.date_now = datetime.datetime.now()

        # получение только даты
        self.date = self.date_now.date()

        # получение только часов и минут
        self.time = self.date_now.strftime("%H:%M:%S")
        self.lb_dt_update.configure(text="Время последненго обновления: " +
                                         "\n" + f"Дата: {self.date}" +
                                         f"Время: {self.time}")
        self.info_kol_tovar()
        self.info_balance()
        self.info_tovar()

    def open_calculator(self):
        subprocess.Popen("calc", shell=True)

new_win = my_window()
