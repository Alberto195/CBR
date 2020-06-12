from tkinter import *
import pathmagic
from tkinter import messagebox
import mysql.connector

with pathmagic.Context():
    from Work.Scripts.front import Front


def getText():
    log1 = text.get(1.0, END)
    log2 = text2.get(1.0, END)
    try:
        '''Подключаем mysql'''
        mydb = mysql.connector.connect(
            auth_plugin='mysql_native_password',
            user=log1[:-1],
            password=log2[:-1],
        )
        '''Создаём бд'''
        mycursor = mydb.cursor()
        all_dbfs = "all_in_one"
        database = "CREATE DATABASE IF NOT EXISTS " + all_dbfs
        mycursor.execute(database)

        if Front(log1, log2):
            rt.quit()

    except mysql.connector.errors.ProgrammingError:
        messagebox.showinfo("Нотификация", "Неправильные данные")


rt = Tk()
rt.geometry("400x400")
rt.resizable(False, False)

lab = Label(text="Введите user и password от MySQL")
lab.place(x=120, y=160)
text = Text(width=10, height=1)
text.place(x=120, y=180)
text2 = Text(width=10, height=1)
text2.place(x=120, y=200)
bttnusr = Button(rt, text="Войти в систему", width=15, height=1, command=lambda: getText())
bttnusr.place(x=120, y=230)
rt.mainloop()
