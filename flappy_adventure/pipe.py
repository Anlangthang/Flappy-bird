"""
Pipe module for Flappy Adventure

This module defines the pipe obstacles that the player must avoid.
"""

import pygame
import os
import random

class Pipe:
    """Pipe obstacle that the player must avoid"""
    
    def __init__(self, x, screen_width, screen_height, level):
        """Initialize the pipe"""
        self.x = x
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.level = level
        
        # Size
        self.width = 80
        self.gap_size = 180 - (level * 20)  # Gap gets smaller with higher levels
        
        # Position
        self.gap_y = random.randint(150, self.screen_height - 150)
        
        # Speed (increases with level)
        self.speed = 3 + (level * 0.5)
        
        # Scoring
        self.scored = False
        
        # Load sprites
        self.top_pipe, self.bottom_pipe = self.load_sprites()
        
        # Hitboxes
        self.top_hitbox = pygame.Rect(
            self.x, 
            0, 
            self.width, 
            self.gap_y
        )
        self.bottom_hitbox = pygame.Rect(
            self.x, 
            self.gap_y + self.gap_size, 
            self.width, 
            self.screen_height - (self.gap_y + self.gap_size)
        )
    
    def load_sprites(self):
        """Load pipe sprites with different colors based on level"""
        # Try to load pipe sprites from assets
        pipe_path = os.path.join('assets', 'pipe-green.png')
        if self.level == 2:
            pipe_path = os.path.join('assets', 'pipe-red.png')
        
        if os.path.exists(pipe_path):
            pipe_sprite = pygame.image.load(pipe_path).convert_alpha()
            pipe_sprite = pygame.transform.scale(pipe_sprite, (self.width, 500))
            
            # Create top pipe (flipped)
            top_pipe = pygame.transform.flip(pipe_sprite, False, True)
            bottom_pipe = pipe_sprite
        else:
            # Create fallback pipe sprites
            top_pipe = self.create_fallback_sprite(True)
            bottom_pipe = self.create_fallback_sprite(False)
        
        return top_pipe, bottom_pipe
    
    def create_fallback_sprite(self, is_top):
        """Create a fallback pipe sprite with pixel art style"""
        # Colors based on level
        if self.level == 1:
            main_color = (0, 200, 0)  # Green
            highlight_color = (0, 255, 0)
            shadow_color = (0, 150, 0)
        elif self.level == 2:
            main_color = (200, 0, 0)  # Red
            highlight_color = (255, 0, 0)
            shadow_color = (150, 0, 0)
        else:
            main_color = (0, 0, 200)  # Blue
            highlight_color = (0, 0, 255)
            shadow_color = (0, 0, 150)
        
        # Create pipe surface
        height = 500
        pipe = pygame.Surface((self.width, height), pygame.SRCALPHA)
        
        # Draw pipe body
        pygame.draw.rect(pipe, main_color, (0, 0, self.width, height))
        
        # Draw pipe edge (top or bottom depending on orientation)
        edge_height = 20
        if is_top:
            pygame.draw.rect(pipe, main_color, (0, height - edge_height, self.width, edge_height))
            pygame.draw.rect(pipe, highlight_color, (0, height - edge_height, self.width, 5))
            pygame.draw.rect(pipe, shadow_color, (0, height - 5, self.width, 5))
        else:
            pygame.draw.rect(pipe, main_color, (0, 0, self.width, edge_height))
            pygame.draw.rect(pipe, highlight_color, (0, 0, self.width, 5))
            pygame.draw.rect(pipe, shadow_color, (0, edge_height - 5, self.width, 5))
        
        # Add pixel art details
        for i in range(0, self.width, 10):
            if i % 20 == 0:
                if is_top:
                    pygame.draw.rect(pipe, highlight_color, (i, 0, 5, height - edge_height))
                    pygame.draw.rect(pipe, shadow_color, (i + 5, 0, 5, height - edge_height))
                else:
                    pygame.draw.rect(pipe, highlight_color, (i, edge_height, 5, height - edge_height))
                    pygame.draw.rect(pipe, shadow_color, (i + 5, edge_height, 5, height - edge_height))
        
        return pipe
    
    def update(self):
        """Update pipe position"""
        # Move pipe to the left
        self.x -= self.speed
        
        # Update hitboxes
        self.top_hitbox.x = self.x
        self.bottom_hitbox.x = self.x
    
    def collides_with(self, bird):
        """Check if the bird collides with this pipe"""
        return bird.hitbox.colliderect(self.top_hitbox) or bird.hitbox.colliderect(self.bottom_hitbox)
    
    def draw(self, screen):
        """Draw the pipe on the screen"""
        # Draw top pipe
        screen.blit(self.top_pipe, (self.x, self.gap_y - 500))
        
        # Draw bottom pipe
        screen.blit(self.bottom_pipe, (self.x, self.gap_y + self.gap_size))
        
        # Debug: draw hitboxes (uncomment for debugging)
        # pygame.draw.rect(screen, (255, 0, 0), self.top_hitbox, 1)
        # pygame.draw.rect(screen, (255, 0, 0), self.bottom_hitbox, 1)