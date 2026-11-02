# Sam's Feline Adventures

**Developer:** Sam  
**Course:** Software Engineering / Game Development Final Project  

---

## Technical Description

### Third-Party Libraries and Dependencies
* **Pygame (`pygame`)**: The primary external library utilized for window creation, 2D vector mathematics (`pygame.math.Vector2`), event handling, surface blitting, clock management for fixed frame rates ($60\text{ FPS}$), audio mixing, and AABB/mask collision detection.
* **Python Standard Libraries (`os`, `sys`)**: Used for robust file system path resolution across directory trees and clean application exit calls.

### Code Structure (Object-Oriented Programming)
The application follows an Object-Oriented Programming (OOP) design pattern, organized into modular script files with clear separation of concerns:

* **`main.py` (`Platformer` Class):** Acts as the entry point and master controller. It initializes the Pygame window, runs the core game loop, monitors system events (`QUIT`, `KEYDOWN`, `KEYUP`), regulates frame timing via `pygame.time.Clock`, and renders background layers.
* **`world.py` (`World` Class):** Manages level layout data from `settings.py`, instantiates and groups sprite containers (`tiles`, `traps`, `player`, `goal`), calculates world-scrolling offsets (`_scroll_x`), and processes collision physics.
* **`player.py` (`Player` Class):** Inherits from `pygame.sprite.Sprite`. Manages Sam the Cat's movement states, gravity application, jump velocity, bounding box collision flags (`on_ground`, `on_ceiling`, `on_left`, `on_right`), and dynamic asset frame animations.
* **`tile.py` (`Tile` Class):** Inherits from `pygame.sprite.Sprite`. Represents terrain blocks rendered from `Sprites/terrain/ground.png`, supporting dynamic camera shifts.
* **`trap.py` (`Trap` Class):** Inherits from `pygame.sprite.Sprite`. Controls hazard animations from `Sprites/trap/` and triggers player health penalties upon collision.
* **`goal.py` (`Goal` Class):** Inherits from `pygame.sprite.Sprite`. Represents the target cupcake objective (`Sprites/goal/cupcakegoal.png`) that triggers level completion.
* **`game.py` (`Game` Class):** Manages high-level UI rendering, including HUD life counters (`Sprites/life/life.png`) and win/lose text overlays.
* **`support.py` (Utility Module):** Provides helper functions like `import_sprite()` to recursively parse sprite directories and load transparent PNG/GIF frames into memory safely.
* **`settings.py` (Configuration Module):** Defines global constants such as `WIDTH`, `HEIGHT`, `tile_size`, and the ASCII-based `world_map` level array.

### Architecture Diagram

![Architecture Diagram](SamsFelineAdventure.png)
