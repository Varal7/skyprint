# unité de longueur choisie 100 mètres
# la première ligne du public se trouve sur la droite d'équation X=Z=0

import math
import time


def resFromCoords(DONNEES):

    tps1 = time.clock()

    DONNEES = [[x / 100 for x in coord] for coord in DONNEES]

    g0=0.1 # accélération de la pesanteur

    N=len(DONNEES) # nombre de points (pixels)


    l=10 # largeur du public, qui est réparti symétriquement de part et d'autre de l'axe des X

    e=5 # épaisseur du public

    M=[4,0,4] # coordonnées de l'origine du plan image (peut-être faudrait-il plutôt choisir une donnée angulaire, à voir...)

    C=[1,0,0] # coordonnées du canon

    # Ci-dessous quelques fonctions liées à la trajectoire (ici parabolique, ce sont les calculs sur le feuille que j'ai mis sur slack le 11 octobre).
    #On suppose les mouvements planaires (effet Magnus négligé)

    def v2(c,h,p): # vitesse au carré à l'explosion avec une pente à l'explosion p, hauteur h, distance au sol c
        return(g0*((c**2+h**2)/(2*(h-c*p))-(h+c*p)/2))


    def v0(c,h,p): # vitesse initiale correspondante
        return(math.sqrt(g0*((c**2+(2*h-c*p)**2)/(2*(h-c*p)))))


    def alpha(c,h,p): # angle initial correspondant (par rapport à la verticale)
        return(math.atan(1/((2*h-c*p)/c))*180/math.pi)


    # fin des fonctions "balistiques"

    POS=[] # positions dans l'espace

    beta=math.atan(M[2]/(M[0]+e/2)) # angle du plan par rapport à la verticale

    for k in range(N):
        POS.append([M[0]-DONNEES[k][1]*math.sin(beta),M[1]-DONNEES[k][0],M[2]+DONNEES[k][1]*math.cos(beta)])

    PENTE=[0 for _ in range(N)]  # valeurs des pentes des trajectoires à l'explosion -- est déterminé par les fonctions suivantes

    RES=[[0,0,0] for _ in range(N)]  # couples (vitesse initiale, angle theta, angle.phi) à fournir aux canons (angles en degrés)

    for k in range(N):
        RES[k][2]=math.atan((POS[k][1]-C[1])/(POS[k][0]-C[0]))*180/math.pi

    VIT=[] # valeurs des vecteurs vitesses à l'explosion

    t0=0.5
    POINTS=[]  # positions à t = t_explosion +ou- to

    for k in range(N):

        h=POS[k][2] # hauteur explosion

        a=POS[k][0]-C[0]
        b=POS[k][1]-C[1]
        c=math.sqrt(a**2+b**2) # distance sol entre canon et explosion


        def pireomega2(p):      # identification du omega2 le plus élevé à p fixé
            V=[math.sqrt(v2(c,h,p))/math.sqrt(1+p**2),math.sqrt(v2(c,h,p))*p/math.sqrt(1+p**2)]
            PA=[c-t0*V[0],h-t0*V[1]]   # position t0 avant l'explosion, dans le plan de la trajectoire en prenant le canon pour origine, que l'on notera P
            PP=[c+t0*V[0],h+t0*V[1]]   # position t0 après l'explosion, dans P
            if PA[1]==PP[1]:
                x=(PA[0]+PP[0])/2
            else:
                l=(PA[1]*PP[0]-PA[0]*PP[1])/(PP[1]-PA[1])
                mu=PP[0]**2-2*PA[1]*((PA[1]+PP[1])/2+(PA[0]+PP[0])/2*(PP[0]-PA[0])/(PP[1]-PA[1]))
                x=-l-math.sqrt(l**2-mu)   # x contient maintenant la position au sol, dans P, pour laquelle l'angle d'observation est maximal - on choisit la plus petite solution du polynôme de dégré 2 car le public se trouve du côté des x négatifs
            X=[C[0]+a*x/c,C[1]+b*x/c]   # retour le repère principal pour se placer sur la zone du public - cependant je discrimine seulement par rapport à la profondeur (la largeur étant considérée comme suffisamment grande), car sinon il faudrait minimiser sous contrainte et ça compliquerait à nouveau les calculs
            if X[0]>0:
                x=-C[0]*c/a
            elif X[0]<-e:
                x=-(e+C[0])*c/a
            angleA=math.atan(PA[1]/(PA[0]-x))
            angleP=math.atan(PP[1]/(PP[0]-x))
            return(abs(angleA-angleP))


        #recherche du p minimisant pireomega2
        p=-0.1
        pas=0.01
        for i in range(4):
            if pireomega2(p-pas)<pireomega2(p):
                pas=-pas
            while pireomega2(p)>pireomega2(p+pas):  # attention, cette boucle peut ne pas s'arrêter
                p=p+pas
            pas=pas/10

        PENTE[k]=p

        #détermination des paramètres de lancement à partir de p
        RES[k][0]=v0(c,h,p)
        RES[k][1]=alpha(c,h,p)

        #calcul des positions à t = t_explosion +ou- to
        VIT.append([math.sqrt(v2(c,h,p))*a/(c*math.sqrt(1+p**2)),math.sqrt(v2(c,h,p))*b/(c*math.sqrt(1+p**2)),math.sqrt(v2(c,h,p))*p/math.sqrt(1+p**2)])
        DELTA=[x * t0 for x in VIT[k]]
        POSMOINS=[POS[k][0]-DELTA[0],POS[k][1]-DELTA[1],POS[k][2]-DELTA[2]]
        POSPLUS=[POS[k][0]+DELTA[0],POS[k][1]+DELTA[1],POS[k][2]+DELTA[2]]
        POINTS.append(POSMOINS)
        POINTS.append(POSPLUS)


    print(POINTS)
    tps2 = time.clock()
    print("durée d'exécution après modification",tps2-tps1)
    return (RES)
