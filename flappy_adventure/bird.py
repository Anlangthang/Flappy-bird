"""
Bird module for Flappy Adventure

This module defines the player-controlled bird character.
"""

import pygame
import os

class Bird:
    """Player-controlled bird character"""
    
    def __init__(self, x, y, screen_width, screen_height):
        """Initialize the bird"""
        self.x = x
        self.y = y
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.game_manager = None  # Reference to game manager for sound effects
        
        # Lives
        self.lives = 1
        
        # Shield status
        self.has_shield = False
        
        # Physics properties
        self.velocity = 0
        self.gravity = 0.5
        self.flap_strength = -8
        self.terminal_velocity = 10
        
        # Size
        self.width = 40
        self.height = 30
        
        # Animation
        self.sprites = self.load_sprites()
        self.current_sprite = 0
        self.animation_speed = 0.2
        self.animation_counter = 0
        
        # Power-up states
        self.invincible = False
        self.speed_boost = False
        self.invincibility_timer = 0
        self.speed_boost_timer = 0
        self.power_up_duration = 5000  # 5 seconds
        
        # Hitbox (slightly smaller than the sprite for better gameplay)
        self.hitbox = pygame.Rect(self.x, self.y, self.width - 10, self.height - 10)
    
    def load_sprites(self):
        """Load bird sprites"""
        sprites = []
        
        # Try to load sprites from assets
        sprite_names = ['yellowbird-upflap.png', 'yellowbird-midflap.png', 'yellowbird-downflap.png']
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
        """Create a cute pixel art bird sprite"""
        sprite = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Default colors
        main_color = (255, 255, 0)  # Yellow
        accent_color = (255, 165, 0)  # Orange
        
        # Pixel art bird with bright colors
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
        
        # Draw pixel art bird
        pixel_size = 2
        colors = {
            'M': main_color,       # Main color
            'W': (255, 255, 255),  # White
            'A': accent_color,     # Accent color
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
        
        # Draw eyes (black)
        pygame.draw.rect(sprite, colors['B'], (self.width - 12, self.height // 3 - 2, 4, 4))
        
        # Draw beak (orange)
        beak_pixels = [
            (self.width - 6, self.height // 2 - 3, 6, 2),
            (self.width - 6, self.height // 2, 6, 2),
            (self.width - 6, self.height // 2 + 3, 6, 2)
        ]
        for x, y, w, h in beak_pixels:
            pygame.draw.rect(sprite, accent_color, (x, y, w, h))
        
        return sprite
    
    def flap(self):
        """Make the bird flap upward"""
        self.velocity = self.flap_strength
        
        # Play flap sound if available
        if self.game_manager and self.game_manager.sounds and 'flap' in self.game_manager.sounds:
            if self.game_manager.sounds['flap']:
                self.game_manager.sounds['flap'].play()
    
    def update(self):
        """Update bird position and state"""
        # Apply gravity
        self.velocity += self.gravity
        
        # Cap terminal velocity
        if self.velocity > self.terminal_velocity:
            self.velocity = self.terminal_velocity
        
        # Update position
        self.y += self.velocity
        
        # Update hitbox position
        self.hitbox.x = self.x + 5  # Offset hitbox to be centered in sprite
        self.hitbox.y = self.y + 5
        
        # Update animation
        self.animation_counter += self.animation_speed
        if self.animation_counter >= len(self.sprites):
            self.animation_counter = 0
        self.current_sprite = int(self.animation_counter)
        
        # Update power-up timers
        current_time = pygame.time.get_ticks()
        
        if self.invincible:
            if current_time - self.invincibility_timer > self.power_up_duration:
                self.invincible = False
        
        if self.speed_boost:
            if current_time - self.speed_boost_timer > self.power_up_duration:
                self.speed_boost = False
                self.flap_strength = -8  # Reset flap strength
    
    def apply_invincibility(self):
        """Apply invincibility power-up"""
        self.invincible = True
        self.invincibility_timer = pygame.time.get_ticks()
    
    def apply_speed_boost(self):
        """Apply speed boost power-up"""
        self.speed_boost = True
        self.speed_boost_timer = pygame.time.get_ticks()
        self.flap_strength = -12  # Stronger flap
    
    def draw(self, screen):
        """Draw the bird on the screen"""
        # Get the current sprite
        sprite = self.sprites[self.current_sprite]
        
        # Apply visual effects for power-ups
        if self.invincible:
            # Create a copy of the sprite with a blue tint for invincibility
            tinted_sprite = sprite.copy()
            blue_overlay = pygame.Surface(sprite.get_size(), pygame.SRCALPHA)
            blue_overlay.fill((0, 0, 255, 100))
            tinted_sprite.blit(blue_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
            
            # Pulsating effect
            pulse = (pygame.time.get_ticks() % 500) / 500.0
            scale_factor = 1.0 + 0.2 * pulse
            scaled_width = int(self.width * scale_factor)
            scaled_height = int(self.height * scale_factor)
            scaled_sprite = pygame.transform.scale(tinted_sprite, (scaled_width, scaled_height))
            
            # Center the scaled sprite
            x_offset = (scaled_width - self.width) // 2
            y_offset = (scaled_height - self.height) // 2
            
            screen.blit(scaled_sprite, (self.x - x_offset, self.y - y_offset))
        
        elif self.speed_boost:
            # Create a copy of the sprite with a yellow trail for speed boost
            screen.blit(sprite, (self.x, self.y))
            
            # Draw speed lines
            for i in range(1, 4):
                trail_sprite = sprite.copy()
                trail_sprite.set_alpha(100 - i * 30)  # Fade out
                screen.blit(trail_sprite, (self.x - i * 10, self.y))
        
        else:
            # Normal drawing
            screen.blit(sprite, (self.x, self.y))
        
        # Draw shield effect if active
        if self.has_shield:
            shield_surface = pygame.Surface((self.width + 10, self.height + 10), pygame.SRCALPHA)
            pygame.draw.circle(shield_surface, (0, 191, 255, 100), (self.width // 2 + 5, self.height // 2 + 5), self.width // 2 + 5)
            pygame.draw.circle(shield_surface, (255, 255, 255, 150), (self.width // 2 + 5, self.height // 2 + 5), self.width // 2 + 5, 2)
            screen.blit(shield_surface, (self.x - 5, self.y - 5))