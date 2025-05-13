#TD6: Entrelacs, Le JEU.
from tkinter import Tk, Canvas, Button, Label  # Importation des composants Tkinter pour l'interface graphique
from random import randint  # Pour générer des entiers aléatoires

# Liste de couleurs utilisables pour les fils
couleurs= [
    "red",        # Rouge
    "green",      # Vert
    "blue",       # Bleu
    "yellow",     # Jaune
    "cyan",       # Cyan
    "magenta",    # Magenta
    "black",      # Noir
    "gray",       # Gris (ou "grey")
    "lightgray",  # Gris clair (ou "lightgrey")
    "darkgray",   # Gris foncé (ou "darkgrey")
    "orange",     # Orange
    "purple",     # Violet
    "pink",       # Rose
    "brown",      # Marron
    "gold",       # Or
    "silver",     # Argent
    "lime",       # Vert clair (citron)
    "navy",       # Bleu marine
    "maroon"      # Bordeaux
]


class Data:  # Classe qui stocke les données nécessaires pour générer les entrelacs

    def __init__(self, nb_fils, croisements):
        self.nbfils=nb_fils
        self.croisement=croisements

    def liste_mots(self):  # Méthode pour transformer la liste de croisements en chemins "mots"
        croisement=self.croisement
        nb_fils=self.nbfils
        Listedespositions=[k for k in range(nb_fils)]  # Représente les positions actuelles des fils
        Mots=['']*nb_fils  # Initialisation des "mots" pour chaque fil

        # Construction des mots à partir des croisements
        for l in self.croisement:
            for j in range(nb_fils):
                if j==l+1:
                    Mots[Listedespositions[j]]+='HU'  # Le fil monte
                elif j==l:
                    Mots[Listedespositions[j]]+='HD'  # Le fil descend
                else:
                    Mots[Listedespositions[j]]+='HH'  # Le fil reste droit
            Listedespositions[l],Listedespositions[l+1]=Listedespositions[l+1],Listedespositions[l]  # Échange des positions des fils croisés
        return(Mots)

    def hasard(self):  # Génère aléatoirement un nouveau nombre de fils et une nouvelle liste de croisements
        newcroisement=[]
        newnb_fils=randint(2,8)  # Choix aléatoire du nombre de fils entre 2 et 8
        for k in range(newnb_fils):
            newcroisement.append(randint(0,newnb_fils-2))  # Ajoute des croisements valides

        self.nbfils=newnb_fils
        self.croisement=newcroisement
        App.self.redraw()  #Ici j'ai ajouté cette ligne pour que quand j'appuye sur "Aléatoire", le nouvel entrelac s'affiche mais ça ne marche pas. À chaque fois pour voir le nouvel entrelac il faut appuyer sur le bouton Color'


class App:   # Classe qui gère l'interface graphique
    def __init__(self,data,couleurs):
        self.data=data
        self.root = Tk()
        self.canvas = Canvas(self.root, width=60*(len(self.data.croisement))*2+2, height=max(200,(self.data.nbfils)*60+40), background="white")  # La taille du Canvas est choisie par rapport au nombre et la longueur des fils
        self.canvas.grid(column =0, row =0,columnspan=5)
        self.couleurs=couleurs
        self.redraw()  # Appel initial pour dessiner les fils

    def run_forever(self):
        self.root.mainloop()


    def redraw(self):  # Fonction pour redessiner tout le canevas à partir des données actuelles
        canvas=self.canvas
        canvas.delete("all")  # Efface le canevas pour redessiner proprement
        couleurs=self.couleurs
        data=self.data
        Mots=data.liste_mots()
        self.root.update()  # Mise à jour de l'affichage


        # Boucle pour tracer chaque fil selon son "mot"
        for num_fil in range(len(Mots)):
            self.read_word(Mots[num_fil]+'H', 55,55,0,20+num_fil*55, couleurs[num_fil] )

        # Création du bouton "Quit"
        Quit = Button(self.root,text="Quit", command=self.quitter)
        Quit.grid(row=2,column=1)

        # Création du bouton "Color"
        ColorButton = Button(self.root,text="Color", command=self.recolorer)
        ColorButton.grid(row=2,column=2 )

        # Affichage de la liste des croisements
        Infoentrelacs =Label(self.root,text="Croisements:"+str(self.data.croisement))
        Infoentrelacs.grid(row=1,column=1)

        # Bouton "Aléatoire" pour générer un entrelacs aléatoire
        Aleatoire = Button(self.root,text="Aleatoire", command=self.data.hasard)
        Aleatoire.grid(row=2,column=3)


    def read_word(self, mot, h, w, departx, departy,color):  # Fonction pour lire un mot et dessiner la ligne correspondante
        canvas=self.canvas
        x=departx
        y=departy
        # Pour chaque lettre du mot, on trace une ligne selon la direction indiquée
        for k in mot:
            if k=='H':
                canvas.create_line(x,y,x+w,y, fill=str(color))  # Trait horizontal
                x=x+h
            if k=='U':
                canvas.create_line(x,y,x+w,y-h, fill=str(color))  # Trait montant
                x=x+w
                y=y-h
            if k=='D':
                canvas.create_line(x,y,x+w,y+h, fill=str(color))  # Trait descendant
                x=x+w
                y=y+h


    def quitter(self):  # Fonction appelée pour quitter le programme
        self.root.destroy()
        print("La page a été fermée") #Je ne sais pas pourquoi sur Mac la commande self.root.destroy() ne marche pas. Ou partiellement, si je lance le programme deux fois, le bouton quitter marche sur la deuxième fenêtre mais pas sur la première 

    def recolorer(self):  # Fonction pour modifier les couleurs (permutation circulaire)
        Newcolor=self.couleurs.copy()
        for k in range(len(Newcolor)-1):
            Newcolor[k],Newcolor[k+1]=Newcolor[k+1],Newcolor[k]  # Échange des couleurs de proche en proche
        self.couleurs=Newcolor
        self.redraw()  # On redessine avec les nouvelles couleurs




#Lignes de test
if __name__ == "__main__":
    print('Début du Test')
    nb_fils=8
    Liste=[2,1,2,1,2,3]

    data=Data(nb_fils,Liste)
    app=App(data,couleurs)
    app.run_forever()
    print('Fin du Test')
#Je n'ai pas pu aller plus loin dans ce TD car n'ayant pas pu avancer jusqu'au Reidemeister en présentiel, je ne connais pas les commandes à utiliser
