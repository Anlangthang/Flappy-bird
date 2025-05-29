#!/usr/bin/env python3
"""
- Flappy Adventure - 

This game features:
- Multiple levels with increasing difficulty
- Power-ups (speed boosts, invincibility, coin multipliers)
- Enemy birds to avoid
- Detailed scoring system
- Sound effects and background music (Mario style!)
- Smooth animations with sprite sheets
- Game menus (start, game over, restart)
- Support for keyboard and touch input

Controls:
- SPACE/UP/MOUSE CLICK: Flap the bird
- ESC: Pause game
- ENTER: Select menu options

To run the game:
    python main.py
"""

import pygame
import sys
import os
from game_manager import GameManager

# Initialize pygame
pygame.init()
pygame.mixer.init()  # Ensure audio is initialized

# Set up the display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Adventure - Pixel Art Style")

# Set up the clock
clock = pygame.time.Clock()
FPS = 60

def main():
    """Main function to run the game"""
    # Create game manager
    game_manager = GameManager(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            game_manager.handle_event(event)
        
        # Update game state
        game_manager.update()
        
        # Draw everything
        game_manager.draw()
        
        # Update the display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(FPS)
    
    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
