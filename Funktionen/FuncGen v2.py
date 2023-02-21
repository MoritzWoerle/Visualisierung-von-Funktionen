#Importieren der ben�tigten Librarys
from ctypes.wintypes import RGB
from turtle import bgcolor, color, width
import numpy as np;
from tkinter import *;
from tkinter import ttk;
import time;
from PIL import Image, ImageTk;
from numba import jit, cuda; 
import Gen;
import sys;
import fileinput;
from importlib import reload;
from tkinter import filedialog;
import math;
import winsound;

#Erstellen eines leeres Arrays und eines leeren Bildes:
data = np.ones((1024, 1024, 3), dtype=np.uint8);
img1 = Image.fromarray(data);

#Definieren der Funktion zum Generieren des Arrays:
def generate(event):
    #Austauschen der alten Funktion durch die neue Funktion in der anderen Datei:
    global oldeq;
    for line in fileinput.input("Gen.py", inplace = True):

        line = line.replace(oldeq, e2.get());

        sys.stdout.write(line);
    
    #die neue Funktion als alte Funktion speichern und neuladen der Datei:
    oldeq = e2.get();
    f = open("Formel.txt", "w");
    f.write(oldeq);
    f.close();
    reload(Gen);

    #neues Array mit der neuen Funktion generieren:
    data = Gen.gen(int(res.get()), sel2.get());

    #Umwandeln des Arrays in ein Bild und Aktualisierung des Bildes in der GUI:
    global img1;
    img1 = Image.fromarray(data); 
    global img2;
    img2 = img1;
    img1 = img1.resize((1024,1024)); 
    img = ImageTk.PhotoImage(img1); 
    panel.configure(image = img); 
    panel.image = img;

#Definieren der Funktion zum Speichern des Bildes:
def save(event):
    #Dateispeicherungsdialogfenster �ffnen:
    f = filedialog.asksaveasfilename(initialfile = "image_" + str(time.time()) + ".png", defaultextension=".png", filetype = [("All Files","*.*"),("Images","*.png")]);
    #Bild als Datei speichern:
    if f:
        global img2;
        img2.save(f);

def animate():
    for i in range(241):
        e2.delete(0,1024);
        equat = "(x * math.cos(y)) * " + str(i / 240) + " - y";
        e2.insert(0, equat);
        generate();
        global img2;
        img2.save("anim/image_" + str(i) + ".png");
    e2.delete(0, 1024);
    e2.insert(0, oldeq);

#verf�gbare Aufl�sungen definieren
resolutions = ["128", "256", "512", "1024", "2048", "4096", "8192", "16384", "32786"];

#Erstellen der GUI:
root = Tk();
root.configure(bg = '#000000');

style_ref = ttk.Style();
style_ref.configure("TFrame", 
                    background='#000000'
                    );
style_ref.configure("My.TFrame", 
                    background='#121212'
                    );
style_ref.configure("TButton", 
                    background = '#121212',
                    foreground = '#121212',
                    activebackground = '#1F1B24'
                    );
style_ref.configure("TLabel", 
                    background='#121212', 
                    foreground = '#FFFFFF'
                    );


#Erstellen des Ausrichtungsrasters:
frm = ttk.Frame(root);
frm.grid();

frm2 = ttk.Frame(frm, relief= RAISED, borderwidth= 10, style = 'My.TFrame');
frm2.grid(column = 1, row = 28);

eqfrm = ttk.Frame(frm2, style = 'My.TFrame');
eqfrm.grid(column = 0, row = 1, pady = 16, padx = 16);

rsfrm = ttk.Frame(frm2, style = 'My.TFrame');
rsfrm.grid(column = 0, row = 2, pady = 16, padx =16);

scfrm = ttk.Frame(frm2, style = 'My.TFrame');
scfrm.grid(column = 0, row = 3, pady = 16, padx = 16);

btnfrm = ttk.Frame(frm2, style = 'My.TFrame');
btnfrm.grid(column = 0, row = 4, pady = 16, padx = 16);

#Umwandeln des Arrays in ein Bild und Erstellung des Anzeigefeldes:
img = ImageTk.PhotoImage(Image.fromarray(data));
panel = Label(frm, image = img, relief= RAISED, bd = 5)
panel.grid(column = 0, row = 0, rowspan = 64, pady=25, padx = 128);
panel.configure(bg = '#121212');

ttk.Label(frm2, text = "Settings").grid(column = 0, row = 0, padx = 16, pady = 16);

#Beschriftung f�r das Eingabefeld der Formel:
ttk.Label(eqfrm, text = "Equation:").grid(column = 0, row = 0, padx = 5, pady = 5);

#alte Formel aus der Datei lesen:
f = open("Formel.txt", "r");
oldeq = f.read();
f.close();

#Eingabefeld f�r die Formel erstellen:
e2 = Entry(eqfrm);
e2.grid(column  = 0, row = 1, padx = 5, pady = 5);
e2.insert(0, oldeq);
e2.configure(bg = '#1F1B29',
             fg = '#FFFFFF',
             highlightbackground = '#332940',
             width= 48,
             selectforeground= '#FFFFFF'
             );

#Umwandeln der verf�gbaren Aufl�sungen in eine StringVar:
res = StringVar(rsfrm);
res.set("1024");

#Beschriftung des Auswahlfeldes f�r die Aufl�sung:
ttk.Label(rsfrm, text = "Resolution:").grid(column = 0, row = 3, padx = 5, pady = 5);

#Auswahlmen� f�r die Aufl�sungen:
sel = OptionMenu(rsfrm, res, *resolutions);
sel.grid(column = 0, row = 4);
sel.configure(bg = '#1F1B24',
               fg = '#FFFFFF',
               activeforeground = '#FFFFFF',
               activebackground = '#332940',
               highlightbackground = '#121212'
               );

#Beschriftung f�r den Skalierungsschieberegler:
ttk.Label(scfrm, text = "Scale:").grid(column = 0, row = 6, padx = 5, pady = 5);

#Erstellen des Skalierungsschiebereglers:
sel2 = Scale(scfrm, from_=1, to=128, orient = HORIZONTAL);
sel2.set(64);
sel2.grid(column = 0, row = 7);
sel2.configure(bg = '#121212',
               fg = '#FFFFFF',
               troughcolor = '#1F1B24',
               activebackground = '#332940',
               highlightbackground = '#121212',
               length= 256
               );

style_ref.configure("My.TLabel", 
                    background='#1F1B24', 
                    foreground = '#FFFFFF',
                    relief = RAISED,
                    borderwidth = 5,
                    border = 5,
                    width = 12,
                    height = 50,
                    anchor = CENTER
                    );

#Knopf f�r das Generieren erschaffen:
btn = ttk.Label(btnfrm, text = 'Generate', style = 'My.TLabel')
btn.grid(column = 0, row = 0, padx = 5, pady = 5)
btn.bind('<Button-1>', generate)
btn.bind('<Enter>', lambda e: btn.configure(background = '#332940'))
btn.bind('<Leave>', lambda e: btn.configure(background = '#1F1B24'))

#Erstellung des Knopfes zum Speichern des Bildes:
btn2 = ttk.Label(btnfrm, text = 'Save', style = 'My.TLabel')
btn2.grid(column = 0, row = 1, padx = 5, pady = 5)
btn2.bind('<Button-1>', save)
btn2.bind('<Enter>', lambda e: btn2.configure(background = '#332940'))
btn2.bind('<Leave>', lambda e: btn2.configure(background = '#1F1B24'))

#btn3 = ttk.Button(frm, text = "Animate", command = animate).grid(column = 0, row = 10)

root.bind('<Escape>', lambda e: root.destroy());

root.attributes("-fullscreen", True);

root.mainloop();