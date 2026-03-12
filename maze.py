#!/usr/bin/env python3
"""
Terminal Maze - Enhanced Edition v2.0
Generate and solve mazes in your terminal
Author: Sagar Jadhav
Version: 2.0 - Optimized & Enhanced
"""

import os
import random
import sys
import time
import keyboard

WALL = '██'
PATH = '  '
PLAYER = '🙂'
EXIT = '🚪'
VISITED = '· '
TREASURE = '💎'

class MazeGame:
    """Enhanced Maze Game"""
    
    def __init__(self, width=21, height=11):
        self.width = width
        self.height = height
        self.maze = [[WALL for _ in range(width)] for _ in range(height)]
        self.player_pos = [1, 1]
        self.exit_pos = [height - 2, width - 2]
        self.visited = set()
        self.treasures = []
        self.score = 0
        self.start_time = None
        self.moves = 0
        self.generate()
        self.place_treasures()
    
    def generate(self):
        """Generate maze using recursive backtracking"""
        self.maze = [[WALL for _ in range(self.width)] for _ in range(self.height)]
        
        def carve(x, y):
            self.maze[y][x] = PATH
            directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 < nx < self.width - 1 and 0 < ny < self.height - 1:
                    if self.maze[ny][nx] == WALL:
                        self.maze[y + dy//2][x + dx//2] = PATH
                        carve(nx, ny)
        
        carve(1, 1)
        self.maze[self.exit_pos[0]][self.exit_pos[1]] = EXIT
    
    def place_treasures(self):
        """Place treasure chests in the maze"""
        empty_cells = []
        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                if self.maze[y][x] == PATH and [y, x] != self.player_pos and [y, x] != self.exit_pos:
                    empty_cells.append((y, x))
        
        # Place 3-5 treasures
        num_treasures = random.randint(3, min(5, len(empty_cells) // 10))
        self.treasures = random.sample(empty_cells, num_treasures)
    
    def draw(self):
        """Draw the maze"""
        os.system('clear')
        
        # Title
        print(f"\n  \033[1;36m╔{'═' * (self.width + 2)}╗")
        print(f"  ║  🧩 MAZE v2.0  ║")
        print(f"  ╚{'═' * (self.width + 2)}╝\033[0m\n")
        
        # Maze
        for y, row in enumerate(self.maze):
            line = "  "
            for x, cell in enumerate(row):
                if [y, x] == self.player_pos:
                    line += f"\033[1;32m{PLAYER}\033[0m"
                elif [y, x] == self.exit_pos:
                    line += f"\033[1;33m{EXIT}\033[0m"
                elif (y, x) in self.treasures:
                    line += f"\033[1;36m{TREASURE}\033[0m"
                elif (y, x) in self.visited:
                    line += f"\033[90m{VISITED}\033[0m"
                else:
                    line += cell
            print(line)
        
        # Stats
        elapsed = int(time.time() - self.start_time) if self.start_time else 0
        print(f"\n  ⏱️ Time: {elapsed}s | 🚶 Moves: {self.moves} | 💎 Treasures: {self.score}/{len(self.treasures)}")
        
        # Legend
        print(f"\n  \033[90mLegend: {VISITED} visited | \033[36m{TREASURE} treasure | \033[33m{EXIT} exit\033[0m")
        print("  \033[90mArrow keys: move | N: new maze | Q: quit\033[0m")
    
    def move(self, direction):
        """Move player in direction"""
        moves = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}
        
        if direction not in moves:
            return False
        
        dx, dy = moves[direction]
        new_y = self.player_pos[0] + dy
        new_x = self.player_pos[1] + dx
        
        if self.maze[new_y][new_x] != WALL:
            self.player_pos = [new_y, new_x]
            self.moves += 1
            
            # Mark visited
            if tuple(self.player_pos) not in self.visited:
                self.visited.add(tuple(self.player_pos))
            
            # Collect treasure
            if tuple(self.player_pos) in [tuple(t) for t in self.treasures]:
                self.treasures.remove(self.player_pos)
                self.score += 100
                print("\a")  # Bell
            
            # Check exit
            if self.player_pos == self.exit_pos:
                return True
        
        return False
    
    def generate_new(self):
        """Generate a new maze"""
        self.__init__(self.width, self.height)


def main():
    """Main entry point"""
    print("\n  🧩 Welcome to Maze v2.0! 🧩\n")
    
    # Difficulty selection
    print("  Select Size:")
    print("  ┌────────────────────────┐")
    print("  │ 1. Small   (15x9)     │")
    print("  │ 2. Medium  (21x11)    │")
    print("  │ 3. Large   (31x17)    │")
    print("  │ 4. XL      (41x21)    │")
    print("  └────────────────────────┘\n")
    
    diff = input("  Enter choice (1-4): ").strip()
    
    sizes = {
        '1': (15, 9),
        '2': (21, 11),
        '3': (31, 17),
        '4': (41, 21),
    }
    
    w, h = sizes.get(diff, (21, 11))
    game = MazeGame(w, h)
    game.start_time = time.time()
    
    while True:
        game.draw()
        
        key = keyboard.read_key()
        
        if key == 'up' or key == 'w':
            if game.move('up'):
                break
        elif key == 'down' or key == 's':
            if game.move('down'):
                break
        elif key == 'left' or key == 'a':
            if game.move('left'):
                break
        elif key == 'right' or key == 'd':
            if game.move('right'):
                break
        elif key in ['n', 'N']:
            game.generate_new()
            game.start_time = time.time()
        elif key in ['q', 'Q', 'escape']:
            break
    
    # Win screen
    os.system('clear')
    print(f"\n  \033[1;32m╔{'═' * 30}╗")
    print("  ║       🎉 YOU WIN! 🎉       ║")
    print(f"  ╚{'═' * 30}╝\033[0m\n")
    
    elapsed = int(time.time() - game.start_time)
    print(f"  ⏱️  Time: {elapsed}s")
    print(f"  🚶  Moves: {game.moves}")
    print(f"  💎  Treasures: {game.score // 100}/{len(game.treasures) + game.score // 100}")
    print(f"  📊  Score: {game.score + max(0, 1000 - game.moves * 2) + max(0, 500 - elapsed * 5)}")
    print("\n  Thanks for playing!\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Game exited.\n")
