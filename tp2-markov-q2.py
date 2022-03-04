# We reuse the codes for TP1 to create the

from random import random
from sys import stdout


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
        self.w = [+0.2 for i in range(L*H)]

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


def calculateSum0(w, i, j):
    sum0 = []
    # calculate sum0
    # action = w
    wall = 99
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
    s0 = 0.8 * u0 + 0.1*u1+0.1*u2
    # action = a
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
    s1 = 0.8 * u0 + 0.1*u1+0.1*u2
    # action = s
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
    s2 = 0.8 * u0 + 0.1*u1+0.1*u2
    # action =d
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
    s3 = 0.8 * u0 + 0.1*u1+0.1*u2
    # construct an array to use max()
    sum0 = [s0, s1, s2, s3]
    # print("sum0:\n")
    # print(sum0)
    id_action = sum0.index(max(sum0))
    return sum0, id_action


def goalArrived(eps, gamma, U0, U1):
    for t1 in range(U0.H):
        for t2 in range(U0.L):
            if abs(U1.w[t1*U1.L+t2]-U0.w[t1*U0.L+t2]) >= (eps*(1-gamma))/gamma:
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
                U0.w[i*U0.L+j] = 0
    # U0.display()
    U1 = world(6, 5)
    for i1 in range(U1.H):
        for j1 in range(U1.L):
            if U1.w[i1*U1.L+j1] != 99:
                U1.w[i1*U1.L+j1] = 0
    # print("Initial U1: \n")
    # U1.display()

    U2 = world(6, 5)
    for i2 in range(U2.H):
        for j2 in range(U2.L):
            if U2.w[i2*U2.L+j2] != 99:
                U2.w[i2*U2.L+j2] = 0

    return w, U0, U1, U2


print("------------\nQuestion 2. Try other rewards\n--> 1. Regular tile with positive rewards.\n")
eps = 0.01
gamma = 0.99
A = ["^", "<", "v", ">"]
counter = 0
w, U0, U1, U2 = initialisation()


while (goalArrived(eps, gamma, U0, U1) == False) or (counter == 0):
    # update the value of each state
    for i in range(w.H):
        for j in range(w.L):
            if w.w[i*w.L+j] != 99:  # if it is not wall
                R = w.w[i*w.L+j]
                while True:
                    sum0 = []
                    sum0, id_action = calculateSum0(U0, i, j)
                    for i1 in range(U0.H):
                        for j1 in range(U0.L):
                            U0.w[i1*U0.L+j1] = U1.w[i1*U1.L+j1]
                    U1.w[i*U1.L+j] = R+gamma*max(sum0)

                    if id_action == 0:
                        U2.w[i*U2.L+j] = "^"
                    elif id_action == 1:
                        U2.w[i*U2.L+j] = "<"
                    elif id_action == 2:
                        U2.w[i*U2.L+j] = "v"
                    elif id_action == 3:
                        U2.w[i*U2.L+j] = ">"
                    print("------------\n")
                    U2.display(A)
                    counter = counter + 1

                    # print("U1", U1.w[i*U1.L+j])
                    # print("U0", U0.w[i*U0.L+j])
                    # print("err", (eps*(1-gamma))/gamma)
                    if abs(U1.w[i*U1.L+j]-U0.w[i*U0.L+j]) < (eps*(1-gamma))/gamma:
                        break
print("------------\n")
print("The world after the convergence of value interation: \n")
U1.display(A)
print("number of iterations: ", counter)
