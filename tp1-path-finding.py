from random import random
from sys import stdout
from termcolor import colored

class world:
    # initialise the world
    # L is the number of columns
    # H is the number of lines
    # P is the probability of having a wall in a given tile
    def __init__(self, L, H, P):
        self.L = L 
        self.H = H

        # the world is represented by an array with one dimension
        self.w = [0 for i in range(L*H)] # initialise every tile to empty (0)

        # add walls in the first and last columns
        for i in range(H):
            self.w[i*L] = 1
            self.w[i*L+L-1] = 1
        
        # add walls in the first and last lines
        for j in range(L):
            self.w[j] = 1
            self.w[(H-1)*L + j] = 1

        for i in range(H):
            for j in range(L):
                # add a wall in this tile with probability P and provided that it is neither
                # the starting tile nor the goal tile 
                if random() < P and not (i == 1 and j == 1) and not (i == H-2 and j == L-2):
                    self.w[i*L+j] = 1

    # display the world
    def display(self, path, path2):
        for i in range(self.H):
            for j in range(self.L):
                if i * self.L + j in path:
                    stdout.write(colored('#', 'red'))
                elif i * self.L + j in path2:
                    stdout.write(colored('#', 'yellow'))
                else:
                    if self.w[i * self.L + j] == 0:
                        stdout.write('.')
                    elif self.w[i * self.L + j] == 1:
                        stdout.write('W')
                
            print('')
    # compute the successors of tile number i in world w
    def successors(self, i):
        if i < 0 or i >= self.L * self.H or self.w[i] == 1:
            # i is an incorrect tile number (outside the array or on a wall)
            return [] 
        else:
            # look in the four adjacent tiles and keep only those with no wall
            return list(filter(lambda x: self.w[x] != 1, [i - 1, i + 1, i - self.L, i + self.L]))

    # Depth-first search
    # starting from tile number s0, find a path to tile number t
    # return (r, path) where r is true if such a path exists, false otherwise
    # and path contains the path if it exists  
    def dfs(self, s0, t):
        r = False
        path = []
        path2 = []
        visited=[]
        waiting=[s0] #DFS -> list, append and pop
        while len(waiting)!=0 and (not r):
            s = waiting.pop()
            if s == t:
                r = True
                path.append(s)
            else:
                visited.append(s)
                for sp in w.successors(s):
                    if sp not in visited and sp not in waiting:
                        if s not in path:
                            path.append(s)
                        waiting.append(sp)
        if r==True:
            path2=[]
        else:
            path2=[]
        return r, path, path2


    # Breadth-first search
    # starting from tile number s0, find a path to tile number t
    # return (r, path) where r is true if such a path exists, false otherwise
    # and path contains the path if it exists  
    def bfs(self, s0, t):
        r = False
        path = []
        visited=[]
        waiting=[s0] #BFS -> queue, append and pop(0)
        while len(waiting)!=0 and (not r):
            s = waiting.pop(0)
            if s == t:
                r = True
                path.append(s)
            else:
                visited.append(s)
                for sp in w.successors(s):
                    if sp not in visited and sp not in waiting:
                        if s not in path:
                            path.append(s)
                        waiting.append(sp)
        return r, path

    # Dijkstra
    def dijkstra(self, s0, t):
        path=[]
        r=False
        cost=[None]*(w.H*w.L-1)
        cost[s0]=0
        for j in range(w.H*w.L-1):
            if j != s0:
                cost[j]=float("inf")
        waiting = []
        waiting.append(s0)
        while not len(waiting)==0 and (not r):
            tmp=[]
            for t2 in waiting:
                tmp.append(cost[t2])

            costmin=min(tmp)
            id_costmin=tmp.index(costmin)
            s=waiting[id_costmin]
            del waiting[id_costmin]
            

            if s==t:
                r=True
                path.append(s)
            else:
                for sp in w.successors(s):
                    if cost[s]+1<=cost[sp]: #the weight between 2 points adjacents is always 1
                        cost[sp]=cost[s]+1
                        if s not in path:
                            path.append(s)
                        if sp not in waiting:
                            waiting.append(sp)
        return r, path, cost

    # A*
    def aStar(self, s0, t):
        path=[]
        r=False
        cost=[None]*(w.H*w.L-1)
        cost[s0]=0+max(t%20-s0%20,t/20-s0/20)
        costbis=[None]*(w.H*w.L-1)
        costbis[s0]=0
        for j in range(w.H*w.L-1):
            if j != s0:
                cost[j]=float("inf")
        waiting = []
        waiting.append(s0)
        while not len(waiting)==0 and (not r):

            tmp=[]
            for t2 in waiting:
                tmp.append(cost[t2])

            costmin=min(tmp)
            id_costmin=tmp.index(costmin)
            s=waiting[id_costmin]
            del waiting[id_costmin]
            

            if s==t:
                r=True
                path.append(s)
            else:
                for sp in w.successors(s):
                    if cost[s]+1<=cost[sp]: #the weight between 2 points adjacents is always 1
                        cost[sp]=cost[s]+1+max(t%20-sp%20,t/20-sp/20)
                        costbis[sp]=costbis[s]+1
                        if s not in path:
                            path.append(s)
                        if sp not in waiting:
                            waiting.append(sp)
        return r, path, costbis
                        
# create a world
w = world(20, 10, 0.2)

# display it 
# w.display()

# print the tile numbers of the successors of the starting tile (1, 1)
# print(w.successors(w.L+1))

# simple DFS
r,path,path2 = w.dfs(w.L+1, 178)
print("Simple DFS. Path exists: ",r,"\nThe result path is colored in red.")
w.display(path,path2)
print("Steps: ",len(path))
# simple BFS
print("--------------------\n")
r,path = w.bfs(w.L+1, 178)
print("Simple BFS. Path exists: ",r,"\nThe result path is colored in red.")
path2=[]
w.display(path,path2)
print("Steps: ",len(path))
# Dijkstra
print("--------------------\n")
r,path,cost = w.dijkstra(w.L+1, 178)
print("Dijkstra. Path exists: ",r,"\nThe result path is colored in red.")
w.display(path,path2)
print("Steps: ",len(path))
print("cost min: ",cost[178])
# aStar
print("--------------------\n")
r,path,cost = w.aStar(w.L+1, 178)
print("A Star. Path exists: ",r,"\nThe result path is colored in red.")
w.display(path,path2)
print("Steps: ",len(path))
print("cost min: ",cost[178])