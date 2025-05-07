#TD5: Entrelacs.

# Importation des modules de Tkinter pour avoir une interface graphique
from tkinter import Tk, Canvas, Button, Label
root = Tk()
root.title("Je suis une interface graphique")
#root.geometry("12000x12000")
canvas = Canvas(root, width=650, height=200, background="white")
canvas.grid(column =0, row =0,columnspan=5)
# Création de la fenêtre, en définissant la taille et création du canva


#Exercice 1: Traçage d'une ligne brisée à partir d'un mot
def read_word(canvas, mot, h, w,departx,departy,color):
    x=departx
    y=departy
    #Par rapport aux différents cas, on fait l'action associé'
    for k in mot:
        if k=='H':
            canvas.create_line(x,y,x+w,y, fill=str(color))
            x=x+h
        if k=='U':
            canvas.create_line(x,y,x+w,y-h, fill=str(color))
            x=x+w
            y=y-h
        if k=='D':
            canvas.create_line(x,y,x+w,y+h, fill=str(color))
            x=x+w
            y=y+h

Colors=['black','red','blue','green']  #Liste des couleurs, dans l'idéal, il faudrait une liste qui s'adapte avec le nombre de fils qu'on veut tracer, peut-être utiliser une fonction random pour choisir les couleurs.



#Exercice 2: Fonction pour dessiner un entrelacs à partir d'une liste de croisements
def entrelacs(Liste,nb_fils,Colors):
    #canvas = Canvas(root, width=50*(nb_fils), height=50*(nb_fils))

    canvas.delete("all") #Cette fonction permet de supprimer le canva, pour pouvoir redessiner par-dessus
    Listedespositions=[k for k in range(nb_fils)] #Je retiens ici la position de chaque fil car les fils changent de place lorsqu'ils se croisent
    Mots=['']*nb_fils #Je stockes les mots dans une liste pour pouvoir faire une boucle et appeler la fonction read_word facilement


#Construction des chemins par rapport à la liste des positions
    for croisement in Liste:
        for j in range(nb_fils):
            if j==croisement+1:
                Mots[Listedespositions[j]]+='HU'
            elif j==croisement:
                Mots[Listedespositions[j]]+='HD'
            else:
                Mots[Listedespositions[j]]+='HH'
#Après avoir tracé les traits, on met à jour la liste des positions pour prendre en compte l'échange de position lors du croisement
        Listedespositions[croisement],Listedespositions[croisement+1]=Listedespositions[croisement+1],Listedespositions[croisement]
        print(Listedespositions) #Cette ligne permet de voir les modifications de la liste à chaque itération, pour comprendre mes erreurs de codage pour cette fonction

#On trace ici les traits avec une boucle en appelant la fonction read_word
#Exercice 3 : On ajoute des couleurs aux fils
    for num_fil in range(len(Mots)):
        read_word(canvas, Mots[num_fil]+'H', 60,60,0,20+num_fil*50, Colors[num_fil])

#Cette partie correspond aux boutons et la description "croisement : [...]"
#Exercice 4 : On ajoute les boutons Quit et Color
    Quit = Button(root,text="Quit", command=quitter)
    Quit.grid(row=2,column=1)
    ColorButton = Button(root,text="Color", command=recolorer)
    ColorButton.grid(row=2,column=2 )
#Exercice 5: On ajoute les tableaux des croisements.
    Infoentrelacs =Label(root,text="                                         Croisements:         "+str(Liste))
    Infoentrelacs.grid(row=1,column=1)

#Ici j'ai un problème d'alignement des éléments, je sais pas si c'est dû à la taille des objets
#Il y a conflit entre la description "Croisement=[...]" et les boutons Quit et colors.
#J'ai aussi un problème avec le bouton Quit qui ne ferme pas la page
#Le bouton Colors ne marche qu'une fois

def recolorer(): #Cette fonction permet d'écrire plusieurs tâches à faire, ce qui est impossible directement dans les paramètres de Button, en mettant command=recolorer, on appelle directement tout le code de "recolorer"
    Newcolor=Colors.copy()
    for k in range(nb_fils-1):
        Newcolor[k],Newcolor[k+1]=Newcolor[k+1],Newcolor[k]
    entrelacs(Liste,nb_fils,Newcolor)

def quitter():
    root.quit()
    print("La page a été fermée") #J'ai ajouté cette ligne parce que la page ne se ferme pas sur mon ordinateur, mais comme j'ai le message de fermeture, je me dis que c'est juste un bug de mon ordi, ou une erreur de formule


#Ces lignes permettent de faire les tests
nb_fils=4
Liste=[2,1,1,0,2]
entrelacs(Liste,nb_fils,Colors)
root.mainloop()
