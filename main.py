from tkinter import *
import pathmagic

with pathmagic.Context():
    from Work.Scripts.front import Front


def getText():
    log1 = text.get(1.0, END)
    log2 = text2.get(1.0, END)
    if Front(log1, log2):
        rt.quit()


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
