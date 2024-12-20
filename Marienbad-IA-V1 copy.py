from random import *
from collections import *

def display_board_with_bare(plateau):
    for i in range(len(plateau)):
        if isinstance(plateau[i], int):
            print(str(i) + " : " + "| " * plateau[i], end="\n")
        else:
            print(f"Erreur: plateau[{i}] n'est pas un entier.")

def creer_plateau(n):
    plateau = [1]
    for i in range(1, n):
        plateau.append(plateau[i-1]+2)
    return plateau

def jeu(nbTas, modeJeu=1, renforcement=None):
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

def IA_renforcement(renforcement, plateau, nomIA='IA_renforcee', probaCoupBase=5):
    print(f"Tour de {nomIA}")
    display_board_with_bare(plateau)

    # Identifier la configuration actuelle du plateau
    key = str(plateau)
    if key not in renforcement:
        renforcement[key] = {}
        for i in range(len(plateau)):
            renforcement[key][str(i)] = {}
            for j in range(1, plateau[i] + 1):
                renforcement[key][str(i)][j] = probaCoupBase  # Initialiser les poids des choix possibles

    # Vérifier que le plateau contient des tas non vides
    if all(tas == 0 for tas in plateau):
        print("Erreur : Plateau vide. Aucun coup possible.")
        return plateau, None

    # Sélection du tas
    tas = None
    while tas is None:
        totalBoulesTas = [sum(renforcement[key][str(i)].values()) for i in range(len(plateau))]
        tas = 0
        for i in range(len(plateau)):
            if totalBoulesTas[i] > totalBoulesTas[tas]:
                tas = i

    # Sélection du nombre d'allumettes
    nbAllumettes = None
    while nbAllumettes is None:
        if plateau[tas] == 0:
            print(f"Erreur : Le tas {tas} est vide, mais sélectionné. Forcer un nouveau choix.")
            tas = next(i for i in range(len(plateau)) if plateau[i] > 0)

        totalPossibleAllumettes = sum(renforcement[key][str(tas)][j] for j in range(1, plateau[tas] + 1))

        # Si aucun choix d'allumettes valide (poids incorrects)
        if totalPossibleAllumettes == 0:
            print("Erreur : Aucun choix valide pour les allumettes. Choix par défaut.")
            nbAllumettes = 1
            break

        choix_allumettes = randint(1, totalPossibleAllumettes)

        for j in range(1, plateau[tas] + 1):
            choix_allumettes -= renforcement[key][str(tas)][j]
            if choix_allumettes <= 0:
                nbAllumettes = j
                break

    # Mise à jour du plateau
    plateau[tas] -= nbAllumettes
    print(f"{nomIA} retire {nbAllumettes} allumette(s) du tas {tas}")

    # Retourner les choix effectués pour l'apprentissage
    return plateau, (key, tas, nbAllumettes)

def apprenstissage(renforcement, recompenses, nbTas=5, nbParties=1000):
    victoireDefaite = [0,0]  # [victoire, défaite]
    for i in range(nbParties):
        lesChoix = []
        plateau = creer_plateau(nbTas)

        print(f"--- Partie {i + 1} ---")
        display_board_with_bare(plateau)

        while not gagne(plateau):
            # IA renforcée joue
            plateau, choix = IA_renforcement(renforcement, plateau, "IA Renforcée")
            lesChoix.append(choix)

            if gagne(plateau):  # Si l'IA renforcée gagne
                print("L'IA Renforcée a gagné")
                victoireDefaite[0] += 1
                for choix in lesChoix:
                    key, tas, nbAllumettes = choix
                    renforcement[key][str(tas)][nbAllumettes] += recompenses[0]
                break

            # L'IA classique joue en suivant la stratégie gagnante
            tas, nbAllumettes = strategie_gagnante(plateau)
            plateau[tas] -= nbAllumettes
            print(f"L'IA classique retire {nbAllumettes} allumette(s) du tas {tas}")

            if gagne(plateau):  # Si l'IA classique gagne
                print("L'IA classique a gagné")
                victoireDefaite[1] += 1
                for choix in lesChoix:
                    key, tas, nbAllumettes = choix
                    renforcement[key][str(tas)][nbAllumettes] -= recompenses[1]
                break
        
    print(f"Résultats : Victoires : {victoireDefaite[0]}, Défaites : {victoireDefaite[1]}")

def main():
    recompenses = [1, 1] # [bonus, malus]
    renforcement = {}

    apprenstissage(renforcement, recompenses, 100, 200)

if __name__ == "__main__":
    main()