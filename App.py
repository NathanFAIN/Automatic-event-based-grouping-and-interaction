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

import datetime
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import date
matplotlib.use('agg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)

import math
import numpy as np


data = []
figure_canvas = None
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
    label = Label(ws, text=content, wraplengt=400)
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
        if cal.selection_get() is not None:
            print(cal.selection_get())
            dataToDisplay.setDate(cal.selection_get())
        if is_float(long.get("1.0","end-1c")) and is_float(lat.get("1.0","end-1c")):
            print(long.get("1.0","end-1c"))
            print(lat.get("1.0","end-1c"))
            dataToDisplay.setLocation(float(long.get("1.0","end-1c")), float(lat.get("1.0","end-1c")))
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
        global figure_canvas
        if figure_canvas is not None:
            for item in figure_canvas.get_tk_widget().find_all():
                figure_canvas.get_tk_widget().delete(item)
        dates = []
        labels = []
        for g in groupedDatas:
            g.generateMissingData()
        for g in groupedDatas:
            dates.append(date(g.getDate().year, g.getDate().month, g.getDate().day))
            labels.append(g.getTitle())
        min_date = date(np.min(dates).year - 1, np.min(dates).month, np.min(dates).day)
        max_date = date(np.max(dates).year + 1, np.max(dates).month, np.max(dates).day)
        labels = ['{0:%d %b %Y}:\n{1}'.format(d, l) for l, d in zip (labels, dates)]

        fig, ax = plt.subplots(figsize=(15, 4), constrained_layout=True)
        _ = ax.set_ylim(-2, 1.75)
        _ = ax.set_xlim(min_date, max_date)
        _ = ax.axhline(0, xmin=0.05, xmax=0.95, c='deeppink', zorder=1)
        
        _ = ax.scatter(dates, np.zeros(len(dates)), s=120, c='palevioletred', zorder=2)
        _ = ax.scatter(dates, np.zeros(len(dates)), s=30, c='darkmagenta', zorder=3)


        label_offsets = np.zeros(len(dates))
        label_offsets[::2] = 0.35
        label_offsets[1::2] = -0.7
        for i, (l, d) in enumerate(zip(labels, dates)):
            txt = ax.text(d, label_offsets[i], l, ha='center', fontfamily='serif', fontweight='bold', color='royalblue',fontsize=12)
        stems = np.zeros(len(dates))
        stems[::2] = 0.3
        stems[1::2] = -0.3   
        markerline, stemline, baseline = ax.stem(dates, stems, use_line_collection=True)
        _ = plt.setp(markerline, marker=',', color='darkmagenta')
        _ = plt.setp(stemline, color='darkmagenta')

        # hide lines around chart
        for spine in ["left", "top", "right", "bottom"]:
            _ = ax.spines[spine].set_visible(False)
        
        # hide tick labels
        _ = ax.set_xticks([])
        _ = ax.set_yticks([])
        
        _ = ax.set_title('Timeline of events', fontweight="bold", fontfamily='serif', fontsize=16, 
                        color='royalblue')

        def onclick(event):
            for g in groupedDatas:
                if math.fabs(event.xdata - mdates.date2num(g.getDate())) < 3:
                    displayGroupedData(g)
                    return


        cid = fig.canvas.mpl_connect('button_press_event', onclick)


        figure_canvas = FigureCanvasTkAgg(fig, app)
        # NavigationToolbar2Tk(figure_canvas, app)

        figure_canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        

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
