# unité de longueur choisie 100 mètres
# la première ligne du public se trouve sur la droite d'équation x=z=0

import math
import time 

tps1 = time.clock()



g0=0.1 # accélération de la pesanteur

N=4 # nombre de points (pixels)

DONNEES=[[0,1],[1,0],[0,-1],[-1,0]] # ([ abscisse dans plan image, ordonnée dans plan image])

l=10 # largeur du public

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

theta=math.atan(M[2]/(M[0]+e/2)) # angle du plan par rapport à la verticale

for k in range(N):
    POS.append([M[0]-DONNEES[k][1]*math.sin(theta),M[1]-DONNEES[k][0],M[2]+DONNEES[k][1]*math.cos(theta)])

PENTE=[0,0,0,0]  # valeurs des pentes des trajectoires à l'explosion -- est déterminé par les fonctions suivantes

RES=[[0,0,0],[0,0,0],[0,0,0],[0,0,0]]  # couples (vitesse initiale, angle theta, angle.phi) à fournir aux canons (angles en degrés)

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


	ycourant=C[1] # point de départ pour les tests faisant varier le spectateur 
	epsilon=1 # indique la direction dans laquelle se trouve le spectateur avec le pire des omega2 
	if POS[k][2]-C[2]<0:
		epsilon=-1


	def omega2(u,p):      # vitesse angulaire au carré observée par un spectateur situé en (0,u,0)
		s=POS[k][0]**2+(POS[k][1]-u)**2+POS[k][2]**2     # distance réelle entre spectateur courant et explosion
		return((1-((a*POS[k][0]+b*(POS[k][1]-u))/c+p*POS[k][2])**2/(s*(1+p**2)))*v2(c,h,p)/s)


	def pireomega2(p):      # identification du omega2 le plus élevé à p fixé (on fait varier le spectateur)
		ycourant=C[1] # initialisation de y courant
		pas=0.01*epsilon
		for i in range(4):
			while omega2(ycourant,p)<omega2(ycourant+pas,p):  # attention, cette boucle peut ne pas s'arrêter
				ycourant=ycourant+pas
			pas=pas/10
		return(omega2(ycourant,p))


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
print(RES)


tps2 = time.clock()
print("durée d'exécution",tps2-tps1)
