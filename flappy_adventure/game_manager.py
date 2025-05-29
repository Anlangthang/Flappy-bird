"""
Game Manager module for Flappy Adventure

This module handles the overall game state, level progression,
and coordinates interactions between game objects.
"""

import pygame
import random
import os
import sys
import math
from enum import Enum
from bird import Bird
from pipe import Pipe
from power_up import PowerUp, PowerUpType
from enemy import Enemy
from ui import Button, Text

class GameState(Enum):
    """Enum for different game states"""
    MENU = 0
    PLAYING = 1
    GAME_OVER = 2
    PAUSED = 3
    LEVEL_COMPLETE = 4

class GameManager:
    """Manages the overall game state and coordinates game objects"""
    
    def __init__(self, screen, screen_width, screen_height):
        """Initialize the game manager"""
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.state = GameState.MENU
        self.current_level = 1
        self.max_levels = 3
        self.score = 0
        self.high_score = 0
        
        # Initialize pygame mixer for sound
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        # Load assets
        self.load_assets()
        
        # Create UI elements
        self.create_ui_elements()
        
        # Create game objects
        self.reset_game()
        
        # Set up timers
        self.enemy_spawn_timer = 0
        self.power_up_spawn_timer = 0
        self.enemy_spawn_interval = 5000  # milliseconds
        self.power_up_spawn_interval = 7000  # milliseconds
        
    def load_assets(self):
        """Load all game assets"""
        # Load backgrounds for different levels
        self.backgrounds = []
        bg_files = ['background-day.png', 'background-night.png']
        
        for i in range(self.max_levels):
            bg_file = bg_files[i % len(bg_files)]
            bg_path = os.path.join('assets', bg_file)
            
            if os.path.exists(bg_path):
                bg = pygame.image.load(bg_path).convert()
                bg = pygame.transform.scale(bg, (self.screen_width, self.screen_height))
                self.backgrounds.append(bg)
            else:
                self.backgrounds.append(self.create_fallback_background(i + 1))
        
        # Load retro Mario-style sound effects
        self.sounds = {
            'flap': self.load_sound('wing.wav'),      # Bird flap sound
            'score': self.load_sound('point.wav'),    # Passing obstacle sound
            'hit': self.load_sound('hit.wav'),        # Collision sound
            'power_up': self.load_sound('swoosh.wav'),  # Collecting item sound
            'level_complete': self.load_sound('point.wav'),  # Level complete sound (higher pitched)
            'game_over': self.load_sound('die.wav')   # Game over sound
        }
        
        # Adjust volume and pitch for retro feel
        if self.sounds['level_complete']:
            self.sounds['level_complete'].set_volume(0.8)
        if self.sounds['power_up']:
            self.sounds['power_up'].set_volume(0.7)
        
        # No background music tracks
    
    def create_fallback_background(self, level):
        """Create a fallback background if the image file doesn't exist"""
        bg = pygame.Surface((self.screen_width, self.screen_height))
        
        # Different colors for different levels
        if level == 1:
            bg.fill((135, 206, 235))  # Sky blue
        elif level == 2:
            bg.fill((255, 165, 0))    # Orange (sunset)
        else:
            bg.fill((25, 25, 112))    # Midnight blue (night)
            
        return bg
    
    def load_sound(self, filename):
        """Load a sound file with retro-style adjustments"""
        path = os.path.join('assets', filename)
        
        try:
            if os.path.exists(path):
                sound = pygame.mixer.Sound(path)
                
                # Set appropriate volume for retro Mario-style sounds
                if 'wing' in filename:  # Flap sound
                    sound.set_volume(0.5)
                elif 'point' in filename:  # Score/passing obstacle sound
                    sound.set_volume(0.7)
                elif 'hit' in filename:  # Collision sound
                    sound.set_volume(0.8)
                elif 'die' in filename:  # Game over sound
                    sound.set_volume(0.9)
                else:
                    sound.set_volume(0.6)
                    
                return sound
            else:
                return None
        except:
            return None  # Return None if sound loading fails
    
    def create_ui_elements(self):
        """Create UI elements for menus"""
        # Main menu buttons
        self.start_button = Button(
            self.screen_width // 2 - 100,
            self.screen_height // 2 - 25,
            200, 50, "Start Game", (100, 200, 100)
        )
        
        self.exit_button = Button(
            self.screen_width // 2 - 100,
            self.screen_height // 2 + 50,
            200, 50, "Exit", (200, 100, 100)
        )
        
        # Game over menu buttons
        self.restart_button = Button(
            self.screen_width // 2 - 100,
            self.screen_height // 2 + 25,
            200, 50, "Restart", (100, 200, 100)
        )
        
        self.menu_button = Button(
            self.screen_width // 2 - 100,
            self.screen_height // 2 + 100,
            200, 50, "Main Menu", (100, 100, 200)
        )
        
        # Text elements
        self.title_text = Text("Flappy Adventure", 48, (255, 255, 255), 
                              self.screen_width // 2, 100)
        
        self.score_text = Text("Score: 0", 24, (255, 255, 255), 
                              70, 30)
        
        self.high_score_text = Text(f"High Score: {self.high_score}", 24, (255, 255, 255), 
                                   self.screen_width - 100, 30)
        
        self.level_text = Text(f"Level: {self.current_level}", 24, (255, 255, 255), 
                              self.screen_width // 2, 30)
        
        # Lives counter
        self.lives_text = Text("Lives: 1", 24, (255, 255, 255),
                              70, 60)
        
        # Shield indicator
        self.shield_text = Text("Shield: None", 24, (255, 255, 255),
                               70, 90)
        
        self.game_over_text = Text("Game Over", 48, (255, 0, 0), 
                                  self.screen_width // 2, self.screen_height // 3)
        
        self.level_complete_text = Text("Level Complete!", 48, (0, 255, 0), 
                                       self.screen_width // 2, self.screen_height // 3)
    
    def reset_game(self):
        """Reset the game state for a new game"""
        # Create the player bird
        self.bird = Bird(100, self.screen_height // 2, self.screen_width, self.screen_height)
        # Give bird a reference to game manager for sound effects
        self.bird.game_manager = self
        
        # Initialize game object lists
        self.pipes = []
        self.power_ups = []
        self.enemies = []
        
        # Reset score for new game
        if self.state == GameState.MENU:
            self.score = 0
            self.current_level = 1
        
        # Set up initial pipes
        self.spawn_initial_pipes()
        
        # Reset timers
        self.enemy_spawn_timer = pygame.time.get_ticks()
        self.power_up_spawn_timer = pygame.time.get_ticks()
        
        # Start music for current level
        self.play_level_music()
    
    def play_level_music(self):
        """Initialize sound effects for the level (no background music)"""
        # No background music, just make sure mixer is initialized
        if not pygame.mixer.get_init():
            pygame.mixer.init()
    
    def spawn_initial_pipes(self):
        """Spawn the initial set of pipes"""
        pipe_spacing = 300  # Horizontal space between pipes
        for i in range(3):  # Start with 3 pipes
            x_pos = self.screen_width + (i * pipe_spacing)
            self.pipes.append(Pipe(x_pos, self.screen_width, self.screen_height, self.current_level))
    
    def handle_event(self, event):
        """Handle pygame events"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.state == GameState.PLAYING:
                    self.state = GameState.PAUSED
                elif self.state == GameState.PAUSED:
                    self.state = GameState.PLAYING
            
            if event.key == pygame.K_RETURN:
                if self.state == GameState.MENU:
                    self.state = GameState.PLAYING
                    self.reset_game()
                elif self.state == GameState.GAME_OVER:
                    self.state = GameState.MENU
                elif self.state == GameState.LEVEL_COMPLETE:
                    self.current_level += 1
                    if self.current_level > self.max_levels:
                        self.current_level = 1
                    self.state = GameState.PLAYING
                    self.reset_game()
            
            # Bird flap controls
            if self.state == GameState.PLAYING:
                if event.key in (pygame.K_SPACE, pygame.K_UP):
                    self.bird.flap()
                    if self.sounds['flap']:
                        self.sounds['flap'].play()
        
        # Mouse controls
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if self.state == GameState.PLAYING:
                self.bird.flap()
                if self.sounds['flap']:
                    self.sounds['flap'].play()
            
            elif self.state == GameState.MENU:
                if self.start_button.is_clicked(mouse_pos):
                    self.state = GameState.PLAYING
                    self.reset_game()
                elif self.exit_button.is_clicked(mouse_pos):
                    pygame.quit()
                    sys.exit()
            
            elif self.state == GameState.GAME_OVER:
                if self.restart_button.is_clicked(mouse_pos):
                    self.state = GameState.PLAYING
                    self.score = 0
                    self.reset_game()
                elif self.menu_button.is_clicked(mouse_pos):
                    self.state = GameState.MENU
    
    def update(self):
        """Update game state"""
        if self.state == GameState.PLAYING:
            # Update bird
            self.bird.update()
            
            # Update pipes
            for pipe in self.pipes[:]:
                pipe.update()
                
                # Check if pipe is passed
                if not pipe.scored and pipe.x + pipe.width < self.bird.x:
                    self.score += 1
                    pipe.scored = True
                    # Play score sound
                    if self.sounds['score']:
                        self.sounds['score'].play()
                    # Update score display
                    self.score_text.update_text(f"Score: {self.score}")
                
                # Remove pipes that are off screen
                if pipe.x + pipe.width < 0:
                    self.pipes.remove(pipe)
                    # Add a new pipe
                    new_x = max([p.x for p in self.pipes]) + 300
                    self.pipes.append(Pipe(new_x, self.screen_width, self.screen_height, self.current_level))
            
            # Update power-ups
            for power_up in self.power_ups[:]:
                power_up.update()
                
                # Check for collision with bird
                if power_up.collides_with(self.bird):
                    self.apply_power_up(power_up)
                    self.power_ups.remove(power_up)
                    if self.sounds['power_up']:
                        self.sounds['power_up'].play()
                
                # Remove power-ups that are off screen
                if power_up.x + power_up.width < 0:
                    self.power_ups.remove(power_up)
            
            # Update enemies
            for enemy in self.enemies[:]:
                enemy.update()
                
                # Check for collision with bird
                if enemy.collides_with(self.bird) and not self.bird.invincible:
                    self.game_over()
                
                # Remove enemies that are off screen
                if enemy.x + enemy.width < 0:
                    self.enemies.remove(enemy)
            
            # Check for collisions with pipes
            for pipe in self.pipes:
                if pipe.collides_with(self.bird) and not self.bird.invincible:
                    self.game_over()
            
            # Check if bird is out of bounds
            if self.bird.y < 0 or self.bird.y > self.screen_height:
                self.game_over()
            
            # Spawn enemies and power-ups
            self.spawn_enemies()
            self.spawn_power_ups()
            
            # Check for level completion
            if self.score >= 10 * self.current_level:
                self.complete_level()
            
            # Update UI text
            self.score_text.update_text(f"Score: {self.score}")
            self.level_text.update_text(f"Level: {self.current_level}")
            self.high_score_text.update_text(f"High Score: {self.high_score}")
    
    def spawn_enemies(self):
        """Spawn enemy birds periodically"""
        current_time = pygame.time.get_ticks()
        if current_time - self.enemy_spawn_timer > self.enemy_spawn_interval:
            # Adjust spawn rate based on level
            spawn_chance = 0.3 * self.current_level
            if random.random() < spawn_chance:
                y_pos = random.randint(100, self.screen_height - 100)
                self.enemies.append(Enemy(self.screen_width, y_pos, self.screen_width, self.screen_height, self.current_level))
            self.enemy_spawn_timer = current_time
    
    def spawn_power_ups(self):
        """Spawn power-ups periodically"""
        current_time = pygame.time.get_ticks()
        if current_time - self.power_up_spawn_timer > self.power_up_spawn_interval:
            # Adjust spawn rate based on level
            spawn_chance = 0.4 - (0.05 * self.current_level)  # Less power-ups in higher levels
            if random.random() < spawn_chance:
                y_pos = random.randint(100, self.screen_height - 100)
                
                # Choose a power-up type with weighted probabilities
                # Hearts are rarer than other power-ups
                weights = [0.4, 0.4, 0.2]  # Speed, Shield, Heart
                power_up_types = list(PowerUpType)
                
                # Choose based on weights
                rand = random.random()
                cumulative = 0
                chosen_type = power_up_types[0]
                
                for i, weight in enumerate(weights):
                    cumulative += weight
                    if rand <= cumulative:
                        chosen_type = power_up_types[i]
                        break
                
                self.power_ups.append(PowerUp(self.screen_width, y_pos, chosen_type))
            self.power_up_spawn_timer = current_time
    
    def apply_power_up(self, power_up):
        """Apply the effect of a power-up with retro sound effect"""
        # Play power-up sound with retro feel
        if self.sounds['power_up']:
            # Play the sound effect with slight delay for better feedback
            pygame.time.delay(50)
            self.sounds['power_up'].play()
            
        if power_up.type == PowerUpType.SPEED:
            self.bird.apply_speed_boost()
            # Lightning allows passing through obstacles temporarily
            self.bird.apply_invincibility()
        elif power_up.type == PowerUpType.INVINCIBILITY:
            # Shield protects from one hit
            self.bird.has_shield = True
        elif power_up.type == PowerUpType.EXTRA_LIFE:
            # Heart grants +1 life
            self.bird.lives += 1
            # Show life count on screen
            self.lives_text.update_text(f"Lives: {self.bird.lives}")
            # Play score sound for extra life
            if self.sounds['score']:
                pygame.time.delay(100)  # Small delay for better audio feedback
                self.sounds['score'].play()
    
    def game_over(self):
        """Handle game over state with retro sound effects"""
        # Check if player has shield
        if self.bird.has_shield:
            # Use shield to prevent death
            self.bird.has_shield = False
            if self.sounds['power_up']:
                self.sounds['power_up'].play()
            return
            
        # Check if player has extra lives
        if self.bird.lives > 1:
            # Use a life and continue playing
            self.bird.lives -= 1
            self.lives_text.update_text(f"Lives: {self.bird.lives}")
            
            # Reset bird position but keep the game going
            self.bird.y = self.screen_height // 2
            self.bird.velocity = 0
            
            # Play hit sound
            if self.sounds['hit']:
                self.sounds['hit'].play()
            
            return
            
        # No lives left, game over
        # Play hit sound first (collision)
        if self.sounds['hit']:
            self.sounds['hit'].play()
            
        # Wait a short moment before playing game over sound (classic retro timing)
        pygame.time.delay(700)
        
        # Play game over sound with retro feel
        if self.sounds['game_over']:
            self.sounds['game_over'].play()
        
        # Update high score
        if self.score > self.high_score:
            self.high_score = self.score
            self.high_score_text.update_text(f"High Score: {self.high_score}")
            
            # Play score sound for new high score
            if self.sounds['score']:
                pygame.time.delay(1000)  # Wait for game over sound to finish
                self.sounds['score'].play()
        
        self.state = GameState.GAME_OVER
    
    def complete_level(self):
        """Handle level completion"""
        # Play level complete sound
        if self.sounds['level_complete']:
            self.sounds['level_complete'].play()
        
        self.state = GameState.LEVEL_COMPLETE
    
    def draw(self):
        """Draw the game state"""
        # Draw background based on current level
        self.screen.blit(self.backgrounds[self.current_level - 1], (0, 0))
        
        if self.state == GameState.MENU:
            # Draw menu
            self.title_text.draw(self.screen)
            self.start_button.draw(self.screen)
            self.exit_button.draw(self.screen)
            self.high_score_text.draw(self.screen)
        
        elif self.state == GameState.PLAYING or self.state == GameState.PAUSED:
            # Draw game objects
            for pipe in self.pipes:
                pipe.draw(self.screen)
            
            for power_up in self.power_ups:
                power_up.draw(self.screen)
            
            for enemy in self.enemies:
                enemy.draw(self.screen)
            
            self.bird.draw(self.screen)
            
            # Draw UI
            self.score_text.draw(self.screen)
            self.high_score_text.draw(self.screen)
            self.level_text.draw(self.screen)
            self.lives_text.draw(self.screen)
            
            # Update shield text
            shield_status = "Active" if self.bird.has_shield else "None"
            self.shield_text.update_text(f"Shield: {shield_status}")
            self.shield_text.draw(self.screen)
            
            # Draw pause overlay
            if self.state == GameState.PAUSED:
                # Semi-transparent overlay
                overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 128))
                self.screen.blit(overlay, (0, 0))
                
                # Pause text
                pause_text = Text("PAUSED", 48, (255, 255, 255), 
                                 self.screen_width // 2, self.screen_height // 2)
                pause_text.draw(self.screen)
                
                # Instructions
                instructions = Text("Press ESC to resume", 24, (255, 255, 255), 
                                   self.screen_width // 2, self.screen_height // 2 + 50)
                instructions.draw(self.screen)
        
        elif self.state == GameState.GAME_OVER:
            # Draw game over screen
            self.game_over_text.draw(self.screen)
            
            final_score = Text(f"Final Score: {self.score}", 36, (255, 255, 255), 
                              self.screen_width // 2, self.screen_height // 2 - 50)
            final_score.draw(self.screen)
            
            self.restart_button.draw(self.screen)
            self.menu_button.draw(self.screen)
        
        elif self.state == GameState.LEVEL_COMPLETE:
            # Draw level complete screen
            self.level_complete_text.draw(self.screen)
            
            if self.current_level < self.max_levels:
                next_level = Text(f"Press ENTER for Level {self.current_level + 1}", 36, (255, 255, 255), 
                                 self.screen_width // 2, self.screen_height // 2)
            else:
                next_level = Text("You've completed all levels! Press ENTER to restart", 24, (255, 255, 255), 
                                 self.screen_width // 2, self.screen_height // 2)
            
            next_level.draw(self.screen)
            
            level_score = Text(f"Level Score: {self.score}", 36, (255, 255, 255), 
                              self.screen_width // 2, self.screen_height // 2 - 50)
            level_score.draw(self.screen)