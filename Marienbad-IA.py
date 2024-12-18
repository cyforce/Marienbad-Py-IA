from random import *
from collections import *

def display_board_with_bare(l):
    for i in range(len(l)):
        print(str(i)+" : "+"| "*l[i], end="\n")

def creer_plateau(n):
    plateau = [1]
    for i in range(1, n):
        plateau.append(plateau[i-1]+2)
    return plateau

def jeu(nbTas, modeJeu):
    plateau = creer_plateau(nbTas)
    match modeJeu:
        case 1: # JcJ
            nom1 = input("Nom du joueur 1: ")
            nom2 = input("Nom du joueur 2: ")

            while not gagne(plateau):
                plateau = joueur_humain(plateau, nom1)
                if not gagne(plateau):
                    plateau = joueur_humain(plateau, nom2)
                    if gagne(plateau):
                        print(f"{nom2} a gagné")
                else:
                    print(f"{nom1} a gagné")
        case 2: # JcO
            nom1 = input("Nom du joueur: ")

            while not gagne(plateau):
                plateau = joueur_humain(plateau, nom1)
                if not gagne(plateau):
                    plateau = ordi(plateau, "IA")
                    if gagne(plateau):
                        print("L'IA a gagné")
                else:
                    print(f"{nom1} a gagné")
        case 3: # OcJ
            nom1 = input("Nom du joueur: ")

            while not gagne(plateau):
                plateau = ordi(plateau, "IA")
                if not gagne(plateau):
                    plateau = joueur_humain(plateau, nom1)
                    if gagne(plateau):
                        print(f"{nom1} a gagné")
                else:
                    print("L'IA a gagné")
        case 4: # OcO
            while not gagne(plateau):
                plateau = ordi(plateau, "IA1")
                if not gagne(plateau):
                    plateau = ordi(plateau, "IA2")
                    if gagne(plateau):
                        print("L'IA2 a gagné")
                else:
                    print("L'IA1 a gagné")
        case 5: # Renforcement
            print("Mode de jeu non implémenté")

def joueur_humain(plateau, nomJoueur):
    print(f"Tour de {nomJoueur}")
    display_board_with_bare(plateau)

    tas = int(input("Choisissez un tas: "))
    while tas not in range(0, len(plateau)) or plateau[tas] == 0:
        tas = int(input("Choisissez un tas: "))
    nbAllumettes = int(input("Choisissez un nombre d'allumettes: "))

    while nbAllumettes>plateau[tas] or nbAllumettes<1:
        nbAllumettes = int(input("Choisissez un nombre d'allumettes: "))
    plateau[tas] -= nbAllumettes

    return plateau

def gagne(plateau):
    gagne = True
    nb1 = 0
    i = 0

    while gagne and i<len(plateau):
        if plateau[i]>1 or nb1>1:
            gagne = False
        elif plateau[i] == 1:
            nb1 += 1
        i += 1
    
    return gagne

def strategie_gagnante(plateau):
    # Calculer le Nim-sum (somme XOR de tous les tas)
    nim_sum = 0
    for tas in plateau:
        nim_sum ^= tas

    # Si le Nim-sum est 0, il n'y a pas de coup gagnant, jouer un coup aléatoire
    if nim_sum == 0:
        for i in range(len(plateau)):
            if plateau[i] > 0:
                return i, 1

    # Trouver le tas à partir duquel jouer pour gagner
    for i in range(len(plateau)):
        if plateau[i] ^ nim_sum < plateau[i]:
            nbAllumettes = plateau[i] - (plateau[i] ^ nim_sum)
            return i, nbAllumettes

    return None, None

def coupAleatoire(plateau):
    tas = randint(0, len(plateau)-1)
    while plateau[tas] == 0:
        tas = randint(0, len(plateau)-1)
    nbAllumettes = randint(1, plateau[tas])
    return tas, nbAllumettes

def ordi(plateau, nomOrdi):
    print(f"Tour de {nomOrdi}")
    display_board_with_bare(plateau)

    tas, nbAllumettes = strategie_gagnante(plateau)
    if tas is not None and nbAllumettes is not None:
        plateau[tas] -= nbAllumettes
        print(f"{nomOrdi} retire {nbAllumettes} allumette(s) du tas {tas}")
    else:
        tas, nbAllumettes = coupAleatoire(plateau)
        plateau[tas] -= nbAllumettes
        print(f"{nomOrdi} retire {nbAllumettes} allumette(s) du tas {tas}")

    return plateau

def IA_renforcement():
    print("Mode de jeu non implémenté")

def main():
    rouges = {}
    jaunes = {}
jeu(5, 4)