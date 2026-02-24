#!/usr/bin/env python3
"""
Terminal Maze - Generate and solve mazes in your terminal
Author: Sagar Jadhav
"""

import os
import random
import sys

WALL = '██'
PATH = '  '
PLAYER = '🙂'
EXIT = '🚪'

class Maze:
    def __init__(self, width=21, height=11):
        self.width = width
        self.height = height
        self.maze = [[WALL for _ in range(width)] for _ in range(height)]
        self.player_pos = [1, 1]
        self.exit_pos = [height - 2, width - 2]
        self.visited = set()
        self.generate()
    
    def generate(self):
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
    
    def draw(self):
        os.system('clear')
        print("╔" + "═" * self.width + "╗")
        for y, row in enumerate(self.maze):
            line = "║"
            for x, cell in enumerate(row):
                if [y, x] == self.player_pos:
                    line += PLAYER
                else:
                    line += cell
            line += "║"
            print(line)
        print("╚" + "═" * self.width + "╝")
        print(f"Use arrow keys to move. Reach the {EXIT}!")
    
    def move(self, direction):
        moves = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}
        dx, dy = moves[direction]
        new_y = self.player_pos[0] + dy
        new_x = self.player_pos[1] + dx
        if self.maze[new_y][new_x] != WALL:
            self.player_pos = [new_y, new_x]
            return [new_y, new_x] == self.exit_pos
        return False

if __name__ == '__main__':
    maze = Maze()
    import keyboard
    while True:
        maze.draw()
        key = keyboard.read_key()
        if maze.move(key):
            break
        if key == 'escape':
            break
    print("🎉 YOU WIN! 🎉")
