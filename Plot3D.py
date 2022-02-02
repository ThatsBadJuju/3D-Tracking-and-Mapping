import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D



# find a parabola from 3 points
def calc_parabola(x1, y1, x2, y2, x3, y3):
    # y1 = a*x1*x1 + b*x1 + c
    # y2 = a*x2*x2 + b*x2 + c
    # y3 = a*x3*x3 + b*x3 + c

    parabola_matrix = np.array([[x1*x1, x1, 1], [x2*x2, x2, 1], [x3*x3, x3, 1]])
    y_vector = np.array([y1, y2, y3])
    quadratic_equation = np.linalg.solve(parabola_matrix, y_vector)
    return quadratic_equation


figure = plt.figure()
axes = figure.add_subplot(111, projection='3d')
# x=np.linspace(-2*np.pi, 2*np.pi)
# sinx=np.sin(x) # calculate sin(x)
# plt.plot(x,sinx, np.cos(x)) #plot x on x-axis and sin_x on y-axis
quadratic_array = [0]
try:
    quadratic_array = calc_parabola(0, 20, 1, 21, 2, 20)
except:
    print("Infinite or no solutions to the points")
    sys.exit(1)

a = quadratic_array[0]
assert a != 0, "Not a quadratic equation"
b = quadratic_array[1]
c = quadratic_array[2]

print(a, b, c)

x = np.linspace(0,10)
z = a * x * x + b * x + c
y = np.linspace(0,0)

plt.plot(x, y, z)
plt.show()
