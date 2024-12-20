import os

class MarienbadBot:

    def principal(self):
        self.launch_home()

    def launch_home(self):
        self.display_clear()
        self.display_home()
        selected_param = input("\033[34m[MENU PRINCIPAL]\033[0m Entrer votre sélection > ")

        while selected_param not in ['a', 'b']:
            self.display_clear()
            self.display_home()
            print("\033[31m[ERREUR]\033[0m Sélection mauvaise")
            selected_param = input("\033[34m[MENU PRINCIPAL]\033[0m Entrer votre sélection > ")

        if selected_param == 'a':
            self.launch_game()
        elif selected_param == 'b':
            input("\033[34m[MENU PRINCIPAL]\033[0m Entrer n'importe quelle touche pour relancer > ")
            self.launch_home()

    def launch_game(self):
        player_who_play = 0  # 1 -> First Player || 2 -> bot
        line_number = 0

        player1 = input("\033[34m[PARAMETRAGE]\033[0m Entrer le nom du joueur : ")
        player_who_play = int(input(f"\033[34m[PARAMETRAGE]\033[0m Choisisser le joueur qui commence ? (1 -> {player1} | 2 -> Robot) : "))
        while player_who_play not in [1, 2]:
            print("\033[31m[ERREUR]\033[0m Sélection mauvaise")
            player_who_play = int(input(f"\033[34m[PARAMETRAGE]\033[0m Choisisser le joueur qui commence ? (1 -> {player1} | 2 -> Robot) : "))

        line_number = int(input("\033[34m[PARAMETRAGE]\033[0m Entrer le nombre de ligne à utiliser pour jouer : "))
        while line_number < 2 or line_number > 15:
            print("\033[31m[ERREUR]\033[0m nombre de ligne incorrect, le nombre de ligne doit être compris entre 2 et 15")
            line_number = int(input("\033[34m[PARAMETRAGE]\033[0m Entrer le nombre de ligne à utiliser pour jouer : "))

        lines_content = self.generate_lines_content(line_number)

        while not self.player_won(lines_content):
            self.display_clear()
            if player_who_play == 1:
                self.display_game(lines_content, player1)
                self.player_remove_stick(lines_content, player1)
                player_who_play = 2
            else:
                self.bot_remove_stick(lines_content)
                player_who_play = 1

        self.display_game(lines_content, player1)
        self.display_clear()
        print("\n\n")
        print("\t\t═════════════════════════════════════════════════════════════════════════════════════════")
        if player_who_play == 1:
            print("\t\t                                    Le robot a gagné !")
        else:
            print(f"\t\t                                {player1} a gagné. Bien joué à toi")
        print("\t\t═════════════════════════════════════════════════════════════════════════════════════════")

        response = input("\t\t\033[34m[MENU PRINCIPAL]\033[0m Entrer q pour quitter ou entrer n'importe quelle touche pour relancer > ")
        if response != 'q':
            self.launch_home()
        else:
            print("\t\t\033[34m[MENU PRINCIPAL]\033[0m Merci d'avoir joué à Marienbad")

    def display_home(self):
        print("\n\n")
        print("\t\t\t\t\033[34m##     ##    ###    ########  #### ######## ##    ## ########     ###    ########  \n" +  
              "\t\t\t\t\033[34m###   ###   ## ##   ##     ##  ##  ##       ###   ## ##     ##   ## ##   ##     ## \n" +
              "\t\t\t\t\033[34m#### ####  ##   ##  ##     ##  ##  ##       ####  ## ##     ##  ##   ##  ##     ## \n" +
              "\t\t\t\t\033[34m## ### ## ##     ## ########   ##  ######   ## ## ## ########  ##     ## ##     ## \n" +
              "\t\t\t\t\033[34m##     ## ######### ##   ##    ##  ##       ##  #### ##     ## ######### ##     ## \n" +
              "\t\t\t\t\033[34m##     ## ##     ## ##    ##   ##  ##       ##   ### ##     ## ##     ## ##     ## \n" +
              "\t\t\t\t\033[34m##     ## ##     ## ##     ## #### ######## ##    ## ########  ##     ## ########  \n")









        print("\t\t\t\t\t\t\033[34mFait par : Augustin LETANG / Célian TOUZEAU\033[0m")
        print("\n\n")
        print("\t\t\t\t\t   a : \033[32mLancer le jeu\033[0m \t b : \033[32mLancer les tests unitaires\033[0m")
        print("\n\n")

    def display_clear(self):
        os.system('clear')

    def display_game(self, lines_content, player_name):
        print("\n\n")
        print("\t\t═════════════════════════════════════════════════════════════════════════════════════════")
        print(f"\t\t                            Au tour de {player_name} de jouer")
        print("\t\t═════════════════════════════════════════════════════════════════════════════════════════")
        print("\t\t  ╔═══════════╦═══════════════════════════════════════════════════════════════╗  ")
        for i, stick_number in enumerate(lines_content):
            if i < 10:
                print(f"\t\t  ║ Ligne {i}   ║", end="")
            else:
                print(f"\t\t  ║ Ligne {i}  ║", end="")
            print(" |" * stick_number + self.create_space(63 - stick_number * 2) + "║")
        print("\t\t  ╚═══════════╩═══════════════════════════════════════════════════════════════╝  ")

    def display_game_with_highlight(self, lines_content, player_name, selected_line):
        print("\n\n")
        print("\t\t═════════════════════════════════════════════════════════════════════════════════════════")
        print(f"\t\t                            Au tour de {player_name} de jouer")
        print("\t\t═════════════════════════════════════════════════════════════════════════════════════════")
        print("\t\t  ╔═══════════╦═══════════════════════════════════════════════════════════════╗  ")
        for i, stick_number in enumerate(lines_content):
            if i < 10:
                print(f"\t\t  ║ Ligne {i}   ║", end="")
            else:
                print(f"\t\t  ║ Ligne {i}  ║", end="")
            if i == selected_line:
                print("\033[44m", end="")
            print(" |" * stick_number, end="")
            if i == selected_line:
                print("\033[0m", end="")
            print(self.create_space(63 - stick_number * 2) + "║")
        print("\t\t  ╚═══════════╩═══════════════════════════════════════════════════════════════╝  ")

    def generate_lines_content(self, line_number):
        line_content = 1
        lines_content = []
        for i in range(line_number):
            lines_content.append(line_content)
            line_content += 2
        return lines_content

    def player_won(self, lines_content):
        total_stick_available = sum(lines_content)
        return total_stick_available == 0

    def player_remove_stick(self, lines_content, player_name):
        remove_done = False
        while not remove_done:
            print("\t\t═════════════════════════════════════════════════════════════════════════════════════════")
            line = int(input("\t\t                         Entrer la ligne à éditer : "))
            self.display_clear()
            self.display_game_with_highlight(lines_content, player_name, line)
            if line > len(lines_content) - 1 or line < 0:
                print("\t\t\033[31m  [ERREUR]\033[0m numéro de ligne mauvais")
            elif lines_content[line] == 0:
                print("\t\t\033[31m  [ERREUR]\033[0m impossible de retirer des batons sur une ligne vide")
            else:
                print("\t\t═════════════════════════════════════════════════════════════════════════════════════════")
                stick_number_to_remove = int(input("\t\t                  Entrer le nombre de baton à retirer : "))
                self.display_clear()
                self.display_game(lines_content, player_name)
                if stick_number_to_remove > lines_content[line]:
                    print(f"\t\t\033[31m  [ERREUR]\033[0m impossible de retirer {stick_number_to_remove} le nombre de baton à retirer est trop élevé pour cette ligne")
                elif stick_number_to_remove <= 0:
                    print(f"\t\t\033[31m  [ERREUR]\033[0m impossible de retirer {stick_number_to_remove} le nombre de baton à retirer est trop faible pour cette ligne")
                else:
                    lines_content[line] -= stick_number_to_remove
                    remove_done = True

    def bot_remove_stick(self, lines_content):
        xor_sum = 0
        removed_line = False

        for stick_number in lines_content:
            xor_sum ^= stick_number

        for e in range(len(lines_content)):
            i = 1
            while i <= lines_content[e] and not removed_line:
                reduced_line = lines_content[e] - i
                new_xor_sum = (xor_sum ^ lines_content[e]) ^ reduced_line
                if new_xor_sum == 0:
                    removed_line = True
                    lines_content[e] = reduced_line
                i += 1

        if not removed_line:
            for j in range(len(lines_content)):
                if lines_content[j] > 0:
                    lines_content[j] -= 1
                    break

    def create_space(self, n):
        return " " * n

if __name__ == "__main__":
    bot = MarienbadBot()
    bot.principal()