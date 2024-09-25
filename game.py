import tkinter as tk
import random

class Game2048:
    def __init__(self, master):
        self.master = master
        self.master.title("2048 Game")
        self.master.config(cursor="hand2")  # Change cursor here
        self.grid_size = 4
        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.score = 0

        self.create_widgets()
        self.start_game()
        self.master.bind("<Key>", self.key_pressed)

    def create_widgets(self):
        self.canvas = tk.Canvas(self.master, width=400, height=400, bg="lightgrey")
        self.canvas.pack()
        self.score_label = tk.Label(self.master, text="Score: 0", font=("Arial", 24))
        self.score_label.pack()

    def start_game(self):
        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()
        self.update_canvas()

    def add_new_tile(self):
        empty_cells = [(r, c) for r in range(self.grid_size) for c in range(self.grid_size) if self.grid[r][c] == 0]
        if empty_cells:
            r, c = random.choice(empty_cells)
            self.grid[r][c] = random.choice([2, 4])

    def update_canvas(self):
        self.canvas.delete("all")
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                value = self.grid[r][c]
                x0, y0 = c * 100, r * 100
                color = self.get_tile_color(value)
                self.canvas.create_rectangle(x0, y0, x0 + 100, y0 + 100, fill=color, outline="black")
                if value != 0:
                    self.canvas.create_text(x0 + 50, y0 + 50, text=str(value), font=("Arial", 24))

        self.score_label.config(text="Score: " + str(self.score))

    def get_tile_color(self, value):
        colors = {
            0: "lightgrey",
            2: "white",
            4: "lightyellow",
            8: "lightgreen",
            16: "lightblue",
            32: "lightsalmon",
            64: "orange",
            128: "cyan",
            256: "blue",
            512: "purple",
            1024: "magenta",
            2048: "red"
        }
        return colors.get(value, "black")

    def key_pressed(self, event):
        if event.keysym in ["Left", "Right", "Up", "Down"]:
            moved = False
            if event.keysym == "Left":
                moved = self.move_tiles(self.grid, is_horizontal=True, reverse=False)
            elif event.keysym == "Right":
                moved = self.move_tiles(self.grid, is_horizontal=True, reverse=True)
            elif event.keysym == "Up":
                moved = self.move_tiles(self.grid, is_horizontal=False, reverse=False)
            elif event.keysym == "Down":
                moved = self.move_tiles(self.grid, is_horizontal=False, reverse=True)

            if moved:
                self.add_new_tile()
                self.update_canvas()
                if not self.can_move():
                    self.canvas.create_text(200, 200, text="Game Over", font=("Arial", 48), fill="black")

    def can_move(self):
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if self.grid[r][c] == 0:
                    return True
                if c < self.grid_size - 1 and self.grid[r][c] == self.grid[r][c + 1]:
                    return True
                if r < self.grid_size - 1 and self.grid[r][c] == self.grid[r + 1][c]:
                    return True
        return False

    def move_tiles(self, grid, is_horizontal, reverse):
        moved = False
        for idx in range(self.grid_size):
            line = grid[idx] if is_horizontal else [grid[r][idx] for r in range(self.grid_size)]
            new_line, score_increment = self.merge_line(line, reverse)
            if new_line != line:
                moved = True
                if is_horizontal:
                    grid[idx] = new_line
                else:
                    for r in range(self.grid_size):
                        grid[r][idx] = new_line[r]
                self.score += score_increment
        return moved

    def merge_line(self, line, reverse):
        if reverse:
            line = line[::-1]
        
        new_line = [num for num in line if num != 0]
        score_increment = 0
        merged_line = []

        skip = False
        for i in range(len(new_line)):
            if skip:
                skip = False
                continue
            if i < len(new_line) - 1 and new_line[i] == new_line[i + 1]:
                merged_value = new_line[i] * 2
                merged_line.append(merged_value)
                score_increment += merged_value
                skip = True
            else:
                merged_line.append(new_line[i])
        
        merged_line += [0] * (self.grid_size - len(merged_line))
        if reverse:
            merged_line = merged_line[::-1]

        return merged_line, score_increment

if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()
