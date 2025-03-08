class Player:
    def __init__(self, name, rating=1500):
        self.name = name
        self.rating = rating

def expected_score(player_a, player_b):
    """Calculate the expected score for player A."""
    return 1 / (1 + 10 ** ((player_b.rating - player_a.rating) / 400))

def update_ratings(player_a, player_b, score_a, score_b, k_factor=32):
    """Update ratings for both players after a match."""
    # Calculate expected scores
    expected_a = expected_score(player_a, player_b)
    expected_b = expected_score(player_b, player_a)

    # Update ratings
    player_a.rating += k_factor * (score_a - expected_a)
    player_b.rating += k_factor * (score_b - expected_b)

def display_ratings(players):
    """Display the current ratings of players."""
    for player in players:
        print(f'{player.name}: {player.rating:.2f}')

# Example usage
if __name__ == "__main__":
    # Create players
    alice = Player('Alice')
    bob = Player('Bob')

    # Display initial ratings
    print("Initial Ratings:")
    display_ratings([alice, bob])

    # Simulate a match where Alice wins against Bob
    update_ratings(alice, bob, score_a=1, score_b=0)

    # Display updated ratings
    print("\nUpdated Ratings after Alice wins:")
    display_ratings([alice, bob])

    # Simulate another match where Bob wins against Alice
    update_ratings(alice, bob, score_a=0, score_b=1)

    # Display updated ratings
    print("\nUpdated Ratings after Bob wins:")
    display_ratings([alice, bob])
