import random

LOG_FILE = "guessing_logs.txt"

# ── CORRECT MESSAGES ──
CORRECT_LINES = [
    "🎉 Boom! You nailed it!",
    "🏆 Perfect guess! Well done!",
    "🔥 Genius move!",
    "😎 Easy win for you!",
    "💥 Direct hit!",
]

# ── CLOSE FEEDBACK ──
CLOSE_LINE = "🔥 Getting closer!"

# ── HINT FLAGS ──
H_EVEN_ODD = 1
H_MOD3 = 2
H_LAST_DIGIT = 4
H_DIV5 = 8

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.games_played = 0
        self.profile = {
            "name": name,
            "score": 0,
            "games_played": 0
        }

    def update_score(self, points):
        self.score += points
        self.profile["score"] = self.score
        self.profile["games_played"] += 1

class NumberGame:
    def __init__(self, player, low=1, high=100, max_attempts=7, difficulty="Normal"):
        self.player = player
        self.low = low
        self.high = high
        self.max_attempts = max_attempts
        self.attempts = 0
        self.secret = random.randint(low, high)
        self.guesses = []
        self.won = False
        self.difficulty = difficulty
        self.hints = 0

    # ── HINT SYSTEM ──
    def unlock_hints(self):
        if self.difficulty == "Hard":
            start = 2
        else:
            start = self.max_attempts // 2

        if self.attempts >= start:
            if self.attempts == start:
                self.hints |= H_EVEN_ODD
            elif self.attempts == start + 1:
                self.hints |= H_MOD3
            elif self.attempts == start + 2:
                self.hints |= H_LAST_DIGIT
            elif self.attempts == start + 3:
                self.hints |= H_DIV5

    def show_hints(self):
        print("💡 HINTS:")
        if self.hints & H_EVEN_ODD:
            print(" - Number is", "Even" if self.secret % 2 == 0 else "Odd")
        if self.hints & H_MOD3:
            print(" - Mod 3 =", self.secret % 3)
        if self.hints & H_LAST_DIGIT:
            print(" - Last digit =", self.secret % 10)
        if self.hints & H_DIV5:
            print(" - Divisible by 5?", "Yes" if self.secret % 5 == 0 else "No")

    # ── GAME ──
    def start(self):
        print("\n" + "═" * 50)
        print(f"🎮 Difficulty: {self.difficulty}")
        print(f"🔢 Range: {self.low} - {self.high}")
        print(f"🎯 Attempts: {self.max_attempts}")
        print("═" * 50)

        while self.attempts < self.max_attempts:
            raw = input(f"\nAttempt {self.attempts + 1}: ").strip()
            try:
                guess = int(raw)
            except ValueError:
                print("Invalid input. Please enter a valid whole number.")
                continue

            if guess < self.low or guess > self.high:
                print("Out of range")
                continue

            if guess in self.guesses:
                print("Already guessed")
                continue

            self.guesses.append(guess)
            self.attempts += 1

            # ── FIX 1: NO HINTS AFTER LAST ATTEMPT ──
            if self.attempts < self.max_attempts:
                self.unlock_hints()

            # ── WIN ──
            if guess == self.secret:
                self.won = True
                bonus = (self.max_attempts - self.attempts + 1) * 10
                self.player.update_score(bonus)

                print("\n" + "🎬" * 20)
                print(random.choice(CORRECT_LINES))
                print(f"\n🎯 Secret Number: {self.secret}")
                print(f"⭐ Score Gained: +{bonus}")
                print(f"🏆 Total Score: {self.player.score}")
                print("🎬" * 20)
                break

            # ── WRONG GUESS ──
            print(CLOSE_LINE)

            if guess < self.secret:
                print("⬆ Go Higher")
            else:
                print("⬇ Go Lower")

            # ── FIX 2: HINTS ONLY IF GAME NOT OVER ──
            if self.hints and self.attempts < self.max_attempts:
                self.show_hints()

            # ── FIX 3: IMPROVEMENT CHECK SAFE ──
            if self.attempts < self.max_attempts and len(self.guesses) >= 2:
                if abs(self.guesses[-1] - self.secret) < abs(self.guesses[-2] - self.secret):
                    print("🧠 Getting closer!")

            print("History:", *self.guesses)

        else:
            print("\n💀 You lost! Number was", self.secret)

        print("\nResult:", "WINNER 🏆" if self.won else "LOSER 💀")
        self.log()

    def log(self):
        with open(LOG_FILE, "a") as f:
            f.write(f"{self.player.name} | {'WIN' if self.won else 'LOSS'} | {self.attempts} | {self.secret}\n")

# ── LOG ──
def view_log():
    try:
        with open(LOG_FILE, "r") as f:
            print("\n--- GAME LOG ---")
            print(f.read())
    except FileNotFoundError:
        print("No log yet. Play a game first to generate a history!")

# ── MAIN ──
def main():
    print("=" * 50)
    print(" NUMBER GUESSING GAME ")
    print("=" * 50)

    name = input("\nEnter name: ").strip() or "Player"
    player = Player(name)

    print(f"\nWelcome, {player.name}!")

    while True:
        print("\n1.Play  2.Log  3.Profile  0.Exit")
        ch = input("> ").strip()

        if ch == "1":
            print("\nSelect Difficulty:")
            print("1.Easy 2.Normal 3.Hard")
            d = input("> ")

            mapping = {
                "1": (10, "Easy"),
                "2": (7, "Normal"),
                "3": (5, "Hard")
            }

            max_att, diff_name = mapping.get(d, (7, "Normal"))

            game = NumberGame(player, max_attempts=max_att, difficulty=diff_name)
            game.start()

            player.games_played += 1
            player.profile["games_played"] = player.games_played

        elif ch == "2":
            view_log()

        elif ch == "3":
            print("\n--- PROFILE ---")
            for k, v in player.profile.items():
                print(k, ":", v)

        elif ch == "0":
            print("Bye! Score:", player.score)
            break

        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()