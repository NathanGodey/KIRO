import matplotlib.pyplot as plt
from math import *
import numpy as np
import csv
import random as rd
import copy

ville="nice"

#Fonction qui plot une suite numérique
def graph(liste):
    plt.plot(range(len(liste)),liste)

#fonction qui parse le nombre de lignes du fichier txt
def row_count_func(ville):
    with open(ville+"\\distances.csv") as csv_file:
        csv_reader = csv.reader(csv_file)
        row_count = sum(1 for row in csv_reader)
    csv_file.close()
    return row_count

#fonction qui renvoie la matrice des distances entre la ville i et la ville j
def parse_dist(ville):
    with open(ville+"\\distances.csv") as csv_file:
        csv_reader = csv.reader(csv_file)
        row_count=row_count_func(ville)
        nb_nodes=int(sqrt(row_count))
        distances=[[0 for i in range(nb_nodes)] for j in range(nb_nodes)]
        
        liste=[int(row[0]) for row in csv_reader]
        for i in range(nb_nodes):
            for j in range(nb_nodes):
                distances[i][j]=liste[j+i*nb_nodes]
    return distances

#fonction qui renvoie les coordonnées des nodes et une liste de booleens
def parse_nodes(ville):
    nodes=[]
    distribution=[]
    with open(ville+"\\nodes.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')
        for row in csv_reader:
            nodes+=[[row[0],row[1]]]
            distribution.append(row[2]=="distribution")
            
    return nodes[1:],distribution[1:]

#Matrice des distances  
distances=parse_dist(ville)

#Le nombre de noeuds
nb_nodes=len(distances)

#La liste des coordonnées des noeuds et un liste de booléens
#indiquant si le i_ème élément est une distribution
nodes, distribution=parse_nodes(ville)





#reseaux est une liste de reseau

#un reseau est une liste de chaines dont les premiers éléments forment
#une boucle

#une chaine est une suite de noeuds, le n_ème noeud étant relié au n+1_ème


#Fonction qui construit le fichier result sous la forme demandée
def result(ville,reseaux):
    file = open(ville+"\\result.txt","w")
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

#Fonction calculant le cout d'une architecture
def cost(reseaux):
    c=0
    for reseau in reseaux:
        for i in range(len(reseau)):
            c+=distances[reseau[i][0]][reseau[(i+1)%len(reseau)][0]]
            if len(reseau[i])>1:   #si une chaine est issue du noeud
                for j in range(len(reseau[i])-1):
                    c+=distances[reseau[i][j]][reseau[i][j+1]]
    return c

#Initialisation d'un réseau ou tous les points de distribution sont
#utilisés une et une seule fois
def init_reseaux():
    return [[[i]] for i in range(sum(distribution))]

#fonction qui teste qu'une architecture est bien valide
def valid_reseaux(reseaux):
    valid=True
    hist=[0 for i in range(nb_nodes)]
    for reseau in reseaux:
        for chain in reseau:
            for node in chain:
                hist[node]+=1
                if hist[node]>1:
                    valid=False
                    break
    return valid

#Initialisation d'une architecture naive   
reseaux=init_reseaux()


#Fonction qui insère le noeud node dans l'architecture reseaux de manière à
#minimiser le coût
def evolve(reseaux,node):
    optimal_reseaux=copy.deepcopy(reseaux)
    minC=float('inf')
    for i_r in range(len(reseaux)):
        
        #On essaie de le mettre dans une chaine existante dans un reseau
        temp_reseaux=copy.deepcopy(reseaux)
        for i in range(len(temp_reseaux[i_r])):
            current_chain=temp_reseaux[i_r][i][:]
            if len(temp_reseaux[i_r][i])<=5:
                for j in range(len(temp_reseaux[i_r][i])):
                    current_chain=current_chain[:j+1]+[node]+current_chain[j+1:]
                    temp_reseaux[i_r][i]=current_chain[:]
                    C=cost(temp_reseaux)
                    if C<minC and valid_reseaux(temp_reseaux):
                        minC=C
                        optimal_reseaux=copy.deepcopy(temp_reseaux)
                    temp_reseaux=copy.deepcopy(reseaux)
        
        #On essaie de le mettre dans une boucle d'un reseau en tête d'une
        #éventuelle future chaîne
        if len(temp_reseaux[i_r])<=30:
            for j in range(len(temp_reseaux[i_r])):
                temp_reseaux[i_r]=temp_reseaux[i_r][:j+1]+[[node]]+temp_reseaux[i_r][j+1:]
                C=cost(temp_reseaux)
                if C<minC and valid_reseaux(temp_reseaux):
                    minC=C
                    optimal_reseaux=copy.deepcopy(temp_reseaux)
                temp_reseaux=copy.deepcopy(reseaux)
        for i_pd in range(sum(distribution)):
            temp_reseaux=copy.deepcopy(reseaux)
            temp_reseaux.append([[i_pd,node]])
            C=cost(temp_reseaux)
            if C<minC and valid_reseaux(temp_reseaux):
                minC=C
                optimal_reseaux=copy.deepcopy(temp_reseaux)
            temp_reseaux=copy.deepcopy(reseaux)
    return optimal_reseaux

# On supprime le noeud node du réseau et on indique si la deletion s'est bien
#passée
def delete(reseaux,node):
    for reseau in reseaux:
        for chaine in reseau:
            if node!=chaine[0]:
                if node in chaine:
                    chaine.remove(node)
                    return True
            return False

def plot_city(reseaux):
    print(cost(reseaux))
    for reseau in reseaux:
        X=[]
        Y=[]
        for chain in reseau:
            x=[]
            y=[]
            for node in chain:
                if distribution[node]:
                    plt.plot([float(nodes[node][0])],[float(nodes[node][1])],c="g",marker="o")
                x.append(float(nodes[node][0]))
                y.append(float(nodes[node][1]))
            plt.plot(x,y,c="r")
            X.append(x[0])
            Y.append(y[0])
        plt.plot(X+[X[0]],Y+[Y[0]],c="b")
    plt.show()
        
def find(reseaux_ini):
    reseaux=copy.deepcopy(reseaux_ini)
    #on crée le premier réseau sous-optimal
    for node in range(sum(distribution),nb_nodes):
        
        reseaux=evolve(reseaux,node)
    plot_city(reseaux)
    for i in range(15):
        for node in range(sum(distribution),nb_nodes):
            delete(reseaux, node)
            reseaux=evolve(reseaux,node)
            result(ville,reseaux)
        plot_city(reseaux)
    stationary=0
    while stationary<1:
        node=rd.randint(sum(distribution),nb_nodes-1)
        delete(reseaux, node)
        next_reseaux=evolve(reseaux,node)
        stationary+=0.2*(1-2*(np.array(reseaux).all()==np.array(next_reseaux).all()))
        reseaux=copy.deepcopy(next_reseaux)
        # plot_city(reseaux)
        print(cost(reseaux))
        result(ville,reseaux)
    return reseaux
    
R=find(reseaux)
