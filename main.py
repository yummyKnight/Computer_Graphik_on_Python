import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import pygame

def insidetriangle(xList, yList):
    xs = xList
    ys = yList
    x_range = np.arange(np.min(xs), np.max(xs) + 1)
    y_range = np.arange(np.min(ys), np.max(ys) + 1)

    X, Y = np.meshgrid(x_range, y_range)
    xc = np.mean(xs)
    yc = np.mean(ys)

    triangle = np.ones(X.shape, dtype=bool)
    for i in range(3):
        ii = (i + 1) % 3
    if xs[i] == xs[ii]:
        include = X * (xc - xs[i]) / abs(xc - xs[i]) > xs[i] * (xc - xs[i]) / abs(xc - xs[i])
    else:
        poly = np.poly1d([(ys[ii] - ys[i]) / (xs[ii] - xs[i]), ys[i] - xs[i] * (ys[ii] - ys[i]) / (xs[ii] - xs[i])])
        include = Y * (yc - poly(xc)) / abs(yc - poly(xc)) > poly(X) * (yc - poly(xc)) / abs(yc - poly(xc))
    triangle *= include

    return X[triangle], Y[triangle]

# с помощью линейного решателя находим уравнение плоскости #треугольника в пространстве, и выражаем его через Z.

XListFir = [1 + 50, 100 + 50, 50]
YListFir = [10, 50, 250]
ZListFir = [50, 50, -10]

XListSec = [1, 100, 50]
YListSec = [25, 45, 450]
ZListSec = [5, 5, -9]

x1 = XListFir[:]
x1.append(XListFir[0])
y1 = YListFir[:]
y1.append(YListFir[0])
z1 = ZListFir[:]
z1.append(ZListFir[0])

# Отрисовка заданных ранее треугольников.
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# отдаем функции дискретизации координаты проекции треугольника на XoY.
bufferFirstTriangle = insidetriangle(XListFir, YListFir)
bufferSecondTriangle = insidetriangle(XListSec, YListSec)

massX = bufferFirstTriangle[0]
massY = bufferFirstTriangle[1]

massX2 = bufferSecondTriangle[0]
massY2 = bufferSecondTriangle[1]

print(bufferFirstTriangle)
print(massX)
print(massY)

# Находим плоскость полигона
coord = [
    [XListFir[0], YListFir[0], 1],
    [XListFir[1], YListFir[1], 1],
    [XListFir[2], YListFir[2], 1],  # it XYZ COORDS
    ZListFir  # IT FULL Z COORDS
]
coord2 = [
    [XListSec[0], YListSec[0], 1],
    [XListSec[1], YListSec[1], 1],
    [XListSec[2], YListSec[2], 1],  # it XYZ COORDS
    ZListSec  # IT FULL Z COORDS
]


def ploskost(coord):
    M5 = np.array([coord[0], coord[1], coord[2]])  # Матрица (левая часть)(3 координаты)
    v5 = np.array(coord[3])  # Вектор (правая часть)
    result = np.linalg.solve(M5, v5)
    return [round(elem, 2) for elem in result]


urPloskosti = ploskost(coord)  # ур.плоскости 1 треугольника
urPloskosti2 = ploskost(coord2)  # ур.плоскости 2 треугольника

print(urPloskosti)


# функция получения z координаты по 2 координатам проекции и уравнению плоскости #фигуры
def getZcoord(x, y, urPloskosti):
    return float(urPloskosti[0] * x + urPloskosti[1] * y + urPloskosti[2])


WIDTH = 500

pygame.init()
sc = pygame.display.set_mode((400, 500))

# здесь будут рисоваться фигуры
zbuff = [[-10000] * WIDTH for i in range(WIDTH)]  # инициализируем z-буфер “бесконечным” значением (-10000)
pygame.time.delay(100)

for i in pygame.event.get():
    if i.type == pygame.QUIT:
        exit()

# для каждой ранее дискретизированной точки находим значение глубины (Z-#координаты) и записываем по координатам дискретной точки в z-буфер отображаемый #цвет фигуры. В нашем случае 1 – RED, 2-GREEN.

for i in range(len(massX)):
    if (getZcoord(massX[i], massY[i], urPloskosti) > zbuff[int(massX[i])][int(massY[i])]):
        zbuff[int(massX[i])][int(massY[i])] = 1.

for i in range(len(massX2)):
    if (getZcoord(massX2[i], massY2[i], urPloskosti2) > zbuff[int(massX2[i])][int(massY2[i])]):
        zbuff[int(massX2[i])][int(massY2[i])] = 2.

for i in range(len(zbuff)):
    for j in range(len(zbuff)):
        if (zbuff[i][j] == 1):
            #print("work")
            pygame.draw.line(sc, (255, 0, 0), [i, j], [i, j], 3)
        if (zbuff[i][j] == 2):
            #print("work")
            pygame.draw.line(sc, (0, 255, 0), [i, j], [i, j], 3)

pygame.display.update()
input()

# вывод содержания z-буфера.
for i in range(zbuff.__len__()):
    print(zbuff[i])

