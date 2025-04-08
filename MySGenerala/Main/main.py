import random
import sys


class Generala:
    def __init__(self):
        self.dice = [0] * 5
        self.rolls_left = 3
        self.held = [False] * 5
        self.scores = {
            "1": None, "2": None, "3": None, "4": None, "5": None, "6": None,
            "Escalera": None, "Full": None, "Poker": None, "Generala": None,
            "Doble": None
        }
        self.last_generala = False  # Para controlar el Doble

    def roll_dice(self):
        if self.rolls_left == 0:
            print("¡No te quedan más tiradas en este turno!")
            return

        print("\nTirando los dados...")
        for i in range(5):
            if not self.held[i]:
                self.dice[i] = random.randint(1, 6)

        self.rolls_left -= 1
        self.display_dice()
        print(f"Tiradas restantes: {self.rolls_left}")

    def display_dice(self):
        print("Dados:", " ".join(str(d) for d in self.dice))
        print("Guardados:", " ".join("X" if h else " " for h in self.held))

    def toggle_hold(self, positions):
        for pos in positions:
            if 1 <= pos <= 5:
                self.held[pos - 1] = not self.held[pos - 1]
        self.display_dice()

    def reset_turn(self):
        self.held = [False] * 5
        self.rolls_left = 3

    def calculate_scores(self):
        counts = [self.dice.count(i) for i in range(1, 7)]
        score_options = {}

        # Puntajes por números
        for i in range(1, 7):
            if self.scores[str(i)] is None:
                score_options[str(i)] = i * counts[i - 1]

        # Combinaciones especiales
        if 5 in counts:
            if self.scores["Generala"] is None:
                score_options["Generala"] = 50
            elif self.last_generala and self.scores["Doble"] is None:
                score_options["Doble"] = 100

        if 4 in counts and self.scores["Poker"] is None:
            score_options["Poker"] = 40

        if (3 in counts and 2 in counts) and self.scores["Full"] is None:
            score_options["Full"] = 30

        sorted_dice = sorted(self.dice)
        is_straight = (
                (sorted_dice == [1, 2, 3, 4, 5] or sorted_dice == [2, 3, 4, 5, 6]) and
                self.scores["Escalera"] is None
        )
        if is_straight:
            score_options["Escalera"] = 25

        return score_options

    def record_score(self, category):
        if self.scores[category] is not None:
            print("¡Ya anotaste puntos en esa categoría!")
            return False

        score_options = self.calculate_scores()
        if category not in score_options and category not in self.scores:
            print("¡Categoría inválida!")
            return False

        if category in score_options:
            self.scores[category] = score_options[category]
        else:
            # Poner cero en la categoría
            self.scores[category] = 0

        # Controlar si fue Generala para el Doble
        self.last_generala = (category == "Generala")
        self.reset_turn()
        return True

    def display_scores(self):
        print("\nPlanilla de Puntajes:")
        for category, score in self.scores.items():
            print(f"{category:>8}: {score if score is not None else '-'}")

    def play_turn(self):
        self.reset_turn()
        self.roll_dice()

        while True:
            if self.rolls_left == 0:
                print("\n¡No te quedan tiradas! Tenés que elegir una categoría para anotar.")
                self.display_dice()
                self.display_scores()
                score_options = self.calculate_scores()

                if score_options:
                    print("\nOpciones para anotar:")
                    for cat, score in score_options.items():
                        print(f"{cat}: {score}")
                else:
                    print("\n¡No hay opciones válidas! Tenés que poner cero en una categoría.")

                while True:
                    category = input("Elegí categoría para anotar (o 'z' para poner cero): ").capitalize()
                    if category.lower() == 'z':
                        category = input("Elegí categoría para poner cero: ").capitalize()
                        if category in self.scores and self.scores[category] is None:
                            self.scores[category] = 0
                            self.reset_turn()
                            break
                        else:
                            print("¡No podés poner cero en esa categoría!")
                    elif category in self.scores:
                        if self.record_score(category):
                            break
                    else:
                        print("¡Categoría inválida!")
                break

            action = input("\n¿Qué hacés? (t)irar, (g)uardar, (a)notar, (s)alir: ").lower()

            if action == 't':
                self.roll_dice()
            elif action == 'g':
                try:
                    positions = list(map(int, input("Posiciones de dados a guardar/liberar (1-5, separados por espacio): ").split()))
                    self.toggle_hold(positions)
                except:
                    print("¡Entrada inválida! Tenés que poner números del 1 al 5.")
            elif action == 'a':
                self.display_scores()
                score_options = self.calculate_scores()
                if score_options:
                    print("\nOpciones para anotar:")
                    for cat, score in score_options.items():
                        print(f"{cat}: {score}")

                    while True:
                        category = input("Elegí categoría para anotar: ").capitalize()
                        if category in self.scores:
                            if self.record_score(category):
                                break
                        else:
                            print("¡Categoría inválida!")
                else:
                    print("¡No hay opciones válidas! Tenés que poner cero en una categoría.")
                    while True:
                        category = input("Elegí categoría para poner cero: ").capitalize()
                        if category in self.scores and self.scores[category] is None:
                            self.scores[category] = 0
                            self.reset_turn()
                            break
                        else:
                            print("¡No podés poner cero en esa categoría!")
                break
            elif action == 's':
                sys.exit()
            else:
                print("¡Acción inválida! Tenés que poner t, g, a o s.")

        self.display_scores()

    def is_game_over(self):
        return all(score is not None for score in self.scores.values())

    def calculate_total(self):
        total = sum(score for score in self.scores.values() if score is not None)

        number_section = sum(self.scores[str(i)] for i in range(1, 7) if self.scores[str(i)] is not None)
        if number_section >= 60:
            total += 30

        return total

    def play_game(self):
        print("¡Bienvenido a la Generala!")
        print("Objetivo: Sumar puntos haciendo combinaciones con cinco dados.")

        while not self.is_game_over():
            print("\n" + "=" * 40)
            print(f"Puntaje actual: {self.calculate_total()}")
            self.play_turn()

        print("\n¡Fin del juego!")
        print(f"Puntaje final: {self.calculate_total()}")


if __name__ == "__main__":
    game = Generala()
    game.play_game()