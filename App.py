from tkinter import *
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
import os
from MediaData import DataType
from GenerateKeywords import GenerateKeywordsFromImage, GenerateKeywordsFromText, UploadPicture

def saveCommand():
    return

def saveAsCommand():
    return

def openCommand():
    return

def AddFileCommand():
    file = filedialog.askopenfile(title='Choose a file', mode='r', filetypes=[('Pictures', '*.png'), ('Pictures', '*.jpeg'), ('Pictures', '*.jpg'), ('Text', '*.txt')])
    if file:
        filepath = os.path.abspath(file.name)
        listbox.insert(END, str(filepath))

def onSelectListbox(event):
    w = event.widget
    if len(w.curselection()) != 0:
        index = int(w.curselection()[0])
        top = Toplevel(app)
        top.geometry("400x100")
        top.title("Remove File")
        Label(top, text= "Do you want to remove the following file?").pack(side = TOP, fill = BOTH)
        Label(top, text= w.get(index)).pack(side = TOP, fill = BOTH)
        Button(top, text="No", command=top.destroy).pack()
        Button(top, text="Yes", command=lambda : (
            w.delete(index), 
            top.destroy())).pack()

app = Tk()
app.title("EventGroupingData")
app.geometry("1280x720")

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

listbox = Listbox(app)
listbox.pack(side = BOTTOM, fill = BOTH)
scrollbar = Scrollbar(app)
scrollbar.pack(side = RIGHT, fill = BOTH)
listbox.config(yscrollcommand = scrollbar.set)
scrollbar.config(command = listbox.yview)
listbox.bind('<<ListboxSelect>>', onSelectListbox)

if __name__ == '__main__':
    app.mainloop()

