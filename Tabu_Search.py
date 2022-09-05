from random import random, randrange
from math import exp, pi, log
from pylab import plot, ylabel, show, fill
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import time
import math
import copy
from matplotlib import cm
from random import randint
import random
from grayutils import dec_to_4bit, dec_to_nbit, bit_flip, dec_to_gray, gray_to_dec

#################################################################################

def function(x,y,mu,sigma):
    return - np.exp(-(np.power((x-4),2)+np.power((y-mu),2))/(2*np.power(sigma,2)))*1/np.sqrt(2*pi*np.power(sigma,2))

def eggholder(x,y):
    # Site reference for function's details: https://www.sfu.ca/~ssurjano/egg.html
    const = 47
    return - (y+const)*np.sin(np.sqrt(abs(y+x/2+const)))-x*np.sin(np.sqrt(abs(x-(y+const))))

def F6_shaffer(x,y):
    const = 0.5
    return const+(np.power(np.sin(np.sqrt(x*x + y*y)),2)-const)/np.power((1+0.001*(x*x + y*y)),2)

#################################################################################
#################################################################################
print('')
print('     #####################################')
print('     ------------ Tabu Search ------------')
print('     #####################################')
print('')
#################################################################################
#-----------------------------SET OF PARAMETERS---------------------------------#
#################################################################################

N_iter      = 1000
N_variables = 2
N_bit       = 10
tabu_length = 4

Eggholder = False
Shaffer   = True
#################################################################################
#################################################################################
minimum = np.power(2,N_bit-1)
maximum = minimum

print('     N iteration : {}'.format(str(N_iter)))
print('     N bit : {}'.format(str(N_bit)))
print('')
# Initialization ---------------------------------------#
'''
Creating the two discrete variable, they must have the lenght of 2 to the power
 of the number of bit, N_bit.'''

x   = np.array([i for i in np.arange(-minimum,maximum)],float)
y   = np.array([i for i in np.arange(-minimum,maximum)],float)
x,y = np.meshgrid(x,y)

# Tabulated eggholder
if Eggholder == True:
    z = eggholder(x,y)

if Shaffer==True:
    x = x/10
    y = y/10
    z = F6_shaffer(x,y)    
 
# Initial configuration (should be rnd) ----------------------------------------#
'''
Values of the function are tabulated. The function is defined on a square with 
lenght np.power(2,N_bit)). The coordinates x and y range from 0 to np.power(2,N_bit)) and are encoded using the gray binary code. The trial move are defined by the flipping of one bit. Tabu search consists in exploring the whole neighbourhood (flipping of every possible bit) of a certain configuration and in picking the best move. Then we keep trace of the performed bit flip (best one), and we don't allow the algorithm to perform the same flip for a certain time by adding the move in a tabu list.

'''

x1,y1  = [randint(0,np.power(2,N_bit)),randint(0,np.power(2,N_bit))]
coord  = [x1,y1]
xcoord = [x1]
ycoord = [y1]

print('     Initial configuration [x,y]: {}'.format(str(coord)))
print('')
print('     -------------- MINIMUM --------------')
print('')
global_minimum_point = np.argmin(z)
y_MIN = np.asarray(np.unravel_index(global_minimum_point, z.shape))[0]
x_MIN = np.asarray(np.unravel_index(global_minimum_point, z.shape))[1]
print('     Value at global minimum : {}'.format(str(np.round(np.min(z),2))))
print('     Coordinates of minimum  : [{}, {}] '.format(str(x_MIN),str(y_MIN)))

LOSS      = []
tabu_list = []
for iteration in range(N_iter):

        #1) First Iteration
        if iteration==0:                
            loss_old  = z[coord[1],coord[0]]
            LOSS.append(loss_old)


        #2) Tabu Search
        Loss       = []
        List_coord = [[],[]]
        List_bit   = []
        for variable in range(N_variables):

            # Converting int to a nbit number
            # Make a copy of coordinates on which perform a trial move.
            coord_TRIAL = copy.deepcopy(coord)
            coord_TRIAL_bit = dec_to_nbit(dec_to_gray(coord_TRIAL[variable])
                                                                     ,N_bit)

            # Converting the n-th variable into a 4bit string in gray code .  
            # Converting nbit to int([0,15])                
            binary_list = list(coord_TRIAL_bit)

            # Begin to perform trial move (flipping bits)
            for bit in range(N_bit):

                # Skip on the tabu trial move!
                if np.any([tabu==variable*N_bit+bit for tabu in tabu_list]): 
                    continue
                
                flipped  = "".join(bit_flip(binary_list,bit))
                new_var = gray_to_dec(int(flipped,2))

                coord_TRIAL[variable] = new_var

                ####### CALCULATE COST FUNCTION, IF BETTER: UPDATE! 
                cost_new   =  z[coord_TRIAL[1],coord_TRIAL[0]]
                
                # Take trace of the move
                N_bit_flip = copy.deepcopy(variable*N_bit+bit)

                List_bit.append(N_bit_flip)
                Loss.append(cost_new)
                List_coord[0].append(coord_TRIAL[0])
                List_coord[1].append(coord_TRIAL[1])

        Loss = np.asarray(Loss)   
        index  = np.random.choice(np.asarray(np.where(Loss == Loss.min()))[0])

        N_move = List_bit[index]
        loss_old = Loss[index]

        coord_best = copy.deepcopy([List_coord[0][index],List_coord[1][index]])

        # Appending trial move to the tabu list                
        tabu_list.append(N_move)
        if iteration%1==0 and iteration>tabu_length-1:
           tabu_list.pop(0)

        # New configuration
        coord    = coord_best
        
        # Saving the trajectory
        xcoord.append(coord[0])
        ycoord.append(coord[1])
        LOSS.append(loss_old)
      

#------------------------------------------------------------------------------
# MINIMUM FOUND

index_min    = np.argmin(LOSS)
x_min_search = xcoord[index_min]
y_min_search = ycoord[index_min]
min_coord    = [x_min_search,y_min_search]

MINIMUM      = np.round(np.min(LOSS),2)
print('')
print('     Value evaluated minimum       : {}'.format(str(MINIMUM)))
print('     Coordinates evaluated minimum : {}'.format(str(min_coord)))
if 1:
    retta_min = np.array([np.min(z) for i in range(len(LOSS))])
    plt.plot(LOSS, 'k')
    plt.plot(index_min, LOSS[index_min], 'om', label='TABU minimum')    
    plt.plot(retta_min,'--r', label='GLOBAL minimum')
    plt.title('Accepted configuration loss function')
    plt.legend()
    plt.grid(True)
    plt.show()


if Eggholder==True:
    fig  = plt.figure()
    ax   = fig.gca(projection='3d')
    surf = ax.plot_surface(x, y, z*10, cmap='viridis',
                    linewidth=0, antialiased=False)
    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.xlabel('x')
    plt.ylabel('y')
    #plt.xlim([0,30])
    plt.show()

if 1:
    xcoord = (np.asarray(xcoord))
    ycoord = (np.asarray(ycoord))
  
    plt.imshow(z, cmap='viridis')
    
    plt.plot(x_MIN,y_MIN,'or', label='GLOBAL MINIMUM')
    plt.plot(x_min_search,y_min_search,'*c', label='TABU MINIMUM')

    if 1:
        snake_length = 10
        for i in range(len(xcoord)):     
                plt.imshow(z, cmap='viridis')
                plt.plot(x_MIN,y_MIN,'or', label='GLOBAL MINIMUM')
                plt.plot(x_min_search,y_min_search,'*c', label='TABU MINIMUM') 
                if i<snake_length:
                    plt.plot(xcoord[0:i],ycoord[0:i],'k', linewidth=2,
                                                    label='Trajectory')
                if i>snake_length:
                    plt.plot(xcoord[0:i],ycoord[0:i],'k', alpha=0.3, linewidth=2,
                                                    label='Trajectory')
                    plt.plot(xcoord[i-snake_length:i],ycoord[i-snake_length:i],
                                            'k', linewidth=2, label='Trajectory')
                
                if Shaffer == True:
                   plt.xlim([200,800])
                   plt.ylim([200,800])
                plt.pause(0.001) 
                plt.clf()

    plt.title('Heatmap optimization function')
    plt.show()



if 1:
    xcoord = (np.asarray(xcoord))
    ycoord = (np.asarray(ycoord))
    t      = np.array([i for i in range(len(xcoord))])
    plt.imshow(z, cmap='viridis') #'.k'
    plt.scatter(xcoord,ycoord, c=t, cmap='gray',linewidth=2)
    plt.plot(x_MIN,y_MIN,'or', label='GLOBAL MINIMUM')
    plt.plot(x_min_search,y_min_search,'*m', label='TABU MINIMUM')
    plt.legend()
    plt.title('Heatmap optimization function')
    plt.show()


print('')
print('     #####################################')
print('')
    
