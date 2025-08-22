##########################################################
# File Name: Final Project Liars Club
#
# Author(s): Michael Cummings
#
# Date: 05/06/25
#
# Description:
# Bluff Game - A two-player card deception game using Pygame
#
# Each player takes turns playing cards while declaring a specific card type (Ace, King, Queen, or Jack).
# The opponent can choose to call a bluff. If a bluff is successfully called, the liar faces Russian Roulette.
# If not, the challenger risks elimination. The last player alive wins.
#
# Features:
# - Card selection and play mechanics
# - Bluff calling with risk (randomized Russian Roulette outcome)
# - Visual card interface using Pygame
# - Auto-refill of hand after all cards are played

###########################################################

import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bluff Game")

# Set up fonts
FONT = pygame.font.Font(None, 36)
BIG_FONT = pygame.font.Font(None, 60)

# Define card types and their colors
CARD_TYPES = ['Ace', 'King', 'Queen', 'Jack']
CARD_COLORS = {
    'Ace': (255, 100, 100),
    'King': (100, 255, 100),
    'Queen': (100, 100, 255),
    'Jack': (255, 255, 100)
}

# Unique ID generator for cards
card_uid_counter = 0
def create_card(card_type):
    """Create a card with a unique ID and specified type."""
    global card_uid_counter
    card = {"type": card_type, "id": card_uid_counter}
    card_uid_counter += 1
    return card

class Player:
    """Class to represent a player in the game."""
    def __init__(self, name):
        self.name = name
        self.hand = [create_card(random.choice(CARD_TYPES)) for _ in range(5)]
        self.is_alive = True

def draw_hand(player, y_offset, selected):
    """Draw a player's hand on the screen."""
    buttons = []
    x = 50
    for card in player.hand:
        rect = pygame.Rect(x, y_offset, 100, 50)
        color = CARD_COLORS[card["type"]]
        pygame.draw.rect(screen, color, rect)

        # Highlight selected cards
        if card in selected:
            pygame.draw.rect(screen, (0, 255, 255), rect, 4)

        text = FONT.render(card["type"], True, (0, 0, 0))
        screen.blit(text, (x + 10, y_offset + 10))
        buttons.append((rect, card))
        x += 120
    return buttons

def show_temporary_message(text, duration=2):
    """Display a temporary message in the center of the screen."""
    screen.fill((30, 30, 30))
    message = BIG_FONT.render(text, True, (255, 255, 255))
    screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 2 - message.get_height() // 2))
    pygame.display.flip()
    time.sleep(duration)

def russian_roulette(player):
    """Simulate Russian Roulette for a player."""
    show_temporary_message(f"{player.name} is facing Russian Roulette...", 2)
    if random.randint(1, 6) <= 2:  # ~33% chance to die
        player.is_alive = False
        show_temporary_message(f"{player.name} has been eliminated!", 2)
    else:
        show_temporary_message(f"{player.name} survived!", 2)

def main():
    # Initialize players and game state
    players = [Player("Player 1"), Player("Player 2")]
    current_player_idx = 0
    current_card_type = random.choice(CARD_TYPES)
    selected_cards = []
    stage = "selecting"
    bluff_decision = None
    death_message = None

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill((30, 30, 30))

        # Check for game end
        alive_players = [p for p in players if p.is_alive]
        if len(alive_players) <= 1:
            if death_message:
                msg = FONT.render(death_message, True, (255, 100, 100))
                screen.blit(msg, (50, 200))
            winner = alive_players[0]
            win_text = FONT.render(f"{winner.name} wins!", True, (255, 255, 255))
            screen.blit(win_text, (50, 250))
            pygame.display.flip()
            pygame.time.wait(4000)
            break

        # Get current and opponent players
        player = players[current_player_idx % 2]
        if not player.is_alive:
            current_player_idx += 1
            continue
        opponent = players[(current_player_idx + 1) % 2]
        if not opponent.is_alive:
            current_player_idx += 1
            continue

        # Display turn and declared card type
        info = FONT.render(f"{player.name}'s Turn - Declare {current_card_type}", True, (255, 255, 255))
        screen.blit(info, (50, 20))

        # Draw hand and show selected count
        buttons = draw_hand(player, 100, selected_cards)
        selected_text = FONT.render(f"Selected: {len(selected_cards)} card(s)", True, (200, 200, 200))
        screen.blit(selected_text, (50, 180))

        # Draw "Play Selected Cards" button
        play_btn = pygame.Rect(50, 250, 280, 50)
        pygame.draw.rect(screen, (180, 180, 180), play_btn)
        play_text = FONT.render("Play Selected Cards", True, (0, 0, 0))
        screen.blit(play_text, (play_btn.x + (play_btn.width - play_text.get_width()) // 2, play_btn.y + 10))

        # Bluff decision buttons
        if stage == "waiting_bluff":
            conceal_rect = pygame.Rect(50, 100, len(player.hand) * 120, 50)
            pygame.draw.rect(screen, (50, 50, 50), conceal_rect)
            conceal_text = FONT.render("Cards Played - Hidden", True, (200, 200, 200))
            screen.blit(conceal_text, (60, 110))

            bluff_text = FONT.render(f"{opponent.name}, Call Bluff?", True, (255, 255, 255))
            screen.blit(bluff_text, (50, 320))

            bluff_btn = pygame.Rect(50, 370, 150, 50)
            pygame.draw.rect(screen, (255, 0, 0), bluff_btn)
            screen.blit(FONT.render("Call Bluff", True, (0, 0, 0)), (60, 380))

            pass_btn = pygame.Rect(220, 370, 150, 50)
            pygame.draw.rect(screen, (0, 255, 0), pass_btn)
            screen.blit(FONT.render("Pass", True, (0, 0, 0)), (250, 380))
        else:
            bluff_btn = pass_btn = None

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # Card selection and play
                if stage == "selecting":
                    for rect, card in buttons:
                        if rect.collidepoint(pos):
                            if card in selected_cards:
                                selected_cards.remove(card)
                            elif len(selected_cards) < 5:
                                selected_cards.append(card)

                    if play_btn.collidepoint(pos) and selected_cards:
                        stage = "waiting_bluff"

                # Bluff call or pass
                elif stage == "waiting_bluff":
                    if bluff_btn and bluff_btn.collidepoint(pos):
                        bluff_decision = True
                    elif pass_btn and pass_btn.collidepoint(pos):
                        bluff_decision = False

        # Evaluate bluff decision
        if bluff_decision is not None:
            if bluff_decision:
                # If any played card doesn't match declared type, player lied
                if any(card["type"] != current_card_type for card in selected_cards):
                    russian_roulette(player)
                    if not player.is_alive:
                        death_message = f"{player.name} has died."
                else:
                    # Opponent falsely accused — they risk death
                    russian_roulette(opponent)
                    if not opponent.is_alive:
                        death_message = f"{opponent.name} has died."
            else:
                print(f"{player.name}'s play accepted.")

            # Remove played cards
            for card in selected_cards:
                if card in player.hand:
                    player.hand.remove(card)

            # Refill hand if empty and still alive
            if not player.hand and player.is_alive:
                player.hand = [create_card(random.choice(CARD_TYPES)) for _ in range(5)]
                show_temporary_message(f"{player.name} draws a new hand!", 2)

            # Reset turn state
            selected_cards = []
            current_card_type = random.choice(CARD_TYPES)
            current_player_idx += 1
            stage = "selecting"
            bluff_decision = None

        clock.tick(30)  # Limit to 30 FPS

    # Quit the game cleanly
    pygame.quit()
    sys.exit()

# Start the game
if __name__ == "__main__":
    main()
