#TD6: Entrelacs, Le JEU.
from tkinter import Tk, Canvas, Button, Label  # Importation de Tkinter pour créer l'interface graphique
from random import randint  # Pour générer des nombres aléatoires

# Liste de couleurs qu’on utilise pour les fils
couleurs= [
    "red", "green", "blue", "yellow", "cyan", "magenta", "black", "gray", "lightgray", "darkgray",
    "orange", "purple", "pink", "brown", "gold", "silver", "lime", "navy", "maroon"
]

# Classe qui gère les données de l'entrelacs
class Data:

    def __init__(self, nb_fils, croisements):
        self.nbfils=nb_fils  # Nombre de fils
        self.croisement=croisements  # Liste des croisements à effectuer

    def liste_mots(self):
        # Méthode pour convertir les croisements en "mots" donnant la direction
        nb_fils=self.nbfils
        Listedespositions=[k for k in range(nb_fils)]  # Ordre  des fils
        Mots=['']*nb_fils  # Liste qui va contenir les mots de chaque fil

        for l in self.croisement:  # Pour chaque croisement
            for j in range(nb_fils):
                if j==l+1:
                    Mots[Listedespositions[j]]+='HU'  # Monte
                elif j==l:
                    Mots[Listedespositions[j]]+='HD'  # Descend
                else:
                    Mots[Listedespositions[j]]+='HH'  # Reste horizontal
            # On échange les positions des deux fils croisés
            Listedespositions[l],Listedespositions[l+1]=Listedespositions[l+1],Listedespositions[l]
        return(Mots)

    def hasard(self):  # Génère un entrelacs aléatoire
        newcroisement = []
        newnb_fils = randint(2, 8)  # Nombre de fils aléatoire
        for k in range(newnb_fils):
            newcroisement.append(randint(0, newnb_fils - 2))  # Croisements aléatoires

        self.nbfils = newnb_fils
        self.croisement = newcroisement

        # Mise à jour de l'affichage
        self.app.canvas.config(width=60 * len(self.croisement) * 2 + 2,
                               height=max(200, self.nbfils * 60 + 40))
        self.app.redraw()


# Classe qui gère tout l’affichage avec Tkinter
class App:
    def __init__(self,data,couleurs):
        self.data=data  
        self.data.app = self  
        self.root = Tk()  
        self.canvas = Canvas(self.root, width=60*(len(self.data.croisement))*2+2, height=max(200,(self.data.nbfils)*60+40), background="white")
        self.canvas.grid(column =0, row =0,columnspan=5)  
        self.couleurs=couleurs  
        self.redraw()  

    def run_forever(self):  
        self.root.mainloop()

    def redraw(self):  # Redessine  le canevas
        canvas=self.canvas
        canvas.delete("all")  # On efface tout pour redessner par-dessus
        couleurs=self.couleurs
        data=self.data
        Mots=data.liste_mots()  # Récupère les mots des fils
        self.root.update()  # Mise à jour interface

        for num_fil in range(len(Mots)):  # Dessine chaque fil
            self.read_word(Mots[num_fil]+'H', 55,55,0,20+num_fil*55, couleurs[num_fil] )

        for i, c in enumerate(self.data.croisement):  # Ajout de rectangles clicquables sur chaque croisement
            x = 60*i*2+55
            y = 20+c*55+25
            longueur = 20
            rect = canvas.create_rectangle(x-longueur, y-longueur, x+2*longueur, y+longueur, outline="", fill="", tags=f"croisement{i}")
            canvas.tag_bind(f"croisement{i}", "<Button-1>", lambda e, numero=i: self.clic_croisement(numero))

        Quit = Button(self.root,text="Quit", command=self.quitter)  # Bouton pour quitter
        Quit.grid(row=2,column=1)

        ColorButton = Button(self.root,text="Color", command=self.recolorer)  # Bouton pour changer les couleurs
        ColorButton.grid(row=2,column=2 )

        Infoentrelacs =Label(self.root,text="Croisements:"+str(self.data.croisement))  # Affichage des croisements
        Infoentrelacs.grid(row=1,column=1)

        Aleatoire = Button(self.root,text="Aleatoire", command=self.data.hasard)  # Nouveau entrelacs aléatoire
        Aleatoire.grid(row=2,column=3)

    def read_word(self, mot, h, w, departx, departy,color):  # Décode les mots (HU, HD, HH) pour dessiner les fils
        canvas=self.canvas
        x=departx
        y=departy
        for k in mot:
            if k=='H':
                canvas.create_line(x,y,x+w,y, fill=str(color))  # Ligne horizontale
                x=x+h
            if k=='U':
                canvas.create_line(x,y,x+w,y-h, fill=str(color))  # Ligne qui monte
                x=x+w
                y=y-h
            if k=='D':
                canvas.create_line(x,y,x+w,y+h, fill=str(color))  # Ligne qui descend
                x=x+w
                y=y+h

    def quitter(self):  # Ferme la fenêtre
        self.root.destroy()
        print("La page a été fermée") #Pour savoir si la fonction marche, car problème de fermeture sur Mac

    def recolorer(self):  # Décale les couleurs (rotation)
        Newcolor=self.couleurs.copy()
        for k in range(len(Newcolor)-1):
            Newcolor[k],Newcolor[k+1]=Newcolor[k+1],Newcolor[k]  
        self.couleurs=Newcolor
        self.redraw()  # Redessine avec les nouvelles couleurs

    def clic_croisement(self,numero):
        croisements=self.data.croisement
        nbfils=self.data.nbfils
    
        # On calcule l'état des fils  
        positions=list(range(nbfils))
        etats=[]
        for indice,numero_croisement in enumerate(croisements):
            etats.append(positions.copy())
            positions[numero_croisement],positions[numero_croisement+1]=positions[numero_croisement+1],positions[numero_croisement]
    
        # On récupère les deux fils concernés par le croisement cliqué
        etat_au_moment=etats[numero]
        indice_croisement=croisements[numero]
        fil1=etat_au_moment[indice_croisement]
        fil2=etat_au_moment[indice_croisement+1]
    
        # On cherche un deuxième croisement entre les mêmes fils
        for indice_suivant in range(numero+1,len(croisements)):
            etat_suivant=etats[indice_suivant]
            indice_prochain=croisements[indice_suivant]
            f1=etat_suivant[indice_prochain]
            f2=etat_suivant[indice_prochain+1]
    
            # Si on retrouve les mêmes fils 
            if set((f1,f2))==set((fil1,fil2)):
                obstacle=False
    
                # On vérifie qu'aucun croisement intermédiaire est présent 
                for indice_inter in range(numero+1,indice_suivant):
                    indice_intermediaire=croisements[indice_inter]
                    inter_pos=etats[indice_inter]
                    inter_fils=(inter_pos[indice_intermediaire],inter_pos[indice_intermediaire+1])
                    if fil1 in inter_fils or fil2 in inter_fils:
                        obstacle=True
                        break
    
                # Si rien ne les sépare, on peut les supprimer
                if not obstacle:
                    croisements.pop(indice_suivant)
                    croisements.pop(numero)
                    self.redraw()
                    return



            


# Lancement du test
if __name__ == "__main__":
    print('Début du Test')
    nb_fils=8
    Liste=[1,1,2,2,3,3,4,1,4,5,5,6,6]

    data=Data(nb_fils,Liste)
    app=App(data,couleurs)
    app.run_forever()
    print('Fin du Test')
