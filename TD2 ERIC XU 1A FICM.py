
#Exercice 1: Création de la classe des objets : polynômes ######################################

class Polynomial:
    #On considère que les coefficients sont rangés dans l'ordre croissant des puissances de X.
    #Exemple : [1,2] => 1+2X
    def __init__(self,L):
        self.coeff=L
#On initialise ici un polynôme à l'aide d'une liste L des coefficients associés
#Cette fonction str permet de lire le polynôme, on met en forme le polynôme dans une forme "naturelle"
    def __str__(self):
        L=self.coeff #On récupère ici les coefficients dans une liste, une liste eqt plus facile à manipuler
        ecriture=''
        for k in range(len(L)-1,-1,-1):#Je parcours ici dans le sens décroissant des puissances pour avoir de gauche à droite les termes de puissance croissantes
            if k==0: #Si k=0 cela veut dire que nous avons un terme constant
                if L[k]==0:#Si le coefficient est nul, il ne faut rien mettre
                    ecriture+=''
                elif L[k]<0: #dans le cas où le coefficient est négatif on a une syntaxe différente,il n'y a pas besoin de le + ce qui donnerait quelque chose comme '+-1'
                    ecriture+=str(L[k])
                else:
                    ecriture+='+'+str(L[k])
            elif k==1: #Dans ce cas là, il ne faut pas écrire la puissance car le puissance 1 est implicite
                if L[k]==0:
                    ecriture+=''
                elif L[k]==1:
                    ecriture+='+'+'X'
                elif L[k]<0:
                    if L[k]==-1:
                        ecriture+='-'+'X'
                    else:
                        ecriture+=str(L[k])+'X'
                else:
                    ecriture+='+'+str(L[k])+'X'
#Les disjonctions de cas suivants sont sur le principe les même que ce qui a été vu avant.
            elif L[k]==0:
                ecriture+=''
            elif L[k]==1:
                ecriture+='+'+'X^'+str(k)
            elif L[k]<0:
                if L[k]==-1:
                    ecriture+='-'+'X^'+str(k)
                else:
                    ecriture+=str(L[k])+'X^'+str(k)
            else:
                ecriture+='+'+str(L[k])+'X^'+str(k)
#Ce tête ligne recouvre le cas où une liste vide ou remplie de 0 est donnée pour un polynôme
        if ecriture=='':
            return("0")
            #la ligne en-dessous permet s'enlever un + en trop en premiere position par exemple enlever lorsque l'on a '+2X+2' on écrit plutôt '2X+2'
        Liste=list(ecriture)
        if ecriture[0]=='+':
            Liste.remove('+')


        ecriture=''
        for k in Liste:
            ecriture+=str(k)
            #Le polynôme est reformé ici après avoir été transformer sous forme de liste pour pouvoir faire les opérations plus facilement.
        return(ecriture)


    def __add__(self,p2):

        L1=self.coeff.copy()
        L2=p2.coeff.copy() #je copie les listes pour pas modifier les originales
        minlen=min(len(L1),len(L2))
        L=[0]*minlen
        for k in range(minlen):
            L[k]=L1[k]+L2[k]
#ici j'ai additionné les coefficients terme à terme tant que les degrés sont égaux
        if len(L1)<len(L2):
            L+=L2[minlen:len(L2)+1]
        if len(L1)>len(L2):
            L+=L2[minlen:len(L1)+1]
            #Pour le reste , il suffit de concatener les coefficients des puissances de X à la lite
        return(Polynomial(L))
#Exercice 3 :
    def scalar(self,c):
        L=self.coeff
        Liste=[]
        for k in L:
            Liste.append(k*c)
        return(Polynomial(Liste))
#ici on repasse par une liste pour pouvoir multiplier les coefficients terme à terme par c

#Jeu de tests

assert(str(Polynomial([1,2,3]))=='3X^2+2X+1')
assert(str(Polynomial( []))=="0")
assert(str(Polynomial( [0]))=="0")
assert(str(Polynomial( [1]))=="1")
assert(str(Polynomial([2,0,3]))=="3X^2+2")

#Exercice 2:  ############################################################################
#Je crée ici une nouvelle classe de polynômes correspondant à l'anneau de l'exercice
class PolynomialZ:
    def __init__(self,L,q,n):
        self.q=q
        self.n=n
        self.coefficients=[]
        for k in L:
            self.coefficients.append(k)
#De la meme manière que les polynomes, on initialise ces nouveaux polynomes a l'aide d'une liste

        degmax=len(self.coefficients) -1 #je prends ici le degré du polynôme avec un -1 car la fonction len compte à partir de 0
        nouveauself=self.coefficients[:n:] #je recupére ici les coefficients de degré inférieur à n car eux ne changent pas
#dans cette boucle, chaque terme de puissance supérieure ou égale à n est réduit jusqu'à avoir un terme de puissance inférieur à n
        for k in range(n,degmax+1):
            compteur=0
            p=k
            while p>=n:
                compteur+=1
                p=p-n
            nouveauself[p]+=self.coefficients[k]*(-1)**(compteur)
            #finalement prend le reste de la division euclidienne de tous les coefficients par q
        self.coeff = [i%q for i in nouveauself]

#Exercice 3 Partie 2  ###########################################################################

    # Cette fonction permet de changer d'anneau (changer la valeur de q en r en gardant n constant)
    def rescale(self,r,n):
        L=self.coeff.copy()
        return(PolynomialZ(L,r,n))



#Exercice 4:  ############################################################################
    #la fonction add est la même que la fonction donnée pour la classe des polynomes classiques en ajoutant les parametreeq q et n
    def __add__(self,p2):
        q=self.q
        n=self.n
        L1=self.coeff.copy()
        L2=p2.coeff.copy()
        minlen=min(len(L1),len(L2))
        L=[0]*minlen
        for k in range(minlen):
            L[k]=L1[k]+L2[k]

        if len(L1)<len(L2):
            L+=L2[minlen:len(L2)+1]
        if len(L1)>len(L2):
            L+=L2[minlen:len(L1)+1]
        return(PolynomialZ(L,q,n))


#Exercice 5: #######################################################################################
    def __mul__(self,P2):
        # dans cette fonction le but est d'ecrire une methode pour multiplier les polynomes, j'utilise ici en théorie la formule du produit de cauchy
        q=self.q
        n=self.n
        L1=self.coeff.copy()
        L2=P2.coeff.copy()
        diff = abs(len(L1) - len(L2))
        if len(L1)>len(L2):
            L2.extend([0]*diff)
        if len(L2)>len(L1):
            L1.extend([0]*(diff))
            #les lignes précédentes servent à remplir avec des 0 les listes de sorte à ce qu'elles soient de même longueur et éviter ainsi les messages d'erreur
        N=len(L1)+len(L2)-1
        L=[0]*N
#ici j'applique la formule du produit de cauchy
        for p in range(N):
            c=0

            for k in range(p+1):
                if k<len(L1) and p-k<len(L2): #dans mes tests j'ai un message 'index out of range' j'ai ainsi mis ces conditions au cas où mais elles sont normalement pas utiles
                    c+=L1[k]*L2[p-k]
            L[p]=c
        return(PolynomialZ(L,q,n))


# jeux de test

print(PolynomialZ([36,2,3,4,5,6,7],4,2).coeff)
print(PolynomialZ([4,7,3,1],4,2).coeff)
print((PolynomialZ([36,2,3,4,5,6,7],4,2)+PolynomialZ([4,7,3,1],4,2)).coeff)
print((PolynomialZ([36,2,3,4,5,6,7],4,2)*PolynomialZ([4,7,3,1],4,2)).coeff)
print((PolynomialZ([0],4,2)*PolynomialZ([0],4,2)).coeff)
print((PolynomialZ([],4,2)*PolynomialZ([],4,2)).coeff)






















