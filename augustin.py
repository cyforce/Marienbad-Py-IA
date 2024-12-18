def regles():
    global nbLignes;
    print("Le jeu de Marienbad, vous devez retirer un nombre de baton sur des lignes, le dernier qui retire un baton a perdu.")
    nbLignes = int(input("Entrez le nombre total de lignes: "))
    while nbLignes < 1:
        nbLignes = int(input("Entrez le nombre total de lignes: "))
        
    print("""
    Modes : 1 - JcJ
            2 - IAcJ (IA aléatoire)
            3 - IAcJ (IA gagnante)
            4 - IAcIA (IA gagnant vs IA gagnante)
    """)
    mode_de_jeu = int(input("Entrez le mode de jeu: "))
    while mode_de_jeu not in [1,2,3,4]:
        mode_de_jeu = int(input("Entrez le mode de jeu: "))

def display_board_with_bare(l):
    for i in l:
        print("| "*i, end="\n")

def creer_plateau(n):
    plateau = []
    for i in range(1, n+1, 2):
        plateau.append(i)
    return plateau

def partie(plateau):
    end=False
    while end==False:
        nb = int(input("Entrez un nombre: "))
        if nb in plateau:
            plateau.remove(nb)
            display_board_with_bare(plateau)
        else:
            end=True

regles()
display_board_with_bare(nbLignes)
#plateau = creer_plateau(total)
