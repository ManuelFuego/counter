import tkinter as tk
from tkinter import  ttk
import sqlite3
from tkinter import messagebox as mb
import pandas as pd
import datetime
import matplotlib.pyplot as plt

class Main(tk.Frame):
    def __init__(self,root):
        super().__init__(root)
        #root.iconbitmap('bin.ico')
        self.init_main()
        self.db = db
        self.show_data()

    def init_main(self):
        ''' окно приложения '''

        toolbar = tk.Frame(bg='grey', bd=2)    # bg цвет фона , bd размер границы
        toolbar.pack(side=tk.TOP, fill=tk.X)     #   side = закрепить тулбар  . x растянуть по окну

        self.add_img = tk.PhotoImage(file='imgs/product.png')
        btn_open_dialog = tk.Button(toolbar,text='Добавить позицию', command = self.open_dialog,fg='black', bg='white', bd=0,
                                    compound = tk.TOP, image= self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file ='imgs/update.png')
        btn_edit_dialog = tk.Button(toolbar, text='Правка', command =self.open_update_dialog ,fg='black', bg='white', bd=0,
                                    compound = tk.TOP, image= self.update_img)
        btn_edit_dialog.pack(side = tk.LEFT)

        self.sell_img = tk.PhotoImage(file ='imgs/sell.png')
        btn_sell = tk.Button(toolbar, text='Продать', command =self.sell_dialog,fg='black', bg='white', bd=0,
                                    compound = tk.TOP, image= self.sell_img)
        btn_sell.pack(side = tk.LEFT)

        self.del_img = tk.PhotoImage(file='imgs/delete.png')
        btn_delete = tk.Button(toolbar, text = 'Удалить', command=self.delete_data,fg='black', bg='white', bd=0,
                                    compound = tk.TOP, image= self.del_img)
        btn_delete.pack(side = tk.LEFT)

        self.search_img = tk.PhotoImage(file='imgs/search.png')
        btn_search = tk.Button(toolbar, text='Поиск', command = self.search_dialog,fg='black', bg='white',bd=0,
                                    compound = tk.TOP, image= self.search_img)
        btn_search.pack(side = tk.LEFT)

        self.reload_img = tk.PhotoImage(file='imgs/reload.png')
        btn_reload = tk.Button(toolbar, text='Обновить', command = self.show_data,fg='black', bg='white', bd=0,
                                    compound = tk.TOP, image= self.reload_img)
        btn_reload.pack(side = tk.LEFT)

        self.doc_img = tk.PhotoImage(file='imgs/doc.png')
        doc_img = tk.Button(toolbar, text='Excel', command=self.make_doc, fg='black', bg='white', bd=0,
                              compound=tk.TOP, image=self.doc_img)
        doc_img.pack(side=tk.LEFT)

        self.analize_img = tk.PhotoImage(file='imgs/analytic.png')
        btn_analytic = tk.Button(toolbar, text='Графики', command=self.open_analytic, fg='black', bg='white', bd=0,
                               compound=tk.TOP, image=self.analize_img)
        btn_analytic.pack(side=tk.LEFT)

        self.sort_img = tk.PhotoImage(file='imgs/sort.png')
        btn_sort = tk.Button(toolbar, text='A-Я', command=self.sort_data, fg='black', bg='white', bd=0,
                                 compound=tk.TOP, image=self.sort_img)
        btn_sort.pack(side=tk.LEFT)


        self.sort_balance_img  = tk.PhotoImage(file='imgs/sort_by_balance.png')
        btn_sort = tk.Button(toolbar, text='Остаток', command=self.sort_by_balance, fg='black', bg='white', bd=0,
                                 compound=tk.TOP, image=self.sort_balance_img)
        btn_sort.pack(side=tk.LEFT)

        self.sort_top_img = tk.PhotoImage(file='imgs/sort_by_top.png')
        btn_sort = tk.Button(toolbar, text='Выручка', command=self.sort_by_profit, fg='black', bg='white', bd=0,
                             compound=tk.TOP, image=self.sort_top_img)
        btn_sort.pack(side=tk.LEFT)


        self.tree = ttk.Treeview(self, columns=('id','description','buy_price',
                                                'quantity','cost_of_product',
                                                'count_for_sell','balance',
                                                'sell_price','profit'), height=15, show='headings')  # информация в иерархической формк
        self.tree.column('id', width=40,anchor=tk.CENTER)
        self.tree.column('description', width=360,anchor=tk.CENTER)
        self.tree.column('buy_price',width=150,anchor=tk.CENTER)
        self.tree.column('quantity', width=150,anchor=tk.CENTER)
        self.tree.column('cost_of_product',width=150,anchor=tk.CENTER)
        self.tree.column('count_for_sell', width=150,anchor=tk.CENTER)
        self.tree.column('balance', width=150,anchor=tk.CENTER)
        self.tree.column('sell_price', width=150,anchor=tk.CENTER)
        self.tree.column('profit', width=150,anchor=tk.CENTER)

        self.tree.heading('id',text='№')
        self.tree.heading('description',text='наименование')
        self.tree.heading('buy_price',text='закупочная цена')
        self.tree.heading('quantity',text='количество')
        self.tree.heading('cost_of_product',text='стоимость закупки')
        self.tree.heading('count_for_sell',text='продано')
        self.tree.heading('balance',text='остаток')
        self.tree.heading('sell_price',text='средняя цена')
        self.tree.heading('profit',text='выручка')
        self.tree.pack(side=tk.LEFT)

        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)


    def write_data(self,description,buy_price,quantity):
        ''' запись данных в таблицу '''
        try:
            self.db.create_data(description.lower(),buy_price,quantity)
        except Exception:
            mb.showinfo('Ошибка', 'Данное наименование уже существует')
        self.show_data()

    def update_data(self,description,buy_price,quantity):
        ''' отредактировать позицию'''
        try:
            self.db.c.execute(''' UPDATE data SET description=?, buy_price=?, quantity=? WHERE id=?''',
                              (description.lower(),buy_price, quantity, self.tree.set(self.tree.selection()[0], '#1')))
            self.db.c.execute('''INSERT INTO data(description,buy_price,quantity) SELECT ?, ?, ? WHERE (SELECT Changes()=0)''',
                          (description.lower(),buy_price,quantity,self.tree.set(self.tree.selection()[0], '#1')))
        except:
            #mb.showinfo('ИНОФРМАЦИЯ','Данное наименование будет заменено')
            pass
        self.db.conn.commit()
        self.show_data()

    def delete_data(self):
        ''' удалить позицию из бд'''
        try:
            for selection_item in self.tree.selection():
                self.db.c.execute('''DELETE FROM data WHERE id=?''',(self.tree.set(selection_item, '#1'),))
        except Exception:
            pass
        self.db.conn.commit()
        self.show_data()

    def sell_product(self,description,count_for_sell,sell_price):
        ''' продать позицию'''
        try:
            self.db.c.execute(''' update data set description=?, count_for_sell=count_for_sell+?, sell_price=? ,profit=(?*?)+profit where id=?''',
                        (description.lower(), count_for_sell, sell_price, count_for_sell,sell_price ,self.tree.set(self.tree.selection()[0],'#1')))
        except Exception:
            mb.showinfo('Иноформация','Что-то пошло не так')
        self.db.conn.commit()
        self.show_data()

    def search_data(self,description):
        ''' поиск значения '''
        description = ('%' + description.lower() + '%',)
        self.db.c.execute(''' SELECT * FROM data WHERE description LIKE ?''', description)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('','end',values=row) for row in self.db.c.fetchall()]

    def calculate_data(self):
        ''' нереализовано подсчет в модуле пандас'''
        df = pd.read_sql("select * from data", self.db.conn)
        fra = pd.DataFrame(df)
        print(fra)

    def show_data(self):
        ''' показать таблицу'''
        #self.db.c.execute(''' SELECT * FROM data''')
        self.db.c.execute('''SELECT id,description,buy_price,
                                    quantity,cost_of_product,count_for_sell,
                                    balance,sell_price,profit  FROM data''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('','end',values=row) for row in self.db.c.fetchall()]

    def make_doc(self):
        ''' создание excel'''
        file = pd.read_sql('select * from data',self.db.conn)
        out_doc = file.to_excel(f'file{datetime.date.today()}.xlsx')
        return out_doc

    def sort_data(self):
        #mb.showinfo(message='in process')
        self.db.c.execute(''' select * from data order by description''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('','end',values=row) for row in self.db.c.fetchall()]

    def sort_by_balance(self):
        self.db.c.execute(''' select * from data order by balance''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def sort_by_profit(self):
        self.db.c.execute(''' select * from data order by profit DESC''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]


    def open_dialog(self):
        '''вызов дочернего окна '''
        Child()
    def open_update_dialog(self):
        ''' окно редактирования'''
        Update()
    def search_dialog(self):
        ''' окно поиска'''
        Search()
    def sell_dialog(self):
        '''  продажа '''
        Sell()
    def open_analytic(self):
        '''окно графиков'''
        Analytic()

class Child(tk.Toplevel):  # топ левел окно верхнего уровня класс child наследован от Toplevel
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        ''' окно редактирования'''
        self.title('внести данные ')
        self.geometry('400x220+400+300')
        self.resizable(False,False)
        pos_lab_x = 50
        label_description = tk.Label(self, text='Наименование:')
        label_description.place(x=pos_lab_x, y=50)
        label_buy_price = tk.Label(self,text='Цена закупки:')
        label_buy_price.place(x=pos_lab_x, y=80)
        label_quantity = tk.Label(self,text='Количество:')
        label_quantity.place(x=pos_lab_x, y=110)

        pos_entr_x = 200
        self.entry_description = ttk.Entry(self)
        self.entry_description.place(x=pos_entr_x, y=50)
        self.entry_buy_price = ttk.Entry(self)
        self.entry_buy_price.place(x=pos_entr_x,y =80)
        self.entry_quantity= ttk.Entry(self)
        self.entry_quantity.place(x=pos_entr_x,y =110)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=200, y=170)
        self.btn_ok.bind('<Button-1>',lambda event : self.view.write_data(self.entry_description.get(),
                                                                          self.entry_buy_price.get(),
                                                                          self.entry_quantity.get()))
        self.grab_set()
        self.focus_set()

class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.db = db
        self.view = app
        self.default_values()

    def init_edit(self):
        ''' окно редактирования'''
        self.title('Редактирование')
        btn_edit = ttk.Button(self, text='ok')
        btn_edit.place(x=200, y=170)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_data(self.entry_description.get(),
                                                                        self.entry_buy_price.get(),
                                                                        self.entry_quantity.get()))
        self.btn_ok.destroy()

    def default_values(self):
        ''' показ исходных значений'''
        self.db.c.execute('''SELECT * FROM data WHERE id=?''',(self.view.tree.set(self.view.tree.selection()[0],'#1'),))
        row = self.db.c.fetchone()
        self.entry_description.insert(0,row[1])
        self.entry_buy_price.insert(0,row[2])
        self.entry_quantity.insert(0,row[3])

class Analytic(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.db = db
        self.make_analytic()

    def make_analytic(self):
        self.title('Графики')
        self.geometry('400x200+400+300')
        self.resizable(False, False)
        btn_sell_to_by = ttk.Button(self, text='Цена продажи к покупке',width=40,command=self.sell_to_by_graph)
        btn_sell_to_by.place(x=40, y=20)
        btn_quantity_to_balance = ttk.Button(self, text='Купленный товар к проданному',width=40 ,command=self.quantity_to_balance_graph)
        btn_quantity_to_balance.place(x=40, y=50)
        #btn_favorite_goods = ttk.Button(self,text = 'Популярные товары')
        #btn_favorite_goods.place(x=40,y=80)

    def sell_to_by_graph(self):
        df = pd.read_sql("select * from data", self.db.conn)
        fra = pd.DataFrame(df)
        fra.plot(x='description', y=['buy_price', 'sell_price'],kind='bar',title='Разница между покупкой и продажей')
        plt.show()

    def quantity_to_balance_graph(self):
        df = pd.read_sql("select * from data", self.db.conn)
        fra = pd.DataFrame(df)
        fra.plot(x='description', y=['quantity', 'balance'],kind='bar',title='Разница между купленным товаром  и балансом')
        plt.show()



class Sell(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_sell()
        self.db = db
        self.view = app
        self.default_values()

    def init_sell(self):
        ''' окно продажи товара '''
        self.title('Продать')
        self.geometry('400x300+400+300')
        self.resizable(False, False)
        pos_lab_x = 50
        label_description = tk.Label(self, text='Наименование:')
        label_description.place(x=pos_lab_x, y=50)
        label_quantity = tk.Label(self, text='Количество:')
        label_quantity.place(x=pos_lab_x, y=80)
        label_sell_price = tk.Label(self, text='Цена продажи:')
        label_sell_price.place(x=pos_lab_x, y=110)
        pos_entr_x = 200
        self.entry_description = ttk.Entry(self)
        self.entry_description.place(x=pos_entr_x, y=50)
        self.entry_quantity = ttk.Entry(self)
        self.entry_quantity.place(x=pos_entr_x, y=80)
        self.entry_sell_price = ttk.Entry(self)
        self.entry_sell_price.place(x=pos_entr_x, y=110)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        self.btn_ok = ttk.Button(self, text='Продать')
        self.btn_ok.place(x=200, y=170)
        self.btn_ok.bind('<Button-1> ', lambda event: self.view.sell_product(self.entry_description.get(),
                                                                             self.entry_quantity.get(),
                                                                             self.entry_sell_price.get()))

    def default_values(self):
        ''' значения по умолчанию'''
        self.db.c.execute('''SELECT * FROM data WHERE id=?''',(self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.c.fetchone()
        self.entry_description.insert(0,row[1])

class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        ''' окно поиска '''
        self.title('Поиск')
        self.geometry('300x100+400+300')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_data(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')

class DB:
    def __init__(self):
        self.conn =sqlite3.connect('data.db')   # создание дб
        self.c = self.conn.cursor()             #    создание курсора (взаимодейсвие с дб)
        self.c.execute('''CREATE TABLE IF NOT EXISTS data (id integer primary key,
                                                           description text,
                                                           buy_price real,
                                                           quantity real check(quantity >= 0),
                                                           cost_of_product real as (buy_price * quantity),
                                                           count_for_sell real DEFAULT 0 CHECK(count_for_sell <= quantity),
                                                           balance real as (quantity - count_for_sell),
                                                           sell_price real ,
                                                           profit real  default 0 ,
                                                           CONSTRAINT un_row UNIQUE (description))''')

        self.conn.commit()     #сохранить данные

    def create_data(self, description, buy_price, quantity):
        self.c.execute(''' INSERT INTO data (description,buy_price,quantity) values(?, ?, ?)''',
                                            (description.lower(), buy_price, quantity))

        self.conn.commit()

if __name__ =='__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Бухсчет 1.04')
    root.geometry('1470x410+300+200')
    root.resizable(False, False)
    root.mainloop()
