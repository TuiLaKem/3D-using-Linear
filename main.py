import tkinter as tk
from tkinter import *
import math
root = tk.Tk()
root.title("Canvas")
w = 7
h = 7

v = []
dots = []
size = 100
angle = 0


class Vertex:
    def __init__(self,x,y,z,r):
        self.x = x
        self.y = y 
        self.z = z

        self.cx = x - r/2
        self.cy = y - r/2
        self.ccx = x + r/2
        self.ccy = y + r/2

    def printout(self):
        print("X: ", self.x, "Y: ", self.y, "Z: ", self.z)

    def getxyz(self):
        return self.x, self.y, self.z

def addDot(x,y,z):
    a = cvs.create_oval(x - w/2, y-h/2, x + w/2, y+h/2,fill="white")
    v.append(Vertex(x,y,z,h))
    dots.append(a)

def getCoord(x,y):
    return x - w/2, y-h/2


# MOVE RIGHT BY 1
def transform():
    for item in dots:
        crd = cvs.coords(item)
        cx, cy, ccx, ccy = crd
        cx += 1
        ccx += 1 
        cvs.coords(item, cx, cy, ccx, ccy)
    cvs.after(16, transform)


def cos(theta):
    return math.cos(math.radians(theta))
def sin(theta):
    return math.sin(math.radians(theta))


# ROTATION
def run():
    global angle
    angle += 3
    projected = [project(*matrixMult(vt, angle, cod=(300,300,0))) for vt in v]
    
    for i, (a,b) in enumerate(edges):
        x1, y1 = projected[a]
        x2, y2 = projected[b]
        cvs.coords(lines[i], x1, y1, x2, y2)

    
    for i, ball in enumerate(dots):
        px, py = projected[i]
        cvs.coords(ball, px-w/2, py-w/2, px+w/2, py+w/2)
    
    
    cvs.after(16, run)


def rotXMat(angles):
    return(
        [
            [1              , 0             , 0             ],
            [0              , cos(angles)    , -sin(angles)  ],
            [0              , sin(angles)   , cos(angles)   ]
        ]
    )

def rotYMat(angles):
    return(
        [
            [cos(angles)    , 0             , sin(angles)   ],
            [0              , 1             , 0             ],
            [-sin(angles)   , 0             , cos(angles)   ]
        ]
    )

def rotZMat(angles):
    return(
        [
            [cos(angles)    , -sin(angles)  , 0             ],
            [sin(angles)    , cos(angles)   , 0             ],
            [0              , 0             , 1             ]
        ]
    )

def matrixMult(obj, a, cod):
    x,y,z = obj.getxyz()
    scale =0.5
    xMat = rotXMat(a)
    x -= cod[0]
    y -= cod[1]
    z -= cod[2]

    x *= scale
    y *= scale
    z *= scale

    rx = (x*xMat[0][0] + y*xMat[0][1] + z*xMat[0][2]) 
    ry = (x*xMat[1][0] + y*xMat[1][1] + z*xMat[1][2]) 
    rz = (x*xMat[2][0] + y*xMat[2][1] + z*xMat[2][2]) 
    
    yMat = rotYMat(a)

    rx2 = (rx*yMat[0][0] + ry*yMat[0][1] + rz*yMat[0][2]) 
    ry2 = (rx*yMat[1][0] + ry*yMat[1][1] + rz*yMat[1][2]) 
    rz2 = (rx*yMat[2][0] + ry*yMat[2][1] + rz*yMat[2][2]) 


    # xMat = rotZMat(a)

    # rx = (rx*xMat[0][0] + ry*xMat[0][1] + rz*xMat[0][2]) 
    # ry = (rx*xMat[1][0] + ry*xMat[1][1] + rz*xMat[1][2]) 
    # rz = (rx*xMat[2][0] + ry*xMat[2][1] + rz*xMat[2][2]) 

    rx2 += cod[0]
    ry2 += cod[1]
    rz2 += cod[2]
    # print(rx, ry, rz)
    return rx2, ry2, rz2

def project(rx, ry, rz, focal=1000):
    factor = focal / (focal + rz)
    return rx*factor, ry*factor

root.configure(background="#303030")
cvs = Canvas(root, width=600, height=600, highlightthickness=0,  bg="black")


line = cvs.create_line(300, 0,300, 600,fill="green")
line = cvs.create_line(0, 300,600, 300,fill="green")


addDot(300-size, 300-size, size)
addDot(300-size, 300+size, size)
addDot(300+size, 300-size, size)
addDot(300+size, 300+size, size)

# back face
addDot(300-size, 300-size, -size)
addDot(300-size, 300+size, -size)
addDot(300+size, 300-size, -size)
addDot(300+size, 300+size, -size)


edges = [
    (0,1),(1,3),(3,2),(2,0),  
    (4,5),(5,7),(7,6),(6,4),  
    (0,4),(1,5),(2,6),(3,7)  
]
lines = [cvs.create_line(0,0,0,0,fill="white") for _ in edges]
cvs.pack()

# for item in v:
#     item.printout()

# matrixMult(v[2], angle)
# print(rotXMat(90)[0][0])
cvs.after(16, run)

root.mainloop()

