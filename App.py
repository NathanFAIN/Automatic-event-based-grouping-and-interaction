from tkinter import *
from tkinter import ttk, filedialog
from tkinter.filedialog import askopenfile, asksaveasfile
from tkcalendar import Calendar
import os
from MediaData import DataType, MediaData
from MediaEvent import MediaEvent
from GenerateKeywords import GenerateKeywordsFromImage, GenerateKeywordsFromText, UploadPicture
from ttkwidgets import TimeLine
import yaml
from PIL import Image, ImageTk

data = []
timeline = None
path = None
groupedDatas = []

def is_float(element) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False

def displayImg(ws, img):
    image = Image.open(img)
    photo = ImageTk.PhotoImage(image.resize((100, 100)))
    label = Label(ws, image=photo)
    label.image = photo
    label.pack()

def displayTxt(ws, txt):
    f = open(txt, "r")
    content = f.read()
    label = Label(ws, text=content, width=60, height=15)
    label.pack()

def displayGroupedData(groupedData):
    n = len(groupedData.getMediaDatas()) + 1
    top = Toplevel(app)
    top.geometry("500x500")
    top.title("displayGroupedData")
    canvas=Canvas(
        top,
        bg='#4A7A8C',
        width=500,
        height=400,
        scrollregion=(0,0,0, n * 100)
    )
    canvas.pack(side=LEFT,expand=True)
    for d in groupedData.getMediaDatas():
        if d.getType() == DataType.PICTURE:
            displayImg(canvas, d.getPath())
        if d.getType() == DataType.TEXT:
            displayTxt(canvas, d.getPath())
    sb_ver = Scrollbar(
        top,
        orient=VERTICAL
    )

    sb_ver.pack(side=RIGHT, fill=Y)

    canvas.config(yscrollcommand=sb_ver.set)
    sb_ver.config(command=canvas.yview)

def removeDataInfo(w, index):
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

def displayDataInfo(dataToDisplay):
    def AddFileInfo():
        global data
        newData = MediaData(filepath)
        if cal.selection_get() is not None:
            print(cal.selection_get())
            newData.setDate(cal.selection_get())
        if is_float(long.get("1.0","end-1c")) and is_float(lat.get("1.0","end-1c")):
            print(long.get("1.0","end-1c"))
            print(lat.get("1.0","end-1c"))
            newData.setLocation(float(long.get("1.0","end-1c")), float(lat.get("1.0","end-1c")))
        listbox.insert(END, filepath)
        print(newData.getPath())
        print(newData.getKeyWords())
        data.append(newData)
        top.destroy()
    top = Toplevel(app)
    top.geometry("300x360")
    top.title("Add Info")
    Label(top, text = dataToDisplay.getPath(), font=("Arial", 20)).pack()
    Label(top, text = "Date", font=("Arial", 20)).pack()
    cal = None
    if dataToDisplay.getDate() is not None:
        cal = Calendar(top, selectmode = 'day', year = dataToDisplay.getDate().year, month = dataToDisplay.getDate().month, day = dataToDisplay.getDate().day)
    else:
        cal = Calendar(top, selectmode = 'day', year = 2022)
    cal.pack()
    Label(top, text = "Location", font=("Arial", 20)).pack()
    Label(top, text = "Longitude : ").pack()
    long = Text(top, height = 1, width = 5)
    if dataToDisplay.getLocation() is not None:
        long.insert(0, str(dataToDisplay.getLocation()[0]))
    long.pack()
    Label(top, text = "Latitude : ").pack()
    lat = Text(top, height = 1, width = 5)
    if dataToDisplay.getLocation() is not None:
        lat.insert(0, str(dataToDisplay.getLocation()[1]))
    lat.pack()
    Button(top, text = "Done", command=AddFileInfo).pack()

def saveCommand():
    global path
    if path is not None:
        global data
        dataToSave = []
        for d in data:
            dataToSave.append([d.getPath(), d.getLocation(), d.getDate()])
        with open(path, 'w') as file:
            yaml.dump(dataToSave, file)
    else:
        saveAsCommand()

def saveAsCommand():
    file = filedialog.asksaveasfile(title='Choose a file', mode='w', filetypes=[('yaml', '*.yml')])
    if file:
        global path
        path = str(os.path.abspath(file.name))
        saveCommand()

def openCommand():
    file = filedialog.askopenfile(title='Choose a file', mode='r', filetypes=[('yaml', '*.yml')])
    if file:
        global data
        filepath = str(os.path.abspath(file.name))
        data = []
        with open(filepath, 'r') as file:
            content = yaml.safe_load_all(file)
            for datas in content:
                for d in datas:
                    newData = MediaData(d[0])
                    if d[1] is not None:
                        newData.setLocation(d[1][0], d[1][1])
                    newData.setDate(d[2])
                    data.append(newData)
                    listbox.insert(END, d[0])

def GroupDataCommand():
    global groupedDatas
    groupedDatas = []
    for d in data:
        isadded = False
        for g in groupedDatas:
            if g.isSame(d):
                g.addMediaData(d)
                isadded = True
                break
        if isadded == False:
            g = MediaEvent()
            g.addMediaData(d)
            groupedDatas.append(g)
    if len(groupedDatas) != 0:
        global timeline
        if timeline != None:
            timeline.destroy()
        timeline = TimeLine(
            app,
            categories={str(key): {"text": "Event n°{}".format(key)} for key in range(1, len(groupedDatas) + 1)},
            width=800, extend=True, start=0.0, finish=100.0
        )
        index = 1
        for gd in groupedDatas:
            ##################
            #Debug:
            #displayGroupedData(gd)
            ##################
            #if gd.getDate() is None:
            timeline.tag_configure(str(index), left_callback=lambda *args: displayGroupedData(groupedDatas[int(args[0])]), hover_border=2)
            timeline.create_marker(str(index), 0.0, 100.0, text="Event", move=False, tags=(str(index),))
            index = index + 1
        timeline.draw_timeline()
        timeline.pack(side = TOP, fill = 'x')

def AddFileCommand():
    def AddFileInfo():
        global data
        newData = MediaData(filepath)
        if cal.selection_get() is not None:
            print(cal.selection_get())
            newData.setDate(cal.selection_get())
        if is_float(long.get("1.0","end-1c")) and is_float(lat.get("1.0","end-1c")):
            print(long.get("1.0","end-1c"))
            print(lat.get("1.0","end-1c"))
            newData.setLocation(float(long.get("1.0","end-1c")), float(lat.get("1.0","end-1c")))
        listbox.insert(END, filepath)
        print(newData.getPath())
        print(newData.getKeyWords())
        data.append(newData)
        top.destroy()
    file = filedialog.askopenfile(title='Choose a file', mode='r', filetypes=[('Pictures', '*.png'), ('Pictures', '*.jpeg'), ('Pictures', '*.jpg'), ('Text', '*.txt')])
    if file:
        filepath = str(os.path.abspath(file.name))
        top = Toplevel(app)
        top.geometry("300x360")
        top.title("Add Info")
        Label(top, text = "Date", font=("Arial", 20)).pack()
        cal = Calendar(top, selectmode = 'day', year = 2022)
        cal.pack()
        Label(top, text = "Location", font=("Arial", 20)).pack()
        Label(top, text = "Longitude : ").pack()
        long = Text(top, height = 1, width = 5)
        long.pack()
        Label(top, text = "Latitude : ").pack()
        lat = Text(top, height = 1, width = 5)
        lat.pack()
        Button(top, text = "Done", command=AddFileInfo).pack()


def removeData(path: str):
    global data
    data = list(filter(lambda x: x.getPath() != path, data))

def getData(path: str):
    global data
    for d in data:
        if d.getPath() == path:
            return d
    return None

def onSelectListbox(event):
    w = event.widget
    if len(w.curselection()) != 0:
        index = int(w.curselection()[0])
        path = w.get(index)
        d = getData(path)
        if d is not None:
            m = Menu(app, tearoff=0)
            m.add_command(label="Edit", command = lambda : (displayDataInfo(d)))
            m.add_command(label="Delete", command = lambda : (removeDataInfo(w, index)))
            try:
                m.tk_popup(event.x_root, event.y_root)
            finally:
                m.grab_release()

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
m2.add_command(label = "Grouping data", command = GroupDataCommand)
menu.add_cascade(label = "Edit", menu = m2)

app.config(menu = menu)

listbox = Listbox(app, selectmode='extended')
listbox.pack(side = BOTTOM, fill = BOTH)
scrollbar = Scrollbar(app, orient='vertical', command=listbox.yview)
#scrollbar = Scrollbar(listbox, orient='vertical', command=listbox.yview)
listbox['yscrollcommand'] = scrollbar.set
scrollbar.pack(side = RIGHT, fill = BOTH)
listbox.bind("<Button-2>", onSelectListbox) 

#displayImg(app, "/Users/nathanfain/Documents/CSC864_Multimedia/media/birthday.png")


if __name__ == '__main__':
    app.mainloop()