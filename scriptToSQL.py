from random import *
from collections import *
import mysql.connector
from env import connection_params

def creer_plateau(n):
    plateau = [1]
    for i in range(1, n):
        plateau.append(plateau[i-1]+2)
    return plateau

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

def IA_renforcement(renforcement, plateau, probaCoupBase=5):

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
            tas = next(i for i in range(len(plateau)) if plateau[i] > 0)

        totalPossibleAllumettes = sum(renforcement[key][str(tas)][j] for j in range(1, plateau[tas] + 1))

        # Si aucun choix d'allumettes valide (poids incorrects)
        if totalPossibleAllumettes == 0:
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

    # Retourner les choix effectués pour l'apprentissage
    return plateau, (key, tas, nbAllumettes)

def apprenstissage(renforcement, params):
    victoireDefaite = [0,0]  # [victoire, défaite]
    for i in range(params[3]):
        lesChoix = []
        plateau = creer_plateau(params[2])

        print(f"--- Partie {i + 1} ---")

        while not gagne(plateau):
            # IA renforcée joue
            plateau, choix = IA_renforcement(renforcement, plateau)
            lesChoix.append(choix)

            if gagne(plateau):  # Si l'IA renforcée gagne
                print("L'IA Renforcée a gagné")
                victoireDefaite[0] += 1
                for choix in lesChoix:
                    key, tas, nbAllumettes = choix
                    renforcement[key][str(tas)][nbAllumettes] += params[0]
                break

            # L'IA classique joue en suivant la stratégie gagnante
            tas, nbAllumettes = strategie_gagnante(plateau)
            plateau[tas] -= nbAllumettes

            if gagne(plateau):  # Si l'IA classique gagne
                print("L'IA classique a gagné")
                victoireDefaite[1] += 1
                for choix in lesChoix:
                    key, tas, nbAllumettes = choix
                    renforcement[key][str(tas)][nbAllumettes] -= params[1]
                break
        envoiDataPartie(params, victoireDefaite, renforcement)
        
    print(f"Résultats : Victoires : {victoireDefaite[0]}, Défaites : {victoireDefaite[1]}")

def main():
    recompenses = [1, 1] # [bonus, malus]
    params = recompenses + [3, 100] # [bonus, malus, nbTas, nbParties]
    renforcement = {}

    apprenstissage(renforcement, params)

def envoiDataPartie(params, victoireDefaite, renforcement):
    with mysql.connector.connect(**connection_params) as db :
        with db.cursor() as c:
            c.execute(f"INSERT INTO Parties (param_bonus, param_malus, param_nbTas, param_nbParties, partie_nbVictoire, jeu_dico) \
                    values (${params[0]}, ${params[1]}, ${params[2]}, ${params[3]}, ${victoireDefaite[0]}, ${str(renforcement)})")
            db.commit()

if __name__ == "__main__":
    main()