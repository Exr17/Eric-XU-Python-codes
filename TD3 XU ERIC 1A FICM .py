#Exercice 1/2 :Création de la classe Tree représentant des arbres

class Tree:
    #Initialisation d'un arbre avec une racine et des sous-arbres(ou pas)
    def __init__(self, label, *children):
        self.__label=label #La racine de l'arbre
        self.__children=children # Les sous-arbres


    def label(self):#Méthode pour récupérer la racine de l'arbre self
        return(self.__label)

    def children(self):#Méthode pour récupérer les enfants/ sous-arbres de l'arbre self
        return(self.__children)

    def nb_children(self):#Méthode pour donnant le nombre de sous-arbres
        return(len(list(self.__children)))

    def child(self, i:int): #Méthode pour directement avoir un des sous-arbres en connaissant sa position
        L=self.children()
        return(L[i])

    def is_leaf(self): #Méthode pour savoir si le sous-arbre est une feuille, c'est-à-dire qu'il n'a lui même pas de sous-arbres
        if len(list(self.children()))==0:
            return(True)
        return(False)
#Exercice 3:
    def depth(self):#Méthode pour calculer la profondeur d'un arbre ayant des sous-arbres.
        L=[]
        if self.is_leaf()==True: #Cas particulier où il n'y a pas de sous-enfants'
            return(0)
        for k in self.children():
            L.append(k.depth())
        return(max(L)+1)

    #Exercice 4: Méthode pour convertir l'arbre en une représentation plus visuelle.

    def __str__(self):
        ecriture=''
        children=self.children()
        nombre_children=self.nb_children()
        if nombre_children==0: # Si l'arbre n'a pas d'enfants (c'est une feuille)
            ecriture+=str(self.label()) # On ajoute simplement le label
        else:
            ecriture+=str(self.label())+'('
            for k in range(len(children)): # On parcourt tous les enfants
                if k==len(children)-1:
                    ecriture+=str(children[k])
                else:
                    ecriture+=str(children[k])+','
            ecriture=ecriture+')'
        return(ecriture)
        #Cette méthode est récursive car il faut traiter tous les sous-arbres des sous-arbres

    def __eq__(self, __value): #Méthode pour comparer deux arbres (On compare les représentations avec la fonction str)
        Arbre1=self
        Arbre2=__value
        if Arbre1.label()!=Arbre2.label():
            return(False)
        else:
            return(str(Arbre1)==str(Arbre2))

            #J'ai écris ce début de code pour le cas où deux arbres ont les mêmes sous-arbres mais dans un ordre différent sont considérés comme équivalents, soit un arbre a(a,b) et un arbre a(b,a)'
    # def ListeTreeEq(L1,L2):
    # L1=L1.copy()
    # L2=L2.copy()
    #     for k in range(len(L1)):
    #         L1[k]=str(L1[k])
    #     for k in range(len(L2)):
    #         L2[k]=str(L2[k])
    #     for k in L1:
    #         if k not in L2:
    #             return(False)
    #     for k in L2:
    #         if k not in L1:
    #             return(False)
    #     return(True)


#Exercice 5
#Le polynôme cité dans l'énoncé est : "P=Tree('+',Tree('*',Tree('3'),Tree('*',Tree('X'), Tree('X'))),Tree('+', Tree('*',Tree('5'),Tree('X')),Tree('7'))) et le code donne bien 6X+5"


#Le code me semble long, je crois faire des disjonctions de cas qui ne sont pas nécessaires, mais ça me permet de mieux comprendre

#Cette méthode permet de dériver un polynôme par rapport à une variable qu'on passe en paramètre

    def deriv(self, var:str):
        operation=self.label()
        X=Tree(var)
        if operation!='+' and operation!='*':
            if operation==var:
                return(Tree('1'))
            else:
                return(Tree('0'))

#Cas de l'addition:(f+g)'=f'+g'
        if operation=='+':
            f=self.child(0)
            g=self.child(1)
#Cas de l'addition:a+X ou X+a ou X+X ou a+a
            if f.is_leaf() and g.is_leaf():
                if f==X and g!=X:
                    f=Tree('1')
                    g=Tree('0')
                    return(Tree('+',f,g))
                if g==X and f!=X:
                    g=Tree('1')
                    f=Tree('0')
                    return(Tree('+',f,g))
                if g!=X and f!=X:
                    g=Tree('0')
                    f=Tree('0')
                    return(Tree('+',f,g))
                if g==X and f==X:
                    g=Tree('1')
                    f=Tree('1')
                    return(Tree('+',f,g))
#Cas de l'addition:g(X)+constante ou g(X)+X
            if f.is_leaf() and (g.is_leaf() is False):
                if f==X:
                    f=Tree('1')
                else:
                    f=Tree('0')
                return(Tree('+',f,g.deriv(var)))
#Cas de l'addition:f(X)+constante ou f(X)+X
            if g.is_leaf() and (f.is_leaf() is False):
                if g==X:
                    g=Tree('1')
                else:
                    g=Tree('0')
                return(Tree('+',f.deriv(var),g))

#Cas général pour l'addition(récursif)
            return(Tree('+',f.deriv(var),g.deriv(var)))
#Cas de la multiplication:(f*g)'=f'*g+f*g'
        if operation=='*':
            f=self.child(0)
            g=self.child(1)
#Cas de la multiplication: aX ou Xa ou aa ou XX.
            if f.is_leaf() and g.is_leaf():
                if f==X and g!=X:
                    return(g)
                if g==X and f!=X:
                    return(f)
                if g!=X and f!=X:
                    return(Tree('0'))
                if g==X and f==X:
                    g=X
                    f=Tree('2')
                    return(Tree('*',f,g))

#Cas général pour la multiplication(récursif)
            return(Tree('+',Tree('*',f.deriv(var),g),Tree('*',f,g.deriv(var))))


#JEU DE TEST DONNÉ PAR L'ÉNONCÉ'

import unittest



class TestTree(unittest.TestCase):

    def test_create_tree1(self):
        a = Tree('a')
        a1 = Tree('a1', a)
        a2 = Tree('a1', a, a)
        self.assertIsNotNone(a)
        self.assertIsNot(a, a1)
        self.assertIsNot(a1, a2)

    def test_create_tree2(self):
        a = Tree('a')
        b = Tree('b')
        fab = Tree('f', a, b)
        ga = Tree('g', a)
        gb = Tree('g', b)

        self.assertEqual(a.label(), 'a')
        self.assertEqual(len(a.children()), 0)
        self.assertEqual(b.label(), 'b')
        self.assertEqual(len(b.children()), 0)

        self.assertEqual(fab.label(), 'f')
        self.assertEqual(fab.child(0), a)
        self.assertEqual(fab.child(1), b)

    def test_leaf(self):
        a = Tree('a')
        ga = Tree('g', a)

        self.assertTrue(a.is_leaf())
        self.assertFalse(ga.is_leaf())

    def test_depth(self):
        a = Tree('a')
        b = Tree('b')
        fab = Tree('f', a, b)
        ga = Tree('g', a)
        gb = Tree('g', b)
        fagb = Tree('f', a, gb)

        self.assertEqual(a.depth(), 0)
        self.assertEqual(fab.depth(), 1)
        self.assertEqual(ga.depth(), 1)
        self.assertEqual(gb.depth(), 1)
        self.assertEqual(fagb.depth(), 2)

    def test_eq_tree(self):
        a1 = Tree('a')
        a2 = Tree('a')
        fab1 = Tree('f', Tree('a'), Tree('b'))
        fab2 = Tree('f', Tree('a'), Tree('b'))

        self.assertEqual(a1, a2)
        self.assertEqual(fab1, fab2)

    def test_deriv_constant(self):
        X = Tree('X')
        a = Tree('a')
        zero = Tree('0')
        self.assertEqual(a.deriv('X'), zero)
        self.assertEqual(zero.deriv('X'), zero)

    def test_deriv_X(self):
        X = Tree('X')
        Y = Tree('Y')
        zero = Tree('0')
        un = Tree('1')

        self.assertEqual(X.deriv('X'), un)
        self.assertEqual(Y.deriv('X'), zero)

    def test_deriv_addition(self):
        X = Tree('X')
        zero = Tree('0')
        un = Tree('1')

        self.assertEqual(Tree('+', X, X).deriv('X'), Tree('+', un, un))
        self.assertEqual(Tree('+', X, un).deriv('X'), Tree('+', un, zero))

if __name__ == '__main__':
    unittest.main()


