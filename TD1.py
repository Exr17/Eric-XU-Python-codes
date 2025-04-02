liste=[]
# Ouverture du fichier dictionnaire français
f = open("frenchssaccent.dic",'r')
for ligne in f:
    liste.append(ligne[0:len(ligne)-1])
f.close()
# Fermeture du fichier

dictionnaire=liste # Copie de la liste dans une autre liste nommée dictionnaire pour mieux comprendre.

#Exercice 2
# Fonction pour trouver les mots faisables et le plus long
def f(tirage):
    Mots=[]# Liste pour stocker les mots faisables
    # Parcours de tous les mots du dictionnaire
    for i in range(len(dictionnaire)):
          # Vérification si le mot peut être formé avec le tirage
        if Test(tirage,dictionnaire[i])==True:
             # Ajout du mot si le test donne un mot valide
            Mots.append(dictionnaire[i])

# Recherche du mot le plus long
    max=Mots[0]  # Initialisation avec le premier mot
    for k in Mots:
        if len(k)>len(max):
            max=k#On met à jour la variable max à chaque fois qu'on a un mot plus long.
    return(Mots,max)  #La fonction renvoie la liste de Mots ainsi que le plus long.

# Fonction pour vérifier si un mot peut être formé avec un tirage

def Test(Tirage,Mot):
    L=Tirage.copy() # Je vais ici un .copy() pour ne pas modifier la liste Tirage lorsque je modifie L
     # En testant sur toutes les lettres du mot.
    for k in Mot:
        if k not in L:
            return(False)# Lettre non valide
        L.remove(k) # J'enlève la lettre utilisée
    return(True)

######### Exercice 3
#La structure adaptée est celle du dictionnaire qui permet d'attribuer une valeur à une clé qui est ici une lettre
# Dictionnaire avec le score associé à chaque lettre
D=dict()
D["a"]=1
D["e"]=1
D["i"]=1
D["l"]=1
D["n"]=1
D["o"]=1
D["r"]=1
D["s"]=1
D["t"]=1
D["u"]=1
D["d"]=2
D["g"]=2
D["m"]=2
D["b"]=3
D["c"]=3
D["p"]=3
D["f"]=4
D["h"]=4
D["v"]=4
D["j"]=8
D["q"]=8
D["k"]=10
D["w"]=10
D["x"]=10
D["y"]=10
D["z"]=10
# Fonction pour calculer le score d'un mot
def score(mot):
    S=0# Initialisation du score
      # Calcul du score lettre par lettre
    for k in mot:
        S+=D[k] # Ajout de la valeur de chaque lettre
    return(S) # Retourne le score total

# Fonction pour trouver le mot avec le score le plus élevé
def max_score(L):
    Smax=0 # J'initialise la variable
    S=0 # J'initialise aussi la variable
    mot="test"  # Mot initial (arbitraire)
        # On regarde tous les mots
    for k in range(len(L)):
        S=score(L[k])# On calcule le score du mot
          # On met à jour si le score est supérieur à Smax
        if Smax<S:
            Smax=S
            mot=L[k]
    return(mot,Smax)# La fonction retourne le meilleur mot et son score



# Fonction améliorée pour trouver le meilleur mot en prenant en compte le score

def fameliore(tirage):
    Mots=[] # Liste des mots faisables
        # Parcours du dictionnaire
    for i in range(len(dictionnaire)):
        if Test(tirage,dictionnaire[i])==True:
            Mots.append(dictionnaire[i])# On ajoute les mots valides
    return(max_score(Mots))# Retourne le meilleur mot et son score

######################## Exercice 4:
# Ajout du joker avec valeur 0
D["?"]=0

# Fonction pour trouver le meilleur mot avec joker
def max_score2(L,Tirage):
    Smax=0 #Initialisation du score max
    S=0  # Initialisation du score
    mot=L[0] # Mot initial (arbitraire aussi)
    for k in range(len(L)):
        Lettrejoker=0# Initialisation de la Lettre remplacée par le joker
        Lmot=list(L)# Conversion en liste

        # Calcul du score
        S=score(Lmot[k])
         # Recherche de la lettre manquante
        for p in Lmot[k]:
            if p not in Tirage:
                Lettrejoker=p
        S=S-D[Lettrejoker] # Ajustement du score

         # Comparaison des scores, recherche du max
        for i in mot:
            if Smax<S:
                Smax=S
                mot=Lmot[k]
    return(mot,Smax)

# Fonction de test améliorée en prenant en compte le joker
def Test2(Tirage,Mot):
      # Cas sans joker
    if '?' not in Tirage:
        return(Test(Tirage,Mot))
    L=Tirage.copy()
    comptage=0
    for k in Mot:

        if k in L:
            L.remove(k) # On retire les lettres qui marchent
        else:
            comptage+=1# On ajoute 1 si une lettre est manquante
             # On autorise une seule et unique lettre manquante (remplacée par le joker)
    if comptage<=1:
        return(True)
    return(False)

# Fonction principale en prenant en compte le joker
def f2(tirage):
    L=list(tirage)# Conversion en liste
    Mots=[] #Liste des mots faisbles
       # Parcours du dictionnaire
    for i in range(len(dictionnaire)):
        if Test2(L,dictionnaire[i])==True:
            Mots.append(dictionnaire[i]) # Ajout des mots valides
    return(Mots)     # Retourne la liste des mots faisables








