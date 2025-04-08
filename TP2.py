
#Exercice 1: Création de la classe des objets : polynômes

class Polynomial:
    #On considère que les coefficients sont rangés de l'ordre croissant des puissances de X.
    #Exemple : [1,2] => 1+2X
    def __init__(self,L):
        self.coeff=L


    def __str__(self):
        L=self.coeff
        ecriture=''
        for k in range(len(L)-1,-1,-1):
            if k==0:
                if L[k]==0:
                    ecriture+=''
                elif L[k]<0:
                    ecriture+=str(L[k])
                else:
                    ecriture+='+'+str(L[k])
            elif k==1:
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

        if ecriture=='':
            return("0")
        Liste=list(ecriture)
        if ecriture[0]=='+':
            Liste.remove('+')

        ecriture=''
        for k in Liste:
            ecriture+=str(k)
        return(ecriture)


    def __add__(self,p2):

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
        return(Polynomial(L))

    def scalar(self,c):
        L=self.coeff
        Liste=[]
        for k in L:
            Liste.append(k*c)
        return(Polynomial(Liste))


#Jeu de tests

assert(str(Polynomial([1,2,3]))=='3X^2+2X+1')
assert(str(Polynomial( []))=="0")
assert(str(Polynomial( [0]))=="0")
assert(str(Polynomial( [1]))=="1")
assert(str(Polynomial([2,0,3]))=="3X^2+2")

#Exercice 2:

class PolynomialZ:
    def __init__(self,L,q,n):
        self.q=q
        self.n=n
        self.coefficients=[]
        for k in L:
            self.coefficients.append(k)


        degmax=len(self.coefficients)
        nouveauself=self.coefficients[:n:]

        for k in range(n,degmax):
            compteur=0
            p=k
            while p>=n:
                compteur+=1
                p=p-n
            nouveauself[p]+=self.coefficients[k]*(-1)**(compteur)
        self.coeff = [i%q for i in nouveauself]

    def rescale(self,r,n):
        L=self.coeff.copy()
        return(PolynomialZ(L,r,n))


#Exercice 4:
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


#Exercice 5:
    def __mul__(self,P2):
        q=self.q
        n=self.n
        L1=self.coeff.copy()
        L2=P2.coeff.copy()
        diff = abs(len(L1) - len(L2))
        if len(L1)>len(L2):
            L2.extend([0]*diff)
        if len(L2)>len(L1):
            L1.extend([0]*(diff))
        N=len(L1)+len(L2)-1
        L=[0]*N

        for p in range(N):
            c=0

            for k in range(p+1):
                if k<len(L1) and p-k<len(L2):
                c+=L1[k]*L2[p-k]
            L[p]=c
        return(PolynomialZ(L,q,n))




print(PolynomialZ([36,2,3,4,5,6,7],4,2).coeff)
print(PolynomialZ([4,7,3,1],4,2).coeff)
print((PolynomialZ([36,2,3,4,5,6,7],4,2)+PolynomialZ([4,7,3,1],4,2)).coeff)
print((PolynomialZ([36,2,3,4,5,6,7],4,2)*PolynomialZ([4,7,3,1],4,2)).coeff)



















