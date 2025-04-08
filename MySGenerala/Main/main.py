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

    def roll_dice(self):
        if self.rolls_left == 0:
            print("No rolls left this turn!")
            return

        print("\nRolling dice...")
        for i in range(5):
            if not self.held[i]:
                self.dice[i] = random.randint(1, 6)

        self.rolls_left -= 1
        self.display_dice()
        print(f"Rolls left: {self.rolls_left}")

    def display_dice(self):
        print("Dice:", " ".join(str(d) for d in self.dice))
        print("Held:", " ".join("X" if h else " " for h in self.held))

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

        # Number scores
        for i in range(1, 7):
            if self.scores[str(i)] is None:
                score_options[str(i)] = i * counts[i - 1]

        # Special combinations
        if 5 in counts and self.scores["Generala"] is None:
            score_options["Generala"] = 50 if counts.count(5) == 1 else 100

        if 5 in counts and self.scores["Generala"] is not None and ["Doble"] is None  :
            score_options["Doble"] = 100 if counts.count(5) == 1 else 100

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
            print("Category already scored!")
            return False

        score_options = self.calculate_scores()
        if category not in score_options:
            print("Invalid category for current dice!")
            return False

        self.scores[category] = score_options[category]
        self.reset_turn()
        return True

    def display_scores(self):
        print("\nScore Card:")
        for category, score in self.scores.items():
            print(f"{category:>8}: {score if score is not None else '-'}")

    def play_turn(self):
        self.reset_turn()
        self.roll_dice()

        while True:
            if self.rolls_left == 0:
                print("\nNo rolls left - you must choose a scoring option!")
                self.display_dice()
                self.display_scores()
                score_options = self.calculate_scores()

                if score_options:
                    print("\nAvailable scoring options:")
                    for cat, score in score_options.items():
                        print(f"{cat}: {score}")
                else:
                    print("\nNo valid scoring options! You must select a category to zero.")

                while True:
                    category = input("Enter category to score (or 'z' to zero a category): ").capitalize()
                    if category.lower() == 'z':
                        category = input("Enter category to zero: ").capitalize()
                        if category in self.scores and self.scores[category] is None:
                            self.scores[category] = 0
                            self.reset_turn()
                            break
                        else:
                            print("Invalid category to zero!")
                    elif category in self.scores and self.scores[category] is None:
                        if category in score_options or not score_options:  # Allow zeroing even if not in options
                            self.record_score(category)
                            break
                        else:
                            print("Invalid category for current dice!")
                    else:
                        print("Invalid category!")
                break

            action = input("\nChoose action: (r)oll, (h)old, (s)core, (q)uit: ").lower()

            if action == 'r':
                self.roll_dice()
            elif action == 'h':
                try:
                    positions = list(
                        map(int, input("Enter dice positions to hold/unhold (1-5, space separated): ").split()))
                    self.toggle_hold(positions)
                except:
                    print("Invalid input!")
            elif action == 's':
                self.display_scores()
                score_options = self.calculate_scores()
                if score_options:
                    print("\nAvailable scoring options:")
                    for cat, score in score_options.items():
                        print(f"{cat}: {score}")

                    category = input("Enter category to score: ").capitalize()
                    if self.record_score(category):
                        break
                else:
                    print("No valid scoring options! You must select a category to zero.")
                    category = input("Enter category to zero: ").capitalize()
                    if category in self.scores and self.scores[category] is None:
                        self.scores[category] = 0
                        self.reset_turn()
                        break
            elif action == 'q':
                sys.exit()
            else:
                print("Invalid action!")

        self.display_scores()

    def is_game_over(self):
        return all(score is not None for score in self.scores.values())

    def calculate_total(self):
        total = sum(score for score in self.scores.values() if score is not None)

        # Bonus for number section (if sum is >= 60)
        number_section = sum(self.scores[str(i)] for i in range(1, 7) if self.scores[str(i)] is not None)
        if number_section >= 60:
            total += 30

        return total

    def play_game(self):
        print("Welcome to Generala!")
        print("Objective: Score points by rolling specific combinations with five dice.")

        while not self.is_game_over():
            print("\n" + "=" * 40)
            print(f"Current total: {self.calculate_total()}")
            self.play_turn()

        print("\nGame Over!")
        print(f"Final Score: {self.calculate_total()}")


if __name__ == "__main__":
    game = Generala()
    game.play_game()