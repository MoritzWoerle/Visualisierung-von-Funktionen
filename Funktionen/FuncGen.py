import numpy as np;
import math;
from PIL import Image;
import time;
from numba import jit, cuda;

time1 = time.time();

dim = 16384;
offy = dim/2;
offx = dim/2;
part = 1024;
dimpart = dim/part;
rd = dim/4;
scale = dim/64;
data = np.ones((dim, dim, 3), dtype=np.uint8);

#eq = ((x - offx)**2 + (y - offy)**2 - rd**2);
#eq = ((0.1*(x))**3 - y);
#eq = (math.sinh(x) - (y));
#eq = x - y;
#eq = (x - math.tan(y**2)) // scale;
#eq = math.asin(x) - math.cos(y) - x;
#eq = y + 2 * math.sin(2 * y) - math.sin(x) + 2 - x;
#eq = math.sin(2 * math.sin(2 * math.sin(2 * math.sin(x)))) - y;
#eq = x * (math.sin(x) * math.cos(y)) - y;
#eq = math.sin(x) / math.cos(y) - x;

@cuda.jit()
def func(data1):
    for x1 in range(dimpart):
        for y1 in range(dimpart):

            x2 = int(x1 + dimpart * (cuda.threadIdx.x));
            y2 = int(y1 + dimpart * (cuda.blockIdx.x));

            x = (x2 - offx) / scale;
            y = -(y2 - offy) / scale;

            eq = x ** 2 - y;

            eq = eq * scale;

            if eq >= 1:
                data1[y2, x2, 0] = eq;
                data1[y2, x2, 1] = 0;
                data1[y2, x2, 2] = 0;
            elif eq < 1:
                eq = -eq;
                data1[y2, x2, 0] = 0;
                data1[y2, x2, 1] = 0;
                data1[y2, x2, 2] = eq;

func[part, part](data);

print("[Done]");

time2 = time.time();
print("Init:" + str(time2 - time1));

image = Image.fromarray(data);

#image.show();

#image.save("images/test " + str(time.time()) + ".png");