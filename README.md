# Flappy-bird
![image](https://github.com/user-attachments/assets/05d9dab7-4b83-483f-9bd5-99a42e271531)

# Flappy Bird Game Design Document

A comprehensive GDD for a Flappy Bird game would include:

## 🤖 About The Game
• Simple side-scrolling game where players control a bird through 
obstacles
• One-touch gameplay mechanic (tap to make the bird flap and rise)
• Endless runner style with increasing difficulty
• Pixel art visual style with bright colors
![image](https://github.com/user-attachments/assets/08ad3eb7-f8f0-48ac-8935-e3de68bcc26e)

## 🚀 How to play it

1. Install pygame : pip install pygame
2. Clone the repository
3. Run the game : python3 main.py

## Game Structure
```
/flappy_adventure/
├── assets/
│   ├── images/
│   │   ├── bird/
│   │   │   ├── bird_frame1.png
│   │   │   ├── bird_frame2.png
│   │   │   └── bird_frame3.png
│   │   ├── background/
│   │   │   ├── background.png
│   │   │   ├── ground.png
│   │   │   └── clouds.png
│   │   ├── pipes/
│   │   │   ├── pipe_top.png
│   │   │   └── pipe_bottom.png
│   │   └── ui/
│   │       ├── title.png
│   │       ├── game_over.png
│   │       ├── medals.png
│   │       └── buttons.png
│   ├── audio/
│   │   ├── sfx/
│   │   │   ├── flap.wav
│   │   │   ├── score.wav
│   │   │   ├── hit.wav
│   │   │   └── die.wav
│   │   └── music/
│   │       └── background_music.mp3
│   └── fonts/
│       └── game_font.ttf
├── src/
│   ├── main.js
│   ├── game.js
│   ├── entities/
│   │   ├── bird.js
│   │   ├── pipe.js
│   │   └── ground.js
│   ├── scenes/
│   │   ├── title_scene.js
│   │   ├── game_scene.js
│   │   └── game_over_scene.js
│   ├── managers/
│   │   ├── asset_manager.js
│   │   ├── audio_manager.js
│   │   ├── score_manager.js
│   │   └── obstacle_manager.js
│   └── utils/
│       ├── physics.js
│       ├── collision.js
│       └── animation.js
├── index.html
├── style.css
└── config.js
```

## Core Mechanics
• Gravity pulls the bird downward constantly
• Each tap/click makes the bird flap upward briefly
• Bird moves at constant horizontal speed
• Pipes appear from right side of screen at regular intervals
• Collision with pipes or ground ends the game
• Score increases by 1 for each pipe successfully passed

## Visual Elements
• Bird character with simple animation (wing flapping)
• Green pipes as obstacles (inspired by Mario games)
• Scrolling background with parallax effect
• Simple UI showing current score and high score

## Audio Design
• Background music with cheerful, arcade-style tune
• Sound effects for:
  • Wing flap
  • Scoring points
  • Collision/game over
  • Menu interactions

## Game States
• Title screen
• Gameplay
• Game over screen with score and restart option
• Optional tutorial for first-time players

## Technical Requirements
• Target platforms: Mobile (iOS/Android) and web
• Portrait orientation
• Optimized for various screen sizes
• Simple save system for high scores

## Development Roadmap
• Core gameplay implementation
• Visual assets creation
• Audio integration
• UI and menus
• Testing and balancing
• Release and post-launch support

# How I build it 

## 

