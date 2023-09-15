import pygame
import numpy as np

pygame.init()

class NonogramGame:
    def __init__(self, size=20):
        self.size = size
        self.cell_size = 30
        self.hint_space = 200  # Space for the hints
        
        self.board = np.full((size, size), ".", dtype=str)
        self.solution = np.full((size, size), ".", dtype=str)
        self.fill_random_cells()
        self.row_hints, self.col_hints = self.get_all_hints()

        self.win_width = self.size * self.cell_size + self.hint_space
        self.win_height = self.size * self.cell_size + self.hint_space

        self.win = pygame.display.set_mode((self.win_width, self.win_height), pygame.FULLSCREEN)

    def fill_random_cells(self):
        num_cells = np.random.randint(400, 401)
        rows = np.random.randint(0, self.size, num_cells)
        cols = np.random.randint(0, self.size, num_cells)
        for r, c in zip(rows, cols):
            self.solution[r, c] = "*"

    def get_row_hints(self, row):
        hints = []
        count = 0
        for cell in row:
            if cell == "*":
                count += 1
            else:
                if count > 0:
                    hints.append(count)
                    count = 0
        if count > 0:
            hints.append(count)
        return hints[::-1]  # Reverse the hints list

    def get_all_hints(self):
        row_hints = [self.get_row_hints(row) for row in self.solution]
        col_hints = [self.get_row_hints(col) for col in self.solution.T]
        return row_hints, col_hints

    def display_board_with_hints(self):
        max_row_hint = max(len(h) for h in self.row_hints)
        max_col_hint = max(len(h) for h in self.col_hints)

        # Adjust the top hints
        for i in range(max_col_hint):
            print(" " * (max_row_hint * 3 + 2), end="")  # 加大左側空白距離
            for col_hint in self.col_hints:
                if len(col_hint) >= max_col_hint - i:
                    print(f"{col_hint[-max_col_hint + i]:2}", end="  ")
                else:
                    print("    ", end="")
            print("\n")

        # Adjust the left hints and display the board
        for r_h, row in zip(self.row_hints, self.board):
            print(" ".join([str(x) for x in r_h] + [" " for _ in range(max_row_hint - len(r_h))]), end="   ")  # 增大左側間距
            print("  ".join(row))
            print("\n")

    def mark_cell(self, row, col, note=None):
        if note == "X":
            self.board[row, col] = "X"
        else:
            if self.board[row, col] == ".":
                self.board[row, col] = "*"
            else:
                self.board[row, col] = "."

    def draw_hints(self):
        font_size = 24
        font = pygame.font.SysFont(None, font_size)
        
        for idx, hints in enumerate(self.row_hints):
            x_offset = self.hint_space - 10  # Starting from the rightmost part
            for hint in hints:
                render = font.render(str(hint), True, (0, 0, 0))
                x_offset -= render.get_width()  # Move left by the width of the hint
                y_position = idx * self.cell_size + self.cell_size - render.get_height() +195 # Align to the bottom of the cell
                self.win.blit(render, (x_offset, y_position))
                x_offset -= 12  # Additional 3 pixel gap between hints

        # Draw column hints
        for idx, hints in enumerate(self.col_hints):
            y_offset = self.hint_space - 10  # Starting from the bottommost part
            for hint in hints:
                render = font.render(str(hint), True, (0, 0, 0))
                y_offset -= render.get_height()  # Move upwards by the height of the hint
                x_position = idx * self.cell_size + self.cell_size - render.get_width() // 2 +185 # Align to the center of the cell
                self.win.blit(render, (x_position, y_offset))
                y_offset -= 3  # Additional 3 pixel gap between hints

    def draw_board(self):
        for i in range(self.size):
            for j in range(self.size):
                color = (255, 255, 255)
                if hasattr(self, 'show_solution') and self.show_solution:
                    # 凸顯不正確的儲存格
                    if self.board[i, j] == "*" and self.solution[i, j] == ".":
                        color = (0, 0, 255)  # 藍色
                    elif self.board[i, j] in [".", "X"] and self.solution[i, j] == "*":
                        color = (0, 0, 255)  # 藍色
                    elif self.solution[i, j] == "*":
                        color = (0, 0, 0)
                else:
                    if self.board[i, j] == "*":
                        color = (0, 0, 0)
                    elif self.board[i, j] == "X":
                        color = (200, 200, 200)
                
                pygame.draw.rect(self.win, color, (j * self.cell_size + self.hint_space, i * self.cell_size + self.hint_space, self.cell_size, self.cell_size))
                pygame.draw.line(self.win, (50, 50, 50), (j * self.cell_size + self.hint_space, self.hint_space), (j * self.cell_size + self.hint_space, self.win_height))
                pygame.draw.line(self.win, (50, 50, 50), (self.hint_space, i * self.cell_size + self.hint_space), (self.win_width, i * self.cell_size + self.hint_space))
        # 定義遊玩說明
        instructions = [
            "play guide:",
            "1. left click to fill up.",
            "2. left click same place to cancel",
            "3. right click to make note.",
            "4. fill in all correct cells to win!",
            "",
            "other functions:",
            "1. esc to exit game.",
            "2. enter to check correct nonogram."]

        # 選擇字型和大小
        font = pygame.font.SysFont('arial', 24)

        # 設定說明的起始位置
        start_x = self.win_width + 20  # 從遊戲版面右側開始
        start_y = 300  # 從頂部開始，你可以根據需要調整

        for line in instructions:
            text = font.render(line, True, (0, 0, 0))  # 渲染文字
            self.win.blit(text, (start_x, start_y))  # 將文字放到畫面上
            start_y += 30  # 下移一些像素以供下一行說明
        
        # 畫最下方的線條
        pygame.draw.line(self.win, (50, 50, 50), (self.hint_space, self.win_height - 1), (self.win_width, self.win_height - 1))
        # 畫最右方的線條
        pygame.draw.line(self.win, (50, 50, 50), (self.win_width - 1, self.hint_space), (self.win_width - 1, self.win_height))
        self.draw_hints()

    def check_win(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.solution[i, j] == "*" and self.board[i, j] != "*":
                    return False
        return True

    def play(self):
        clock = pygame.time.Clock()
        running = True
        self.show_solution = False  #初始設定不顯示答案
        game_won = False  #初始化 game_won 變數

        while running:
            clock.tick(60)
            self.win.fill((255, 255, 255))  #背景顏色填為白色

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:  #檢測鍵盤按鍵
                    if event.key == pygame.K_RETURN:  #檢測 Enter 鍵
                        self.show_solution = not self.show_solution  #切換是否顯示答案
                    elif event.key == pygame.K_ESCAPE:  # 檢測 ESC 鍵
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    adjusted_x = x - self.hint_space
                    adjusted_y = y - self.hint_space

                    if 0 <= adjusted_x < self.size * self.cell_size and 0 <= adjusted_y < self.size * self.cell_size:
                        row, col = adjusted_y // self.cell_size, adjusted_x // self.cell_size
                        if event.button == 1:
                            self.mark_cell(row, col)
                        elif event.button == 3:
                            self.mark_cell(row, col, "X")
            
            if self.check_win() and not game_won:
                game_won = True
                font = pygame.font.SysFont('arial', 48)  # 設定字型和大小
                text = font.render("Congratulations! You've solved this nonogram!", True, (0, 0, 0))  # 生成文本圖像
                text_rect = text.get_rect(center=(self.win_width/2 + 150, self.win_height/2))  # 設定文本位置
                self.win.blit(text, text_rect)  # 將文本繪製到視窗上
                pygame.display.flip()  # 更新視窗以顯示文本
                pygame.time.wait(10000)
                running = False
            elif not game_won:  # 只有在遊戲沒有贏的情況下才更新畫面
                self.draw_board()
                pygame.display.flip()
        pygame.quit()

game = NonogramGame()
game.play()
