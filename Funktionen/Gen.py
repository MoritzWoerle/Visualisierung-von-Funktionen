#Importieren der benötigten Librarys:
import numpy as np;
from tkinter import *;
from tkinter import ttk;
import time;
from PIL import Image, ImageTk;
from numba import jit, cuda;
import math;

#Definieren der Funktion, die durch die andere Datei aufgerufen wird:
def gen(dim1, scale):
    #Entscheiden, ob die Funktion auf der GPU oder dem CPU ausgeführt wird:
    if dim1 < 1024:
        data = cpufunc(dim1, dim1/scale);
    else:
        data = np.ones((dim1, dim1, 3), dtype=np.uint8);
        try:
            func[1024, 1024](data, dim1, dim1/1024, dim1/scale);
        except:
            print("Die Funktion ist nicht valide");
    return data;

#Definieren der Funktion, die auf der Grafikkarte ausgeführt wird:
@cuda.jit()
def func(data, dim, dimpart, scale):
    for x1 in range(dimpart):
        for y1 in range(dimpart):

            #Umwandeln der Koordinaten:
            x2 = int(x1 + dimpart * (cuda.threadIdx.x));
            y2 = int(y1 + dimpart * (cuda.blockIdx.x));

            x = (x2 - dim/2) / scale; 
            y = -(y2 - dim/2) / scale;

            #Berechnen der Funktion:
            eq = y + 2 * math.sin(2 * y) - math.sin(x) + 2 - x

            eq = eq * scale;

            #Pixel einfärben:
            if eq < 0:
                data[y2, x2, 2] = -eq % 256;
            elif eq >= 0:
                data[y2, x2, 0] = eq % 256;

#Definieren der Funktion, die auf dem CPU ausgeführt wird:
def cpufunc(dim, scale): 
    try:
        data = np.ones((dim, dim, 3), dtype=np.uint8);
        for x1 in range(dim):
            for y1 in range(dim):

                #Umwandeln der Koordinaten
                x = (x1 - dim/2) / scale;
                y = -(y1 - dim/2) / scale;

                #Funktion berechnen:
                eq = y + 2 * math.sin(2 * y) - math.sin(x) + 2 - x

                eq = eq * scale;

                #Pixeln einfärben:
                if eq < 0:
                    data[y1, x1, 2] = -eq % 256;
                elif eq >= 0:
                    data[y1, x1, 0] = eq % 256;
        return data;
    except:
        print("Die Funktion ist nicht valide");