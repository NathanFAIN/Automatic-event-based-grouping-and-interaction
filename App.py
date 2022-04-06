from tkinter import *
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile
import os
from MediaData import DataType, MediaData
from GenerateKeywords import GenerateKeywordsFromImage, GenerateKeywordsFromText, UploadPicture

data = []

def saveCommand():
    return

def saveAsCommand():
    return

def openCommand():
    return

def AddFileCommand():
    file = filedialog.askopenfile(title='Choose a file', mode='r', filetypes=[('Pictures', '*.png'), ('Pictures', '*.jpeg'), ('Pictures', '*.jpg'), ('Pictures', '*.webp'), ('Text', '*.txt')])
    if file:
        global data
        filepath = str(os.path.abspath(file.name))
        listbox.insert(END, filepath)
        newData = MediaData(filepath)
        print(newData.getPath())
        print(newData.getKeyWords())
        data.append(newData)

def removeData(path: str):
    global data
    data = list(filter(lambda x: x.getPath() != path, data))

def onSelectListbox(event):
    w = event.widget
    if len(w.curselection()) != 0:
        index = int(w.curselection()[0])
        top = Toplevel(app)
        top.geometry("400x100")
        top.title("Remove File")
        path = w.get(index)
        Label(top, text= "Do you want to remove the following file?").pack(side = TOP, fill = BOTH)
        Label(top, text= path).pack(side = TOP, fill = BOTH)
        Button(top, text="No", command=top.destroy).pack()
        Button(top, text="Yes", command=lambda : (
            w.delete(index), 
            top.destroy(),
            removeData(path))).pack()

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

