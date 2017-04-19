import numpy as np
import matplotlib
import numpy as np
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import time as time
matplotlib.rcParams['xtick.direction'] = 'out'
matplotlib.rcParams['ytick.direction'] = 'out'

class fish:
    def __init__(self):
        self.origin=[0 for i in range(2)]
        self.position=[0 for i in range(2)]
        self.velocity=[0 for i in range(2)]

class shark:
    def __init__(self):
        self.origin=[0 for i in range(2)]
        self.position=[0 for i in range(2)]
        self.velocity=[0 for i in range(2)]
        self.lifetime=10
        self.team=0
        self.target=fish()

#Init
num_func_params = 2
swarm_row = 60
swarm_col = 60
num_sharks=3

radius=10**2#sesuaikan
thrustscale=0.7
gravityscale=0.25

space = 1
margin = 2

fishswarm=[[fish() for i in range(swarm_col)] for j in range(swarm_row)]
for i in range(swarm_row):
    for j in range(swarm_col):
        fishswarm[i][j].position[0]=margin + space * j
        fishswarm[i][j].position[1]=margin + space * i
        fishswarm[i][j].origin[0]=margin + space * j
        fishswarm[i][j].origin[1]=margin + space * i
        
sharks=[shark() for i in range(num_sharks)]
for i in range(num_sharks):
    sharks[i].position=2+np.random.rand(num_func_params) * 60
    sharks[i].origin=sharks[i].position
    var = 1
    while var == 1 :
        sharks[i].velocity=np.random.rand(num_func_params)
        if sharks[i].velocity[0]!=0 and sharks[i].velocity[1]!=0:
            if sharks[i].velocity[0]<0.1:
                sharks[i].velocity[0]+=0.1
                '''if sharks[i].velocity[0]<0.3:
                    sharks[i].velocity[0]+=0.4
                else:
                    sharks[i].velocity[0]+=0.2'''
            if sharks[i].velocity[1]<0.1:
                sharks[i].velocity[1]+=0.1
                '''if sharks[i].velocity[1]<0.3:
                    sharks[i].velocity[1]+=0.4
                else:
                    sharks[i].velocity[1]+=0.2'''
            direction=[0 for i in range(2)]
            direction=np.random.randint(2, size=2)
            if direction[0]==1:
                sharks[i].velocity[0]*=-1
            if direction[1]==1:
                sharks[i].velocity[1]*=-1
            break


#Step
tmax = 400

for t in range(tmax):
    fig = plt.figure()
    #CS = plt.contour(X, Y, Z, levels =levels, cmap=cm.gist_stern)
    plt.gca().set_xlim([0,64])
    plt.gca().set_ylim([0,64])

    for i in range(num_sharks):
        if t%2==0:
            sharks[i].position+=sharks[i].velocity
            if sharks[i].position[0]<=2 or sharks[i].position[0]>=62:
                sharks[i].velocity[0]*=-1
            if sharks[i].position[1]<=2 or sharks[i].position[1]>=62:
                sharks[i].velocity[1]*=-1

    for i in range(swarm_row):
        for j in range(swarm_col):
            for k in range(num_sharks):
                dx=sharks[k].position[0]-fishswarm[i][j].position[0]
                dy=sharks[k].position[1]-fishswarm[i][j].position[1]
                dist=dx*dx+dy*dy
                forcescale=-radius/dist
                if dist<radius:
                    rad=np.arctan2(dy,dx)
                    fishswarm[i][j].velocity[0]+=forcescale*np.cos(rad)
                    fishswarm[i][j].velocity[1]+=forcescale*np.sin(rad)
                fishswarm[i][j].velocity[0]*=thrustscale
                fishswarm[i][j].velocity[1]*=thrustscale
                fishswarm[i][j].position[0]+=fishswarm[i][j].velocity[0]+(fishswarm[i][j].origin[0]-fishswarm[i][j].position[0])*gravityscale
                fishswarm[i][j].position[1]+=fishswarm[i][j].velocity[1]+(fishswarm[i][j].origin[1]-fishswarm[i][j].position[1])*gravityscale
            plt.plot(fishswarm[i][j].position[0], fishswarm[i][j].position[1], 'b.', markersize=2.0)

    for i in range(num_sharks):
        plt.plot(sharks[i].position[0], sharks[i].position[1], 'ro', markersize=7.0)
    
    plt.title('{0:03d}'.format(t))
    filename = 'img{0:03d}.png'.format(t)
    plt.savefig(filename, bbox_inches='tight')
    plt.close(fig)