import tkinter
import tkinter.messagebox
import pickle
from tkinter import *
from xlwt import Workbook

root = tkinter.Tk()
root.title("To-DoList Nogueira")

def add_task():
    task = entry_task.get()
    date = entry_date.get()

    try:
        if task != "":
            listbox_tasks.insert(tkinter.END, task + "-" + date)
            entry_task.delete(0, tkinter.END)
            entry_date.delete(0, tkinter.END)
        else:
            tkinter.messagebox.showwarning(title="Aviso!", message="Introduz uma tarefa.")
    except ValueError: 
        tkinter.messagebox.showwarning(title="Aviso!", message="Introduz uma data válida. (yyyy-MM-dd)")

def delete_task():
    try:
        task_index = listbox_tasks.curselection()[0]
        listbox_tasks.delete(task_index)
    except:
        tkinter.messagebox.showwarning(title="Aviso!", message="Seleciona uma tarefa.")

def load_tasks():
    try:
        tasks = pickle.load(open("tasks.dat", "rb"))
        listbox_tasks.delete(0, tkinter.END)
        for task in tasks:
            listbox_tasks.insert(tkinter.END, task)
    except:
        tkinter.messagebox.showwarning(title="Aviso!", message="Nao foi possivel encontrar tarefas")

def save_tasks():
    tasks = listbox_tasks.get(0, listbox_tasks.size())
    pickle.dump(tasks, open("tasks.dat", "wb"))

def export_excel():
    wb = Workbook()

    i = 0

    tasks = listbox_tasks.get(0, listbox_tasks.size())

    tarefas_sheet = wb.add_sheet('TarefasSheet')

    for task in tasks:
            tarefas_sheet.write(i, 0, task)
            i = i + 1

    wb.save('Tarefas_Excel.xls')

    tkinter.messagebox.showwarning(title="Aviso!", message="Exportação concluída com sucesso")


# Create GUI

if __name__ == '__main__':

    frame_tasks = tkinter.Frame(root)
    frame_tasks.pack()

    listbox_tasks = tkinter.Listbox(frame_tasks, height=10, width=50)
    listbox_tasks.pack(side=tkinter.LEFT)

    scrollbar_tasks = tkinter.Scrollbar(frame_tasks)
    scrollbar_tasks.pack(side=tkinter.RIGHT, fill=tkinter.Y)

    listbox_tasks.config(yscrollcommand=scrollbar_tasks.set)
    scrollbar_tasks.config(command=listbox_tasks.yview)

    label = Label(text = "Tarefa")  
    label.pack()

    entry_task = tkinter.Entry(root, width=50)
    entry_task.pack()

    label = Label(text = "Data (yyyy-MM-dd)")  
    label.pack()

    entry_date = tkinter.Entry(root, width=50)
    entry_date.pack()

    button_add_task = tkinter.Button(root, text="Adicionar tarefa", width=48, command=add_task)
    button_add_task.pack()

    button_delete_task = tkinter.Button(root, text="Apagar tarefa", width=48, command=delete_task)
    button_delete_task.pack()

    button_load_tasks = tkinter.Button(root, text="Carregar tarefas", width=48, command=load_tasks)
    button_load_tasks.pack()

    button_save_tasks = tkinter.Button(root, text="Guardar tarefas", width=48, command=save_tasks)
    button_save_tasks.pack()

    button_save_tasks = tkinter.Button(root, text="Exportar para Excel", width=48, command=export_excel)
    button_save_tasks.pack()

    root.mainloop()
