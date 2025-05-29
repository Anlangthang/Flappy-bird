"""
Enemy module for Flappy Adventure

This module defines the enemy birds that the player must avoid.
"""

import pygame
import os
import random
import math

class Enemy:
    """Enemy bird that the player must avoid"""
    
    def __init__(self, x, y, screen_width, screen_height, level):
        """Initialize the enemy"""
        self.x = x
        self.y = y
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.level = level
        
        # Size
        self.width = 40
        self.height = 30
        
        # Speed (increases with level)
        self.base_speed = 4 + (level * 0.5)
        self.speed = self.base_speed
        
        # Movement pattern (different patterns based on level)
        self.pattern = random.choice(['straight', 'sine', 'chase'])
        self.pattern_offset = 0
        self.amplitude = random.randint(30, 80)
        self.frequency = random.uniform(0.02, 0.05)
        
        # Animation
        self.sprites = self.load_sprites()
        self.current_sprite = 0
        self.animation_speed = 0.2
        self.animation_counter = 0
        
        # Hitbox
        self.hitbox = pygame.Rect(self.x, self.y, self.width - 10, self.height - 10)
    
    def load_sprites(self):
        """Load enemy sprites"""
        sprites = []
        
        # Try to load sprites from assets
        if self.level == 1:
            sprite_names = ['redbird-upflap.png', 'redbird-midflap.png', 'redbird-downflap.png']
        else:
            sprite_names = ['bluebird-upflap.png', 'bluebird-midflap.png', 'bluebird-downflap.png']
            
        for name in sprite_names:
            sprite_path = os.path.join('assets', name)
            
            if os.path.exists(sprite_path):
                sprite = pygame.image.load(sprite_path).convert_alpha()
                sprites.append(pygame.transform.scale(sprite, (self.width, self.height)))
            else:
                # Create a fallback sprite
                sprite = self.create_fallback_sprite(len(sprites))
                sprites.append(sprite)
        
        return sprites
    
    def create_fallback_sprite(self, index):
        """Create a fallback enemy sprite with pixel art style"""
        sprite = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Different colors based on level
        if self.level == 1:
            main_color = (255, 0, 0)  # Red
            accent_color = (200, 0, 0)
        else:
            main_color = (0, 0, 255)  # Blue
            accent_color = (0, 0, 200)
        
        # Pixel art bird with evil look
        if index == 0:  # Wings up position
            # Bird body
            pixel_art = [
                "    MMMMM     ",
                "   MWWWWMM    ",
                "  MWWWWWWMM   ",
                " MWWWWWWWWMM  ",
                "MWWWWWWWWWWMM ",
                "MWWWWWWWWWWMM ",
                "MWWWWWWWWWWMM ",
                " MWWWWWWWWMM  ",
                "  MWWWWWWMM   ",
                "   MWWWWMM    ",
                "    MMMMM     "
            ]
            # Wings up
            wings = [
                "AA            ",
                "AAAA          ",
                "AAAAAA        ",
                "AAAA          ",
                "AA            "
            ]
        elif index == 1:  # Wings middle position
            # Bird body (same as above)
            pixel_art = [
                "    MMMMM     ",
                "   MWWWWMM    ",
                "  MWWWWWWMM   ",
                " MWWWWWWWWMM  ",
                "MWWWWWWWWWWMM ",
                "MWWWWWWWWWWMM ",
                "MWWWWWWWWWWMM ",
                " MWWWWWWWWMM  ",
                "  MWWWWWWMM   ",
                "   MWWWWMM    ",
                "    MMMMM     "
            ]
            # Wings middle
            wings = [
                "              ",
                "AA            ",
                "AAAA          ",
                "AAAAAA        ",
                "AAAA          "
            ]
        else:  # Wings down position
            # Bird body (same as above)
            pixel_art = [
                "    MMMMM     ",
                "   MWWWWMM    ",
                "  MWWWWWWMM   ",
                " MWWWWWWWWMM  ",
                "MWWWWWWWWWWMM ",
                "MWWWWWWWWWWMM ",
                "MWWWWWWWWWWMM ",
                " MWWWWWWWWMM  ",
                "  MWWWWWWMM   ",
                "   MWWWWMM    ",
                "    MMMMM     "
            ]
            # Wings down
            wings = [
                "              ",
                "              ",
                "AA            ",
                "AAAA          ",
                "AAAAAA        "
            ]
        
        # Draw pixel art enemy bird
        pixel_size = 2
        colors = {
            'M': main_color,
            'W': (255, 255, 255),  # White
            'A': accent_color,
            'B': (0, 0, 0)         # Black
        }
        
        # Draw body
        for y, row in enumerate(pixel_art):
            for x, col in enumerate(row):
                if col != ' ':
                    pygame.draw.rect(
                        sprite, 
                        colors[col], 
                        (x * pixel_size, y * pixel_size, pixel_size, pixel_size)
                    )
        
        # Draw wings
        for y, row in enumerate(wings):
            for x, col in enumerate(row):
                if col != ' ':
                    pygame.draw.rect(
                        sprite, 
                        colors[col], 
                        (x * pixel_size, (y + 3) * pixel_size, pixel_size, pixel_size)
                    )
        
        # Draw angry eyes (black)
        pygame.draw.rect(sprite, colors['B'], (self.width - 12, self.height // 3 - 3, 4, 2))
        pygame.draw.rect(sprite, colors['B'], (self.width - 12, self.height // 3, 4, 2))
        
        # Draw sharp beak
        beak_pixels = [
            (self.width - 4, self.height // 2 - 4, 4, 2),
            (self.width - 6, self.height // 2 - 2, 6, 2),
            (self.width - 4, self.height // 2, 4, 2),
            (self.width - 6, self.height // 2 + 2, 6, 2),
            (self.width - 4, self.height // 2 + 4, 4, 2)
        ]
        for x, y, w, h in beak_pixels:
            pygame.draw.rect(sprite, accent_color, (x, y, w, h))
        
        return sprite
    
    def update(self):
        """Update enemy position and animation"""
        # Move enemy to the left
        self.x -= self.speed
        
        # Apply movement pattern
        if self.pattern == 'sine':
            # Sinusoidal movement
            self.pattern_offset += self.frequency
            self.y = self.y + math.sin(self.pattern_offset) * 2
            
        elif self.pattern == 'chase' and random.random() < 0.05:
            # Occasionally adjust y position to "chase" the player
            # (In a real game, you would pass the player's position)
            target_y = random.randint(100, self.screen_height - 100)
            if self.y < target_y:
                self.y += 2
            else:
                self.y -= 2
        
        # Keep enemy within screen bounds
        if self.y < 0:
            self.y = 0
        elif self.y > self.screen_height - self.height:
            self.y = self.screen_height - self.height
        
        # Update hitbox
        self.hitbox.x = self.x + 5
        self.hitbox.y = self.y + 5
        
        # Update animation
        self.animation_counter += self.animation_speed
        if self.animation_counter >= len(self.sprites):
            self.animation_counter = 0
        self.current_sprite = int(self.animation_counter)
    
    def collides_with(self, bird):
        """Check if the bird collides with this enemy"""
        return bird.hitbox.colliderect(self.hitbox)
    
    def draw(self, screen):
        """Draw the enemy on the screen"""
        # Get the current sprite
        sprite = self.sprites[self.current_sprite]
        
        # Draw the enemy
        screen.blit(sprite, (self.x, self.y))
        
        # Debug: draw hitbox (uncomment for debugging)
        # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 1)