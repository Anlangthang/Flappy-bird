"""
Power-up module for Flappy Adventure

This module defines the power-ups that the player can collect.
"""

import pygame
import os
from enum import Enum

class PowerUpType(Enum):
    """Types of power-ups"""
    SPEED = 0       # Lightning - increases speed and allows passing through obstacles
    INVINCIBILITY = 1  # Shield - protects from one hit
    EXTRA_LIFE = 2  # Heart - grants +1 life

class PowerUp:
    """Power-up that the player can collect"""
    
    def __init__(self, x, y, power_up_type):
        """Initialize the power-up"""
        self.x = x
        self.y = y
        self.type = power_up_type
        
        # Size
        self.width = 30
        self.height = 30
        
        # Speed
        self.speed = 3
        
        # Animation
        self.sprite = self.create_sprite()
        self.animation_counter = 0
        self.pulse_direction = 1
        
        # Hitbox
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def create_sprite(self):
        """Create a sprite for the power-up"""
        sprite = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Different colors and shapes based on power-up type
        if self.type == PowerUpType.SPEED:
            # Lightning bolt (yellow)
            color = (255, 255, 0)  # Bright yellow
            
            # Draw lightning bolt
            points = [
                (15, 0),
                (20, 10),
                (25, 10),
                (15, 20),
                (20, 20),
                (10, 30),
                (15, 15),
                (10, 15)
            ]
            pygame.draw.polygon(sprite, color, points)
            pygame.draw.polygon(sprite, (255, 255, 255), points, 1)  # White outline
            
        elif self.type == PowerUpType.INVINCIBILITY:
            # Shield (blue)
            color = (0, 191, 255)  # Deep sky blue
            
            # Draw shield
            pygame.draw.circle(sprite, color, (15, 15), 12)
            pygame.draw.circle(sprite, (255, 255, 255), (15, 15), 12, 2)  # White outline
            pygame.draw.line(sprite, (255, 255, 255), (15, 5), (15, 25), 2)  # Vertical line
            pygame.draw.line(sprite, (255, 255, 255), (5, 15), (25, 15), 2)  # Horizontal line
            
        else:  # EXTRA_LIFE
            # Heart (red)
            color = (255, 0, 0)  # Red
            
            # Draw heart
            pygame.draw.circle(sprite, color, (10, 10), 7)  # Left circle
            pygame.draw.circle(sprite, color, (20, 10), 7)  # Right circle
            points = [(5, 12), (15, 25), (25, 12)]
            pygame.draw.polygon(sprite, color, points)  # Bottom triangle
        
        return sprite
    
    def update(self):
        """Update power-up position and animation"""
        # Move power-up to the left
        self.x -= self.speed
        
        # Update hitbox
        self.hitbox.x = self.x
        self.hitbox.y = self.y
        
        # Animate (pulsating effect)
        self.animation_counter += 0.1 * self.pulse_direction
        if self.animation_counter >= 1.0:
            self.pulse_direction = -1
        elif self.animation_counter <= 0.0:
            self.pulse_direction = 1
    
    def collides_with(self, bird):
        """Check if the bird collides with this power-up"""
        return bird.hitbox.colliderect(self.hitbox)
    
    def draw(self, screen):
        """Draw the power-up on the screen"""
        # Apply pulsating effect
        scale = 1.0 + 0.2 * self.animation_counter
        scaled_width = int(self.width * scale)
        scaled_height = int(self.height * scale)
        scaled_sprite = pygame.transform.scale(self.sprite, (scaled_width, scaled_height))
        
        # Center the scaled sprite
        x_offset = (scaled_width - self.width) // 2
        y_offset = (scaled_height - self.height) // 2
        
        screen.blit(scaled_sprite, (self.x - x_offset, self.y - y_offset))