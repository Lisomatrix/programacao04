import os
import re
import csv
import tkinter
from glob import iglob
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showinfo

# 96804726
directory = "/Users/lisomati/Downloads/create-composition-animation/Work with Compositions"
output = "/Users/lisomati/Downloads/waldo.csv"


def create_csv(folders, output):
    f = open(output, 'w')
    writer = csv.writer(f)

    for pair in folders:
        writer.writerow(pair)

    f.close()


def scan_folder(folder_path, folders):
    file_list = [f for f in iglob(folder_path + "/**/*", recursive=True)]

    folder_image = tkinter.PhotoImage(file="folder.png")
    file_image = tkinter.PhotoImage(file="file.png")

    for f in file_list:

        is_folder = os.path.isdir(f)

        parts = f.split("/")
        name = parts[len(parts) - 1]

        extension = ""

        if not is_folder:
            name_parts = name.split(".")
            extension = name_parts[len(name_parts) - 1]

        img = file_image

        if is_folder:
            img = folder_image

        folders.append({
            "name": name,
            "extension": extension,
            "path": f,
            "folder": os.path.dirname(f),
            "isFolder": is_folder,
            "image": img
        })

        # folders.append([name, "." + extension, f, folder_path])


def filter_files(folders, expression):
    if expression == "":
        return folders

    filtered_folders = []

    for pair in folders:
        if re.match(expression, pair["name"]):
            filtered_folders.append(pair)

    return filtered_folders


def insert_data(root_folder, folders):
    for pair in folders:

        values = [pair["name"], pair["extension"], pair["path"]]

        if not pair["isFolder"] and pair["folder"] != root_folder:
            tree.insert(pair["folder"], tkinter.END, image=pair["image"], values=values, iid=pair["path"], open=False)
        else:
            tree.insert('', tkinter.END, values=values, image=pair["image"], iid=pair["path"], open=False)


def item_selected(event):
    for selected_item in tree.selection():
        item = tree.item(selected_item)
        record = item['values']
        # show a message
        # showinfo(title='Info', message="waldo")


def initial_search():
    scan_folder(root_folder, folders)


if __name__ == '__main__':
    root = Tk()

    folders = []

    menubar = Menu(root)
    root.config(menu=menubar)

    s = ttk.Style()
    s.configure('Treeview', rowheight=40)

    columns = ["name", "extension", "path"]

    root.title("Explorador de ficheiros")
    root.geometry('920x600')

    frm = ttk.Frame(root)
    frm.pack(fill="both", expand=True)

    frm.rowconfigure(1, weight=1)
    frm.columnconfigure(0, weight=0)
    frm.columnconfigure(1, weight=0)
    frm.columnconfigure(2, weight=1)

    ttk.Label(frm, text="Pesquisar:").grid(sticky=W, row=0, column=0)

    search_value = tkinter.StringVar()

    search_entry = ttk.Entry(frm, textvariable=search_value)
    search_entry.grid(sticky=W, row=0, column=1)

    tree = ttk.Treeview(frm, columns=columns, show="tree headings")

    def search_pressed():
        filtered_values = filter_files(folders, search_value.get())
        tree.delete(*tree.get_children())
        insert_data(root_folder, filtered_values)

    def cancel_pressed():
        search_value.set("")
        tree.delete(*tree.get_children())
        insert_data(root_folder, folders)

    ttk.Button(frm, text="Pesquisar", command=search_pressed).grid(sticky=W, row=0, column=2)
    ttk.Button(frm, text="Limpar Pesquisa", command=cancel_pressed).grid(sticky=E, row=0, column=3)

    tree.heading("name", text="Nome")
    tree.heading("extension", text="Extensão")
    tree.heading("path", text="Path")

    tree.column("extension", width=5)

    tree.grid(row=1, column=0, columnspan=4, sticky='nsew')

    scrollbar = ttk.Scrollbar(frm, orient=tkinter.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=1, column=4, sticky='ns')

    tree.bind('<<TreeviewSelect>>', item_selected)

    #root_folder = askdirectory(title='Select Folder')
    root_folder = directory
    initial_search()

    #create_csv(filtered_folders, output)

    insert_data(root_folder, folders)


    def on_choose_path():
        folders = []
        root_folder = askdirectory(title='Select Folder')
        scan_folder(root_folder, folders)
        tree.delete(*tree.get_children())
        insert_data(root_folder, folders)


    fileMenu = Menu(menubar)
    fileMenu.add_command(label="Sair", command=root.quit)
    fileMenu.add_command(label="Escolher pasta", command=on_choose_path)
    menubar.add_cascade(label="Ficheiro", menu=fileMenu)

    root.mainloop()
