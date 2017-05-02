import numpy as np
import matplotlib
import numpy as np
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import time as time
matplotlib.rcParams['xtick.direction'] = 'out'
matplotlib.rcParams['ytick.direction'] = 'out'

#Referensi:
#1) Source Code behavior fish menjauhi shark: http://codepen.io/soulwire/full/Ffvlo
#2) Pseudocode 4 rules untuk behavior flocking dari fish: http://www.kfish.org/boids/pseudocode.html

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
swarm_row = 20
swarm_col = 20
num_sharks=3
sumSwarm=swarm_row*swarm_col

radius=10**2#sesuaikan
thrustscale=0.7
gravityscale=0.25

dist_betw_fish=1

space = 1
margin = 2

fishswarm=[[fish() for i in range(swarm_col)] for j in range(swarm_row)]
for i in range(swarm_row):
    for j in range(swarm_col):
        fishswarm[i][j].position[0]=margin - 32+ np.random.rand() * 60
        fishswarm[i][j].position[1]=margin - 32+ np.random.rand() * 60
        fishswarm[i][j].origin[0]=margin + space * j
        fishswarm[i][j].origin[1]=margin + space * i
        
sharks=[shark() for i in range(num_sharks)]
for i in range(num_sharks):
    sharks[i].position=margin - 32+np.random.rand(num_func_params) * 60
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
goalPos=[0 for a in range(2)]

for t in range(tmax):
    fig = plt.figure()
    #CS = plt.contour(X, Y, Z, levels =levels, cmap=cm.gist_stern)
    plt.gca().set_xlim([-32,32])
    plt.gca().set_ylim([-32,32])

    
    if t%60==0 and t!=0:
        goalPos=margin - 32+np.random.rand(num_func_params) * 60

    for i in range(num_sharks):
          sharks[i].position+=sharks[i].velocity
          if sharks[i].position[0]<=-30 or sharks[i].position[0]>=30:
              sharks[i].velocity[0]*=-1
          if sharks[i].position[1]<=-30 or sharks[i].position[1]>=30:
              sharks[i].velocity[1]*=-1
    #'''
    sumPos=[0 for w in range(2)]
    sumVel=[0 for w in range(2)]
    for i in range(swarm_row):
        for j in range(swarm_col):
            sumPos[0]+=fishswarm[i][j].position[0]
            sumPos[1]+=fishswarm[i][j].position[1]
            sumVel[0]+=fishswarm[i][j].velocity[0]
            sumVel[1]+=fishswarm[i][j].velocity[1]
    #'''
    absSumPos=[0 for i in range(2)]
    absSumPos=sumPos
    absSumVel=[0 for i in range(2)]
    absSumVel=sumVel
    vr1=[0 for a in range(2)]
    vr2=[0 for a in range(2)]
    vr3=[0 for a in range(2)]
    vr4=[0 for a in range(2)]
    for i in range(swarm_row):
        for j in range(swarm_col):
            #3 rule
            #'''
            sumPos=absSumPos
            sumVel=absSumVel
            vr1=[0,0]
            vr2=[0,0]
            vr4=[0,0]
            sumPos[0]-=fishswarm[i][j].position[0]
            sumPos[1]-=fishswarm[i][j].position[1]
            sumVel[0]-=fishswarm[i][j].velocity[0]
            sumVel[1]-=fishswarm[i][j].velocity[1]
            sumPos[0]/=(sumSwarm-1)
            sumPos[1]/=(sumSwarm-1)
            sumVel[0]/=(sumSwarm-1)
            sumVel[1]/=(sumSwarm-1)
            #if t<60:
            vr1[0]=(sumPos[0]-fishswarm[i][j].position[0])/60 
            vr1[1]=(sumPos[1]-fishswarm[i][j].position[1])/60
            vr3[0]=(sumVel[0]-fishswarm[i][j].velocity[0])/8 
            vr3[1]=(sumVel[1]-fishswarm[i][j].velocity[1])/8
            if t>=60:
                vr4[0]=(goalPos[0]-fishswarm[i][j].position[0])/60
                vr4[1]=(goalPos[1]-fishswarm[i][j].position[1])/60
            #'''
            for c in range(swarm_row):
                for d in range(swarm_col):
                    if c!=i or d!=j:
                        fishx=fishswarm[c][d].position[0]-fishswarm[i][j].position[0]
                        fishy=fishswarm[c][d].position[1]-fishswarm[i][j].position[1]
                        fishdist=fishx*fishx+fishy*fishy
                        if fishdist<dist_betw_fish:
                            vr2[0]-=fishx
                            vr2[1]-=fishy
            #'''
            fishswarm[i][j].position[0]+=(vr1[0]+vr2[0]+vr3[0]+vr4[0])
            fishswarm[i][j].position[1]+=(vr1[1]+vr2[1]+vr3[1]+vr4[1])
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
                fishswarm[i][j].position[0]+=fishswarm[i][j].velocity[0]#+(fishswarm[i][j].origin[0]-fishswarm[i][j].position[0])*gravityscale
                fishswarm[i][j].position[1]+=fishswarm[i][j].velocity[1]#+(fishswarm[i][j].origin[1]-fishswarm[i][j].position[1])*gravityscale
            plt.plot(fishswarm[i][j].position[0], fishswarm[i][j].position[1], 'b.', markersize=4.0)

    for i in range(num_sharks):
        plt.plot(sharks[i].position[0], sharks[i].position[1], 'ro', markersize=7.0)
    if t>=60:
        plt.plot(goalPos[0], goalPos[1], 'g^', markersize=7.0)

    plt.title('{0:03d}'.format(t))
    filename = 'img{0:03d}.png'.format(t)
    plt.savefig(filename, bbox_inches='tight')
    plt.close(fig)
