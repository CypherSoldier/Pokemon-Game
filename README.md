# Catch That Pokémon!

## Description

"Catch That Pokémon!" is a simple yet exciting 2D game built using **Pygame**. The goal is to collect all Pokéballs on the map while avoiding enemies like Team Rocket and wild Pokémon. You control Ash and must navigate the environment strategically before time runs out!

## Features

- **Grid-Based Movement**: Move Ash using the arrow keys.
- **Time Limit**: Complete the game before the timer reaches zero.
- **Enemy AI**: Team Rocket and wild Pokémon move randomly to challenge you.
- **Simple Graphics**: Custom media assets (images) can be added.
- **Score System**: Gain points by collecting Pokéballs.
- **Game Over Scenarios**:
  - If time runs out.
  - If Ash collides with an enemy.
  - If all Pokéballs are collected, you win!

## Installation

1. Ensure you have Python installed (Python 3 recommended).
2. Install Pygame if you haven't already:
   ```bash
   pip install pygame
   ```
3. Place your media files (images) in the same directory as the script:
   - `floor.png`
   - `green_wall.png`
   - `pokeball.png`
   - `ash.png`
   - `cat.png`
   - `rocket.png`

## How to Play

1. Run the script:
   ```
   python catch_that_pokemon.py
   ```
2. Use the **arrow keys** to move Ash:
   - **Left Arrow**: Move left
   - **Right Arrow**: Move right
   - **Up Arrow**: Move up
   - **Down Arrow**: Move down
3. Avoid enemies and collect Pokéballs before the timer runs out.

- **Game Logic**:
  - The game runs at **30 FPS**.
  - Enemies move at regular intervals.
  - If all Pokéballs are collected, you win!
  - If Ash collides with an enemy, the game ends.
