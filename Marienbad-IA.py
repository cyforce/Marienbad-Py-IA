def display_board_with_bare(l):
    for i in l:
        print("| "*i, end="\n")

def creer_plateau(n):
    plateau = []
    for i in range(1, n+1, 2):
        plateau.append(i)
    return plateau

def jeu(nbTas):
    plateau = creer_plateau(nbTas)
    