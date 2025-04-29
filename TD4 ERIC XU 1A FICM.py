        
#Exercice 1: 
#Fonction de hachage : somme des codes ASCII des caractères
h = lambda x: sum([ord(c) for c in x])
#######################################################################################################################
#Création de classe d'objets :"Dictionnaire"
class Hashtable:
    #Méthode permettant d'initialiser la tablec à partir d'une fonction de hachage et de la taille de la table N'
    def __init__(self,hash,N):
        self.hash=hash
        L=[None]*N
        self.table=L
        self.N=N
        self.nb_elements=len(L)
        #On définit ici les variables pour retrouver les caractéristiques importantes des tables
#######################################################################################################################
    #Méthode permettant d'ajouter dans le dictionnaire
    def put(self,key,value):
        Table=self.table
        hash=self.hash
        N=self.N
        index=hash(key)%N
        #Dans toutes les méthodes, il y a ces premières lignes qui permettent de récupérer les données de la table.

        if Table[index]==None: #Si le couple n'est pas encore dans la table, on l'ajoute. ( Le dictionnaire est rempli de None à l'initialisation.
            Table[index]=[(key,value)]
            return

        Collisionkeys=[]
        for k in Table[index]:
            Collisionkeys.append(k[0])

#Cette partie permet d'ajouter le couple (clé,valeur) s'il n'est pas déjà dans la table et s'il y a collision
        if key not in Collisionkeys:
            Table[index].append((key,value))
            return
#S'il y a collision et que la clé est déjà dans la table, on lui modifie sa valeur
        else:
            for k in range(len(Collisionkeys)):
                if Collisionkeys[k]==key:
                    Table[index][k][1]=value
#######################################################################################################################
    #Méthode permettant d'obtenir la valeur en donnant en paramètre la clé

    def get(self,key):
        Table=self.table
        hash=self.hash
        N=self.N
        index=hash(key)%N
#Si la case est vide :
        if Table[index]==None:
            return(None)
        else:
            #Sinon on cherche la valeur associée (on prend en compte le cas où on a collision)
            for k in Table[index]:
                if k[0]==key:
                    return(k[1])
#######################################################################################################################
    #Méthode permettant d'avoir un graphique montrant le nombre de collisions dans une table.
    def repartition(self):
        import matplotlib.pyplot as plt
        Table=self.table
        N=self.N
        y=[0]*N
        for k in range(N):
            if Table[k]==None:
                y[k]=0
            else:
                y[k]=len(Table[k])
        x=range(N)
        width = 1/1.5
        plt.bar(x, y, width, color="blue")
        plt.show()
#######################################################################################################################
#Exercice 6:
    #Méthode permettant de redimensionner une table, en réinsérant aux bons emplacements les différents éléments
    def resize(self):
        Table=self.table
        hash=self.hash
        N=self.N
#On créer ici les nouveaux paramètres, on a décidé de doubler la taille du dictionnaire, et on garde la même fonction de hashage.
        NewN=2*N
        NewTable=Hashtable(hash,NewN)
        Donnees=[]
        #On récupère ici toutes les données pour pouvoir les ré-insérer après.
        for k in Table:
            if k!=None:
                for p in k:
                    Donnees.append(p)

            #On rajoute les données à leurs bonnes cases.
        for k in Donnees:
            NewTable.put(k[0],k[1])

        #Et finalement, on ne créer pas de nouvelles tables, on garde la même, on la modifie seulement.
        self.table = NewTable.table
        self.N = NewTable.N
        self.nb_elements = NewTable.nb_elements
#######################################################################################################################
    #Méthode permettant d'ajouter un couple (clé, valeur) en redimensionnant si besoin lorsque la table est suffisamment remplie avec resize

    def put2(self,key,value):
        N=self.N
        if self.nb_elements>=1.2*N:
            self.resize()
#Cette méthode est exactement la même que put, seulement ici on met une condition supplémentaire, si le nombre d'éléments est supérieur à 1.2*N, on double la taille du tableau.
        Table=self.table
        hash=self.hash
        N=self.N

        index=hash(key)%N
        if Table[index]==None:
            Table[index]=[(key,value)]
            self.nb_elements+=1
            return

        Collisionkeys=[]
        for k in Table[index]:
            Collisionkeys.append(k[0])

        if key not in Collisionkeys:
            Table[index].append((key,value))
            self.nb_elements+=1
            return

        else:
            for k in range(len(Collisionkeys)):
                if Collisionkeys[k]==key:
                    Table[index][k][1]=value


#######################################################################################################################



#Exercice 5


liste=[]
# Ouverture du fichier dictionnaire français
f = open("/Users/erixxu/Desktop/Python Mines/26 mars/frenchssaccent.dic",'r')
for ligne in f:
    liste.append(ligne[0:len(ligne)-1])
f.close()
     # Fermeture du fichier

dictionnaire=liste # Copie de la liste dans une autre liste nommée dictionnaire pour mieux  comprendre.


def repartitiondictionnaire():

    H=Hashtable(h,10000)
    for k in dictionnaire:
        H.put(k,len(k))
    H.repartition()
#######################################################################################################################
import time
#Fonction permettant de mesurer le temps moyen de la fonction put2 et get pour vérifier qu'on a bien du temps constant.
def Temps(N):
    H=Hashtable(h,10)
    Listetempsput=[]
    Listetempsget=[]
    for k in range(N):
        debut=time.perf_counter()
        H.put2(str(k),1) #J'ajoute ici str(k) pour ajouter à chaque fois des clés différentes
        fin=time.perf_counter()
        tempsput=fin-debut
        debut=time.perf_counter()
        H.get(str(k))
        fin=time.perf_counter()
        tempsget=fin-debut
        Listetempsput.append(tempsput)
        Listetempsget.append(tempsget)
    tempsmoyenput=0
    tempsmoyenget=0
    for k in range(len(Listetempsput)):
        tempsmoyenput+=Listetempsput[k]
        tempsmoyenget+=Listetempsget[k]
    tempsmoyenput=tempsmoyenput/(len(Listetempsput))
    tempsmoyenget=tempsmoyenget/(len(Listetempsput))
    print("Le temps du put est :", tempsmoyenput)
    print("Le temps du get est :", tempsmoyenget)

#######################################################################################################################
#######################################################################################################################


















