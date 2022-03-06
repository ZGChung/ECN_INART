# We reuse the codes for TP1 to create the

from random import random
from sys import stdout
import numpy as np


class world:
    # initialise the world
    # L is the number of columns
    # H is the number of lines
    # P is the probability of having a wall in a given tile
    def __init__(self, L, H):
        self.L = L
        self.H = H

        # the world is represented by an array with one dimension
        # initialise every tile to empty (0)
        self.w = [-0.04 for i in range(L*H)]

        # add walls in the first and last columns
        for i in range(H):
            self.w[i*L] = 99
            self.w[i*L+L-1] = 99

        # add walls in the first and last lines
        for j in range(L):
            self.w[j] = 99
            self.w[(H-1)*L + j] = 99

        # add the little wall in the middle
        self.w[14] = 99

        # add the 2 terminals
        self.w[10] = 1
        self.w[16] = -1

    # display the world
    def display(self, A):
        for i in range(self.H):
            for j in range(self.L):
                if self.w[i * self.L + j] == -0.04:
                    stdout.write('-0.04\t')
                elif self.w[i * self.L + j] == 99:
                    stdout.write('W\t')
                elif self.w[i*self.L+j] == 1:
                    stdout.write('+1\t')
                elif self.w[i*self.L+j] == -1:
                    stdout.write('-1\t')
                elif self.w[i*self.L+j] == 0:
                    stdout.write('\t')
                elif self.w[i*self.L+j] in A:
                    stdout.write(self.w[i*self.L+j]+'\t')
                else:

                    stdout.write('%+-.2f\t' % self.w[i*self.L+j])

            print('')


def calculateSum0(w, i, j, action):
    # calculate sum0
    wall = 99
    # action = w
    if action == '^':
        if w.w[i*w.L+j-w.L] == wall:  # wall to up
            u0 = w.w[i*w.L+j]
        else:
            u0 = w.w[i*w.L+j-w.L]
        if w.w[i*w.L+j+1] == wall:  # wall to right
            u1 = w.w[i*w.L+j]
        else:
            u1 = w.w[i*w.L+j+1]
        if w.w[i*w.L+j-1] == wall:  # wall to left
            u2 = w.w[i*w.L+j]
        else:
            u2 = w.w[i*w.L+j-1]
        sum0 = 0.8 * u0 + 0.1*u1+0.1*u2
        return sum0
    # action = a
    if action == '<':
        if w.w[i*w.L+j-1] == wall:  # wall to left
            u0 = w.w[i*w.L+j]
        else:
            u0 = w.w[i*w.L+j-1]
        if w.w[i*w.L+j+w.L] == wall:  # wall to down
            u1 = w.w[i*w.L+j]
        else:
            u1 = w.w[i*w.L+w.L]
        if w.w[i*w.L+j-w.L] == wall:  # wall to up
            u2 = w.w[i*w.L+j]
        else:
            u2 = w.w[i*w.L+j-w.L]
        sum0 = 0.8 * u0 + 0.1*u1+0.1*u2
        return sum0
    # action = s
    if action == 'v':
        if w.w[i*w.L+j+w.L] == wall:  # wall to down
            u0 = w.w[i*w.L+j]
        else:
            u0 = w.w[i*w.L+j+w.L]
        if w.w[i*w.L+j+1] == wall:  # wall to right
            u1 = w.w[i*w.L+j]
        else:
            u1 = w.w[i*w.L+1]
        if w.w[i*w.L+j-1] == wall:  # wall to left
            u2 = w.w[i*w.L+j]
        else:
            u2 = w.w[i*w.L+j-1]
        sum0 = 0.8 * u0 + 0.1*u1+0.1*u2
        return sum0
    # action =d
    if action == '>':
        if w.w[i*w.L+j+1] == wall:  # wall to right
            u0 = w.w[i*w.L+j]
        else:
            u0 = w.w[i*w.L+j+1]
        if w.w[i*w.L+j-w.L] == wall:  # wall to up
            u1 = w.w[i*w.L+j]
        else:
            u1 = w.w[i*w.L-w.L]
        if w.w[i*w.L+j+w.L] == wall:  # wall to down
            u2 = w.w[i*w.L+j]
        else:
            u2 = w.w[i*w.L+j+w.L]
        sum0 = 0.8 * u0 + 0.1*u1+0.1*u2
        return sum0
    else:
        return 999


def goalArrived(eps, gamma, U0, U1):
    for t1 in range(U0.H):
        for t2 in range(U0.L):
            if U1.w[t1*U1.L+t2] != U0.w[t1*U0.L+t2]:
                return False
    return True


def initialisation():
    A = ["^", "<", "v", ">"]
    print("------------")
    w = world(6, 5)
    print("Initial world:\n")
    w.display(A)

    U0 = world(6, 5)
    for i in range(U0.H):
        for j in range(U0.L):
            if U0.w[i*U0.L+j] != 99:
                U0.w[i*U0.L+j] = np.random.choice(A)
    print("Initial U0: \n")

    U0.display(A)
    U1 = world(6, 5)
    for i1 in range(U1.H):
        for j1 in range(U1.L):
            if U1.w[i1*U1.L+j1] != 99:
                U1.w[i1*U1.L+j1] = U0.w[i1*U1.L+j1]
    print("Initial U1: \n")
    U1.display(A)

    U2 = world(6, 5)
    for i2 in range(U2.H):
        for j2 in range(U2.L):
            if U2.w[i2*U2.L+j2] != 99:
                U2.w[i2*U2.L+j2] = 0
    print("Initial U2: \n")
    U2.display(A)
    print("\n")
    return w, U0, U1, U2


print("------------\nQuestion 3. Police iteration\n")
eps = 0.01
gamma = 0.99
A = ["^", "<", "v", ">"]
counter = 0
w, U0, U1, U2 = initialisation()


while ((goalArrived(eps, gamma, U0, U1) == False) or (counter == 0)) and (counter < 50):
    # U0 <- U1
    for i in range(w.H):
        for j in range(w.L):
            if w.w[i*w.L+j] != 99:  # if it is not wall
                U0.w[i*U0.L+j] = U1.w[i*U1.L+j]
    print("U0 before compute U2:\n")
    U0.display(A)
    for k in range(w.H):
        for l in range(w.L):
            if w.w[k*w.L+l] != 99:  # if it is not wall
                # compute U^pi
                U2.w[k*U2.L+l] = w.w[k*w.L+l] + gamma * \
                    calculateSum0(w, k, l, U0.w[k*U0.L+l])
    print("U2 after compute U^pi: \n")
    U2.display(A)
    # update U1
    for i2 in range(U1.H):
        for j2 in range(U1.L):
            if w.w[i2*w.L+j2] != 99:  # if it is not wall
                temp = []
                if U2.w[i2*U2.L+j2-U2.L] != 99:
                    temp.append(U2.w[i2*U2.L+j2-U2.L])  # up
                else:
                    temp.append(-999)
                if U2.w[i2*U2.L+j2+U2.L] != 99:
                    temp.append(U2.w[i2*U2.L+j2+U2.L])  # down
                else:
                    temp.append(-999)
                if U2.w[i2*U2.L+j2-1] != 99:
                    temp.append(U2.w[i2*U2.L+j2-1])  # left
                else:
                    temp.append(-999)
                if U2.w[i2*U2.L+j2+1] != 99:
                    temp.append(U2.w[i2*U2.L+j2+1])  # right
                else:
                    temp.append(-999)
                print("temp: ", temp)
                max_temp = max(temp)
                print("max_temp: ", max_temp)
                id_max_temp = temp.index(max_temp)
                if id_max_temp == 0:  # up
                    U1.w[i2*U1.L+j2] = "^"
                elif id_max_temp == 1:  # down
                    U1.w[i2*U1.L+j2] = "v"
                elif id_max_temp == 2:  # left
                    U1.w[i2*U1.L+j2] = "<"
                elif id_max_temp == 3:  # right
                    U1.w[i2*U1.L+j2] = ">"
    print("U1 after update of U1: \n")
    U1.display(A)
    counter = counter + 1


print("------------\n")
print("The world after the convergence of value interation: \n")
U1.display(A)
print("number of iterations: ", counter)
