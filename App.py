from tkinter import *
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
import os

def saveCommand():
    return

def saveAsCommand():
    return

def openCommand():
    return

def AddFileCommand():
    return

def FileClick(event):
    for child in frame.winfo_children():
        if str(type(child)) == "<class 'tkinter.Button'>":
            child.destroy()
            break

def AddFileCommand():
    file = filedialog.askopenfile(mode='r', filetypes=[('Pictures', '*.png'), ('Pictures', '*.jpeg'), ('Pictures', '*.jpg'), ('Text', '*.txt')])
    if file:
        num = 0
        for child in frame.winfo_children():
            if str(type(child)) == "<class 'tkinter.Button'>":
                num += 1
        #root.columnconfigure(0, weight=1)
        filepath = os.path.abspath(file.name)
        button = Button(frame, text = "- " + str(filepath) + " [Click to remove]", bg = 'grey', fg = 'black')
        button.bind("<Button-1>", FileClick)
        #button.place(x=0, y=0)
        button.grid(row = num, column = 0, sticky = 'NW', padx = 5, pady = 5)
        #button.pack()
        #button.pack(pady = 50, padx = 50)

app = Tk()
menu = Menu(app)

m1 = Menu(menu, tearoff = 0)
m1.add_command(label = "Save",command = saveCommand)
m1.add_command(label = "Save As",command = saveAsCommand)
m1.add_separator()
m1.add_command(label = "Open",command = openCommand)
menu.add_cascade(label = "File",menu = m1)

m2 = Menu(menu)
m2.add_command(label = "Add File", command = AddFileCommand)
menu.add_cascade(label = "Edit", menu = m2)

app.config(menu = menu)
app.title("EventGroupingData")
app.geometry("1280x720")

frame = Frame(app, width = 1280, height = 200, bg='white', highlightbackground = 'black', highlightthickness = 2)
frame.pack_propagate(False)
frame.pack(fill = 'both', side = 'bottom')

if __name__ == '__main__':
    app.mainloop()
