import numpy as np
import random
from tkinter import Tk, Canvas
#Importation des bibliothèques utiles au TD
# Initialisation du graph sur lequel on va travailler
graph = [[2, 7, 3], [3, 4, 9, 10], [5, 8, 0], [10, 1, 4, 6, 0], 
         [3, 1, 6], [2], [3, 10, 4], [0], [2], [10, 1], [3, 1, 6, 9]]
#Un pas de temps de 1.
DeltaT=1
# Dimensions de la fenêtre
WIDTH= 800
HEIGHT= 800
# Création de la fenêtre
root = Tk()
root.title("Dessin du graph")
# Création du Canvas
canvas = Canvas(root, width=WIDTH, height=HEIGHT, background="white")
canvas.grid(row=0, column=0)
 

# Initialisation des positions aléatoires et vitesses aléatoires
pos = np.array([(random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50)) 
                for i in range(len(graph))])
vit = np.array([((random.random()-0.5)*10, (random.random()-0.5)*10) 
       for i in range(len(graph))])

#Fonction permettant de dessiner le graphique
def draw(can, graph, pos):
    can.delete("all")

    for i in range(len(graph)):
        for j in graph[i]:  
            can.create_line(pos[i][0], pos[i][1], pos[j][0], pos[j][1], fill="#ea0c0c")
    for (x, y) in pos:
        can.create_oval(x-15,y-15,x+15,y+15,fill="#ea0c0c")
    for i in range(len(graph)):
        for j in graph[i]:  
            can.create_text(pos[i][0],pos[i][1],text=str(i),fill="#ffffff")
    
#Fonction modélisant la force de rappel élastique entre deux points 
def Force(p1,p2):
    x1=pos[p1][0]
    y1=pos[p1][1]
    x2=pos[p2][0]
    y2=pos[p2][1]
    k=0.01
    l0=100
    l=((x1-x2)**2+(y1-y2)**2)**0.5
    u=np.array([(x1-x2)/l,(y1-y2)/l])
    F=k*(l0-l)*u
    return(F)
         
#Fonction modélisant la force de répulsion entre 2 points pour pas qu'ils se superposent
def repulsion(p1,p2):
    x1=pos[p1][0]
    y1=pos[p1][1]
    x2=pos[p2][0]
    y2=pos[p2][1]
    krepulsion=100
    l=((x1-x2)**2+(y1-y2)**2)**0.5
    if l<100:
        u=np.array([(x1-x2)/l,(y1-y2)/l])
        F=(krepulsion)*u/l
        return(F)
    return(0)
#Pour calculer la somme des forces pour avoir m*a avec a l'accélération, on considère ici que m=1kg

def Sommeforce(p):
    Somme = np.array([0.0, 0.0])
    for voisin in graph[p]:
        Somme += Force(p, voisin)
        
    for k in range(len(graph)):
        if k!=p:
            Somme+= repulsion(p,k)

    return Somme

#Je rajoute des frottements pour qu'il y ai une stabilisation après un certain temps
frottement = 0.90  # entre 0 (fort amortissement) et 1 (aucun)

#Fonction de calcul des nouvelles vitesses en fonction de la somme de force : m*a
def newvitesse():
    global vit
    ListeFx = []
    ListeFy = []
    for point in range(len(graph)):
        F = Sommeforce(point)
        ListeFx.append(F[0])
        ListeFy.append(F[1])
    
    # Mise à jour de la vitesse avec amortissement
    ListeV = []
    for k in range(len(ListeFx)):
        vx = (vit[k][0] + ListeFx[k] * DeltaT) * frottement
        vy = (vit[k][1] + ListeFy[k] * DeltaT) * frottement
        ListeV.append([vx, vy])
    return ListeV

#Les nouvelles positions après un temps DeltaT
def newposition():
    newpos = pos.copy()
    vit=newvitesse()
    for i in range(len(newpos)):
        newpos[i][0] += vit[i][0] * DeltaT
        newpos[i][1] += vit[i][1] * DeltaT
        
     # Rebond sur les bords horizontaux
        if newpos[i][0] <= 0 or newpos[i][0] >= WIDTH:
            vit[i][0] = -vit[i][0]
            newpos[i][0] = max(0, min(WIDTH, newpos[i][0]))

        # Rebond sur les bords verticaux
        if newpos[i][1] <= 0 or newpos[i][1] >= HEIGHT:
            vit[i][1] = -vit[i][1]
            newpos[i][1] = max(0, min(HEIGHT, newpos[i][1]))
    
     
    return newpos

#La fonction Temps permet de faire passer le temps, pour simuler le mouvement.
def Temps(event):
    global pos, vit
    vit=newvitesse()
    pos=newposition()
    draw(canvas,graph,pos)
    print(vit, pos)
    
root.bind("<f>",Temps)
# Position initiale 
draw(canvas, graph, pos)
root.mainloop()
