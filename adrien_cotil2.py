import matplotlib.pyplot as plt
from math import *
import numpy as np
import csv
import copy

ville="grenoble"

def graph(liste):
    plt.plot(range(len(liste)),liste)

def row_count_func(ville):
    with open("/home/adrien/KIRO/"+ville+"/distances.csv") as csv_file:
        csv_reader = csv.reader(csv_file)
        row_count = sum(1 for row in csv_reader)
    csv_file.close()
    return row_count
def parse_dist(ville):
    with open("/home/adrien/KIRO/"+ville+"/distances.csv") as csv_file:
        csv_reader = csv.reader(csv_file)
        row_count=row_count_func(ville)
        nb_nodes=int(sqrt(row_count))
        distances=[[0 for i in range(nb_nodes)] for j in range(nb_nodes)]
        
        liste=[int(row[0]) for row in csv_reader]
        for i in range(nb_nodes):
            for j in range(nb_nodes):
                distances[i][j]=liste[j+i*nb_nodes]
    return distances
    
def parse_nodes(ville):
    nodes=[]
    distribution=[]
    with open("/home/adrien/KIRO/"+ville+"/nodes.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            nodes+=[[row[0],row[1]]]
            distribution.append(row[2]=="distribution")
            
    return nodes[1:],distribution[1:]
      
distances=parse_dist(ville)
nb_nodes=len(distances)
nodes, distribution=parse_nodes(ville)

def result(ville,reseaux):
    file = open("/home/adrien/KIRO/"+ville+"/result.txt","w")
    for reseau in reseaux:
        file.write('b')
        reseau_str=""
        for chaine in reseau:
            reseau_str+=" "+str(chaine[0])
        file.write(reseau_str+"\n")
        for chaine in reseau:
            if len(chaine)>1:
                file.write("c")
                for node in chaine:
                    file.write(" "+str(node))
                file.write("\n")

def cost(reseaux):
    c=0
    
    for reseau in reseaux:
        for i in range(len(reseau)):
            c+=distances[reseau[i][0]][reseau[(i+1)%len(reseau)][0]]
            if len(reseau[i])>1:
                for j in range(len(reseau[i])-1):
                    c+=distances[reseau[i][j]][reseau[i][j+1]]
            
    return c

def init_reseaux():
    return [[[i]] for i in range(sum(distribution))]

def valid_reseaux(reseaux):
    valid=True
    hist=[0 for i in range(nb_nodes)]
    for r in reseaux:
        for c in r:
            for k in c:
                hist[k]+=1
    for i in hist:
        if i>1:
            valid=False
            break
    return valid
            
reseaux=init_reseaux()
print(cost(reseaux))

def evolve(reseaux,node):
    R=copy.deepcopy(reseaux)
    optR=copy.deepcopy(R)
    m=float('inf')
        
    for i_r in range(len(reseaux)):
        R=copy.deepcopy(reseaux)
        for i in range(len(R[i_r])):
            if len(R[i_r][i])<=5:
                for j in range(distribution[R[i_r][i][0]],len(R[i_r][i])+1):
                    R[i_r][i]=R[i_r][i][:j]+[node]+R[i_r][i][j:]
                    C=cost(R)
                    if C<m and valid_reseaux(R):
                        m=C
                        optR=copy.deepcopy(R)
                    R=copy.deepcopy(reseaux)
        
        if len(R[i_r])<=30:
            for j in range(len(R[i_r])):
                R[i_r]=R[i_r][:j+1]+[[node]]+R[i_r][j+1:]
                C=cost(R)
                if C<m and valid_reseaux(R):
                    m=C
                    optR=copy.deepcopy(R)
                R=copy.deepcopy(reseaux)
    
    for i_pd in range(sum(distribution)):
        
        R=R+[[[i_pd,node]]]
    
        C=cost(R)
        if C<m and valid_reseaux(R):
            m=C
            optR=copy.deepcopy(R)
            R=copy.deepcopy(reseaux)
        R=copy.deepcopy(reseaux)
    return optR

def delete(reseaux,node):
    for reseau in reseaux:
        for chaine in reseau:
            if node!=chaine[0]:
                if node in chaine:
                    chaine.remove(node)
                
def find(reseaux_ini):
    reseaux=copy.deepcopy(reseaux_ini)
    m=float('inf')
    
    for i in range(100):
        reseaux=copy.deepcopy(reseaux_ini)
        c=cost(reseaux)+1
        while cost(reseaux)!=c:
            c=cost(reseaux)
            nodes_permut=np.random.permutation([i for i in range(sum(distribution),nb_nodes)])
            for node in nodes_permut:
                delete(reseaux, node)
                reseaux=evolve(reseaux,node)
            
                
        
        C=cost(reseaux)
        if C<m and valid_reseaux(reseaux):
            m=C
            opt_reseaux=copy.deepcopy(reseaux)
            result(ville,opt_reseaux)
            print(m)
           
    
    return(opt_reseaux)
R=find(reseaux)
print("coût final = ",cost(R))