import time


class Player:
    def __init__(self, name, rating=1500.0):
        self.name = name
        self.rating = rating
        self.games_played = 0
        self.rd = 350.0
        self.last_active = time.time()
        self.streak = 0

    def __str__(self):
        return (f"{self.name}: Rating={self.rating:.2f}, "
                f"RD={self.rd:.2f}, Games={self.games_played}, "
                f"Streak={self.streak}")


# -----------------------------
# Core Functions
# -----------------------------

def expected_score(player_a, player_b):
    return 1 / (1 + 10 ** ((player_b.rating - player_a.rating) / 400))


def get_k_factor(player):
    if player.games_played < 30:
        return 40
    elif player.rating >= 2400:
        return 10
    else:
        return 20


def rd_multiplier(player):
    return player.rd / 350.0


def update_inactivity(player, current_time):
    time_passed = (current_time - player.last_active) / 86400
    player.rd = min(350.0, player.rd + time_passed * 5)


def streak_bonus(player):
    return min(abs(player.streak) * 2, 10)


def importance_multiplier(match_type):
    if match_type == "casual":
        return 0.5
    elif match_type == "ranked":
        return 1.0
    elif match_type == "tournament":
        return 1.5
    return 1.0


def update_ratings(player_a, player_b, score_a, score_b, match_type):
    current_time = time.time()

    update_inactivity(player_a, current_time)
    update_inactivity(player_b, current_time)

    expected_a = expected_score(player_a, player_b)
    expected_b = expected_score(player_b, player_a)

    k_a = get_k_factor(player_a)
    k_b = get_k_factor(player_b)

    rd_a = rd_multiplier(player_a)
    rd_b = rd_multiplier(player_b)

    streak_a = streak_bonus(player_a)
    streak_b = streak_bonus(player_b)

    importance = importance_multiplier(match_type)

    delta_a = importance * k_a * rd_a * (score_a - expected_a) + streak_a
    delta_b = importance * k_b * rd_b * (score_b - expected_b) + streak_b

    player_a.rating += delta_a
    player_b.rating += delta_b

    # Update streaks
    if score_a == 1:
        player_a.streak = max(1, player_a.streak + 1)
        player_b.streak = min(-1, player_b.streak - 1)
    elif score_b == 1:
        player_b.streak = max(1, player_b.streak + 1)
        player_a.streak = min(-1, player_a.streak - 1)
    else:
        player_a.streak = 0
        player_b.streak = 0

    # Reduce RD
    player_a.rd = max(30.0, player_a.rd * 0.95)
    player_b.rd = max(30.0, player_b.rd * 0.95)

    player_a.last_active = current_time
    player_b.last_active = current_time

    player_a.games_played += 1
    player_b.games_played += 1


# -----------------------------
# CLI Interface
# -----------------------------

def get_player(players, name):
    if name not in players:
        rating = float(input(f"Enter initial rating for {name}: "))
        players[name] = Player(name, rating)
    return players[name]


def get_match_type():
    while True:
        mt = input("Enter match type (casual/ranked/tournament): ").lower()
        if mt in ["casual", "ranked", "tournament"]:
            return mt
        print("Invalid match type!")


def get_match_result():
    print("Enter result:")
    print("1 → Player A wins")
    print("2 → Player B wins")
    print("3 → Draw")

    while True:
        choice = input("Choice: ")
        if choice == "1":
            return 1, 0
        elif choice == "2":
            return 0, 1
        elif choice == "3":
            return 0.5, 0.5
        else:
            print("Invalid choice!")


def display_players(players):
    print("\n--- Current Ratings ---")
    for p in players.values():
        print(p)
    print("------------------------\n")


# -----------------------------
# Main Loop
# -----------------------------

def main():
    players = {}

    print("=== Elo Rating System ===")

    while True:
        name_a = input("Enter Player A name: ")
        name_b = input("Enter Player B name: ")

        player_a = get_player(players, name_a)
        player_b = get_player(players, name_b)

        match_type = get_match_type()
        score_a, score_b = get_match_result()

        update_ratings(player_a, player_b, score_a, score_b, match_type)

        display_players(players)

        cont = input("Do you want to enter another match? (y/n): ").lower()
        if cont != "y":
            break


if __name__ == "__main__":
    main()
