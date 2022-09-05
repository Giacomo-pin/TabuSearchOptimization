import os
import cv2
import time
import copy
import numpy as np
from matplotlib import pyplot as plt


#################################################################################
#                           GRAY BINARY ENCODING
#################################################################################


'''
To get the gray encoding of an integer I will use dec_to_gray to map to integers (N -> M) and then the dec_to_4bit function to write it in gray encoding.
The bit_flip (binary, i) function takes a binary string and flip the i-th bit, it can be used in any encoding.
After the flip of a bit in gray code it is necessary to return to the corresponding integer with the command int (number, 2) (IN BINARY CODE) and finally remapping the integer to obtain the correct number corresponding to the gray encoding with the gray_to_dec () function


Esempio: N = 4 

Binario  4    ----------(dec_to_4bit)------------->    0100 

Gray     4    --(xor)-->    6    --(dec_to_4bit)-->    0110 

NB:
0100 corrisponde a  4 in codifica binaria
0110 corrisponde a  6 in codifica binaria
1110 corrisponde a 14 in codifica binaria 

0110 corrisponde a  4 in codifica gray
1110 corrisponde a 11 in codifica gray

flip del primo bit         : 0110 --> 1110 
torno al decimale(binario) : 1110 --> 14   
gray_to_dec(14)            : 14 ----> 11


Example: 
             2D function 4 bit

x -> [0,16]
y -> [0,16]

Initial configuration: (x0,y0) = (4,7) --> 0110 0100

DECIMALE    |    BINARIO     |     GRAY
---------------------------------------
    0       |       0000     |     0000
    1       |       0001     |     0001
    2       |       0010     |     0011
    3       |       0011     |     0010
    4       |       0100     |     0110
    5       |       0101     |     0111
    6       |       0110     |     0101
    7       |       0111     |     0100
   11       |       1011     |     1110

Initial configuration:  0110 0100


Bit nr: 1  2  3  4  5  6  7  8
        ----------------------
        0  1  1  0  0  1  0  0
        ¯¯¯¯¯¯¯¯¯¯  ¯¯¯¯¯¯¯¯¯¯

Flipped Bit    |    GRAY     |     New Config (decimal)
---------------------------------------

     1         |  1110 0100  |   (11, 7)
     2         |  0010 0100  |   ( 3, 7)
     3         |  0100 0100  |   ( 7, 7)
     4         |  0111 0100  |   ( 5, 7)
     5         |  0110 1100  |   ( 4, 8)
     6         |  0110 0000  |   ( 4, 0)
     6         |  0110 0110  |   ( 4, 4)
     6         |  0110 0101  |   ( 4, 6)
'''

def dec_to_4bit(number):
    '''dec_to_4bit trasforma un numero intero nell'intervallo [0,15] in una stringa a 4 bit in codifica binaria.
     Quindi per ottenere un intero N in codifica binaria (4bit) uso la funzione dec_to_4bit.'''
    binary = bin(number).replace('0b','')
    x = binary[::-1]
    while len(x)<4:
        x+='0'
    binary = x[::-1]
    return binary
    

def dec_to_nbit(number,nbit):
    binary = bin(number).replace('0b','')
    x = binary[::-1]
    while len(x)<nbit:
        x+='0'
    binary = x[::-1]
    return binary


def bit_flip(binary,i):
    binflip = copy.deepcopy(binary)
    if binflip[i]=='0' : binflip[i]='1'
    else : binflip[i]='0'
    return binflip

def dec_to_gray(int_number):
    ''' dec_to_gray trasforma un intero N in un intero M, il cui binario è la codifica di N in codice gray.'''
    gray = int_number ^ (int_number>>1)
    return gray

def gray_to_dec(int_number):
    inv = 0
    while (int_number):
        inv = inv^int_number
        int_number   = int_number>>1
    return inv
