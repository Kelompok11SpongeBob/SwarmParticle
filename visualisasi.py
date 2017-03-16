import numpy as np
import matplotlib
import numpy as np
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
matplotlib.rcParams['xtick.direction'] = 'out'
matplotlib.rcParams['ytick.direction'] = 'out'

def sixhump(X,Y):
    A = ((4 - (2.1 * X**2) + (X**4 / 3)) * X**2 + X * Y + ((-4 + 4 * Y**2) * Y**2))
    return A 

def dropwave(X,Y):
    A = -((1 + np.cos(12 * np.sqrt(X**2 + Y**2))) / (0.5*(X**2 + Y**2) + 2))
    return A

def shubert(X,Y):
    tempx = 0
    tempy = 0

    for i in range(1,5):
        tempx += i * np.cos((i + 1) * X + 1)
        tempy += i * np.cos((i + 1) * Y + 1)
    A = -tempx * tempy
    return A

# Make data.
X = np.arange(-3, 3, 0.01)
Y = np.arange(-3, 3, 0.01)
X, Y = np.meshgrid(X, Y)
#https://en.wikipedia.org/wiki/Rosenbrock_function

Z = sixhump(X,Y)

num_func_params = 3
num_swarm = 100
position = -3 + 6 * np.random.rand(num_swarm, num_func_params)
velocity = np.zeros([num_swarm, num_func_params])
personal_best_position = np.copy(position)
personal_best_value = np.zeros(num_swarm)

for i in range(num_swarm):
    #Z = (1-X)**2 + 1 *(Y-X**2)**2
    personal_best_value[i] = (1-position[i][0])**2 + 1 *(position[i][1]-position[i][0]**2)**2

tmax = 200
c1 = 0.001
c2 = 0.002
#omega=0.9
levels = np.linspace(-1, 35, 100)
global_best = np.min(personal_best_value)
global_best_position = np.copy(personal_best_position[np.argmin(personal_best_value)])

for t in range(tmax):
    for i in range(num_swarm):
        error = (1-position[i][0])**2 + 1 *(position[i][1]-position[i][0]**2)**2
        if personal_best_value[i] > error:
            personal_best_value[i] = error
            personal_best_position[i] = position[i]
    best = np.min(personal_best_value)
    best_index = np.argmin(personal_best_value)
    if global_best > best:
        global_best = best
        global_best_position = np.copy(personal_best_position[best_index])
        
    for i in range(num_swarm):
        #update velocity
        #velocity[i] = 2 / np.absolute(2 - (c1 + c2) - ((c1 + c2)**2 - 4 * (c1 + c2))**0.5) * (omega * velocity[i] + c1 * np.random.rand() * (personal_best_position[i]-position[i]) + c2 * np.random.rand() * (global_best_position - position[i]))
        velocity[i] += c1 * np.random.rand() * (personal_best_position[i]-position[i]) + c2 * np.random.rand() * (global_best_position - position[i])
        position[i] += velocity[i]
    #omega-=0.0025
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    #CS = plt.contour(X, Y, Z, levels =levels, cmap=cm.gist_stern)
    plt.gca().set_xlim([-3,3])
    plt.gca().set_ylim([-3,3])
    tx =[]
    ty =[]
    tz =[]

    for i in range(num_swarm):
        tx.append(i)
        ty.append(i)
        tz.append(i)
        tx[i] = position[i][0]
        ty[i] = position[i][1]
        tz[i] = position[i][2]
        #plt.plot(position[i][0], position[i][1], 'go')
    ax.scatter(tx, ty, tz, c='g', marker='o')
    ax.scatter(global_best_position[0], global_best_position[1], global_best_position[2], c='r', marker='x')
    #plt.plot(global_best_position[0], global_best_position[1], global_best_position[2], 'ro')
    
    plt.title('{0:03d}'.format(t))
    filename = 'frame{0:03d}.png'.format(t)
    plt.savefig(filename, bbox_inches='tight')
    plt.close(fig)