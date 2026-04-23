import time
import math


class Player:
    def __init__(self, name):
        self.name = name
        self.rating = 1500.0
        
        self.games_played = 0
        self.rd = 350.0            # rating deviation (uncertainty)
        self.last_active = time.time()
        self.streak = 0            # +ve = win streak, -ve = loss streak

    def __str__(self):
        return f"{self.name}: Rating={self.rating:.2f}, RD={self.rd:.2f}, Games={self.games_played}, Streak={self.streak}"


# -----------------------------
# Core Elo Functions
# -----------------------------

def expected_score(player_a, player_b):
    """Probability that player A wins."""
    return 1 / (1 + 10 ** ((player_b.rating - player_a.rating) / 400))


def get_k_factor(player):
    """Dynamic K-factor based on experience and rating."""
    if player.games_played < 30:
        return 40
    elif player.rating >= 2400:
        return 10
    else:
        return 20


def rd_multiplier(player):
    """Scale updates based on uncertainty."""
    return player.rd / 350.0


def update_inactivity(player, current_time):
    """Increase uncertainty if player inactive."""
    time_passed = (current_time - player.last_active) / 86400  # days
    player.rd = min(350.0, player.rd + time_passed * 5)


def streak_bonus(player):
    """Small bonus for streaks."""
    return min(abs(player.streak) * 2, 10)


def importance_multiplier(match_type):
    """Adjust rating impact based on match importance."""
    if match_type == "casual":
        return 0.5
    elif match_type == "ranked":
        return 1.0
    elif match_type == "tournament":
        return 1.5
    return 1.0


# -----------------------------
# Rating Update Function
# -----------------------------

def update_ratings(player_a, player_b, score_a, score_b, match_type="ranked"):
    current_time = time.time()

    # Handle inactivity
    update_inactivity(player_a, current_time)
    update_inactivity(player_b, current_time)

    # Expected scores
    expected_a = expected_score(player_a, player_b)
    expected_b = expected_score(player_b, player_a)

    # K-factors
    k_a = get_k_factor(player_a)
    k_b = get_k_factor(player_b)

    # RD scaling
    rd_a = rd_multiplier(player_a)
    rd_b = rd_multiplier(player_b)

    # Streak bonus
    streak_a = streak_bonus(player_a)
    streak_b = streak_bonus(player_b)

    # Match importance
    importance = importance_multiplier(match_type)

    # Rating changes
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

    # Reduce uncertainty after playing
    player_a.rd = max(30.0, player_a.rd * 0.95)
    player_b.rd = max(30.0, player_b.rd * 0.95)

    # Update activity time
    player_a.last_active = current_time
    player_b.last_active = current_time

    # Increment games
    player_a.games_played += 1
    player_b.games_played += 1


# -----------------------------
# Utility Functions
# -----------------------------

def display_players(players):
    print("\n--- Player Ratings ---")
    for p in players:
        print(p)
    print("----------------------\n")


# -----------------------------
# Example Simulation
# -----------------------------

if __name__ == "__main__":
    alice = Player("Alice")
    bob = Player("Bob")

    display_players([alice, bob])

    # Match 1: Alice wins
    update_ratings(alice, bob, 1, 0, match_type="ranked")
    print("After Match 1 (Alice wins):")
    display_players([alice, bob])

    time.sleep(1)

    # Match 2: Bob wins (upset)
    update_ratings(alice, bob, 0, 1, match_type="ranked")
    print("After Match 2 (Bob wins):")
    display_players([alice, bob])

    time.sleep(1)

    # Match 3: Tournament match (Alice wins)
    update_ratings(alice, bob, 1, 0, match_type="tournament")
    print("After Match 3 (Tournament - Alice wins):")
    display_players([alice, bob])

    # Simulate inactivity
    print("Simulating inactivity...")
    alice.last_active -= 10 * 86400  # 10 days inactive

    update_ratings(alice, bob, 1, 0, match_type="ranked")
    print("After inactivity match (Alice wins):")
    display_players([alice, bob])
