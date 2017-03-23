import numpy as np
import matplotlib
import numpy as np
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
matplotlib.rcParams['xtick.direction'] = 'out'
matplotlib.rcParams['ytick.direction'] = 'out'

class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)


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
X = np.arange(-3, 3, 0.01)########
Y = np.arange(-3, 3, 0.01)#######
X, Y = np.meshgrid(X, Y)
#https://en.wikipedia.org/wiki/Rosenbrock_function

Z = shubert(X,Y)

num_func_params = 3
num_swarm = 100
position = -3 + 6 * np.random.rand(num_swarm, num_func_params)
velocity = np.zeros([num_swarm, num_func_params])
for i in range(num_swarm):#############
    position[i][2]=4
personal_best_position = np.copy(position)
personal_best_value = np.zeros(num_swarm)

for i in range(num_swarm):
    #Z = (1-X)**2 + 1 *(Y-X**2)**2
    personal_best_value[i] = (1-position[i][0])**2 + 1 *(position[i][1]-position[i][0]**2)**2######

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
    fig = plt.figure(figsize=(15,15))
    ax = fig.add_subplot(111, projection='3d')
    #axarr=plt.axes()
    #CS = plt.contour(X, Y, Z, levels =levels, cmap=cm.gist_stern)

    plt.gca().set_xlim([-3,3])#########
    plt.gca().set_ylim([-3,3])##########
    plt.gca().set_zlim([-4,4])
    tx =[]
    ty =[]
    tz =[]

    for i in range(num_swarm):
        lengx=0.4*velocity[i][0]/np.absolute(velocity[i][0])####ganti tergantung fungsi
        lengy=0.4*velocity[i][1]/np.absolute(velocity[i][1])
        degree=np.absolute(velocity[i][1])/np.absolute(velocity[i][0])
        limit=np.absolute(lengy*degree/lengx)
        if limit>1:###ganti tergantung fungsi
            lengx/=limit
            lengy/=limit
        #axarr.arrow(position[i][0],position[i][1],lengx,lengy*degree,head_width=0.05,head_length=0.1,fc='k',ec='k')
        a = Arrow3D([position[i][0],position[i][0]+lengx],[position[i][1],position[i][1]+lengy*degree],[position[i][2],position[i][2]], mutation_scale=20, lw=1, arrowstyle="-|>", color="k")
        ax.add_artist(a)
        tx.append(i)
        ty.append(i)
        tz.append(i)
        tx[i] = position[i][0]
        ty[i] = position[i][1]
        tz[i] = position[i][2]
        #plt.plot(position[i][0], position[i][1], 'go')
    
    ax.scatter(tx, ty, tz, s=50, c='g', marker='o')
    ax.scatter(global_best_position[0], global_best_position[1], global_best_position[2], s=150, c='r', marker='o')
    #plt.plot(global_best_position[0], global_best_position[1], global_best_position[2], 'ro')
    
    ax.set_xlabel('x_values')
    ax.set_ylabel('y_values')
    ax.set_zlabel('z_values')

    plt.title('{0:03d}'.format(t))
    filename = 'frame{0:03d}.png'.format(t)
    plt.savefig(filename, bbox_inches='tight')
    plt.close(fig)