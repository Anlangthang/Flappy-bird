"""
UI module for Flappy Adventure

This module defines UI elements like buttons and text.
"""

import pygame

class Button:
    """Button UI element"""
    
    def __init__(self, x, y, width, height, text, color, hover_color=None):
        """Initialize the button"""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.hover_color = hover_color or self.lighten_color(color, 30)
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.SysFont('Arial', 24)
        
        # Pixel art styling
        self.border_width = 4
        self.shadow_offset = 4
        self.is_hovered = False
    
    def lighten_color(self, color, amount):
        """Lighten a color by the given amount"""
        r = min(255, color[0] + amount)
        g = min(255, color[1] + amount)
        b = min(255, color[2] + amount)
        return (r, g, b)
    
    def darken_color(self, color, amount):
        """Darken a color by the given amount"""
        r = max(0, color[0] - amount)
        g = max(0, color[1] - amount)
        b = max(0, color[2] - amount)
        return (r, g, b)
    
    def is_clicked(self, mouse_pos):
        """Check if the button is clicked"""
        return self.rect.collidepoint(mouse_pos)
    
    def update(self, mouse_pos):
        """Update button state based on mouse position"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
    
    def draw(self, screen):
        """Draw the button on the screen"""
        # Draw button shadow (pixel art style)
        shadow_rect = pygame.Rect(
            self.x + self.shadow_offset, 
            self.y + self.shadow_offset, 
            self.width, 
            self.height
        )
        pygame.draw.rect(screen, self.darken_color(self.color, 50), shadow_rect)
        
        # Draw button background
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        
        # Draw pixel art border
        border_color = self.lighten_color(color, 50)
        pygame.draw.rect(screen, border_color, self.rect, self.border_width)
        
        # Draw button text
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
        # Update hover state based on mouse position
        mouse_pos = pygame.mouse.get_pos()
        self.update(mouse_pos)

class Text:
    """Text UI element"""
    
    def __init__(self, text, size, color, x, y):
        """Initialize the text"""
        self.text = text
        self.size = size
        self.color = color
        self.x = x
        self.y = y
        self.font = pygame.font.SysFont('Arial', size)
        self.surface = self.font.render(text, True, color)
        self.rect = self.surface.get_rect(center=(x, y))
        
        # Pixel art styling
        self.shadow_offset = 2
        self.shadow_color = (0, 0, 0)
    
    def update_text(self, new_text):
        """Update the text content"""
        self.text = new_text
        self.surface = self.font.render(new_text, True, self.color)
        self.rect = self.surface.get_rect(center=(self.x, self.y))
    
    def draw(self, screen):
        """Draw the text on the screen"""
        # Draw text shadow for pixel art style
        shadow_surface = self.font.render(self.text, True, self.shadow_color)
        shadow_rect = shadow_surface.get_rect(
            center=(self.x + self.shadow_offset, self.y + self.shadow_offset)
        )
        screen.blit(shadow_surface, shadow_rect)
        
        # Draw main text
        screen.blit(self.surface, self.rect)