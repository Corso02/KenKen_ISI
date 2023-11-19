import tkinter as tk
import json
import time
import itertools
from array import array
import os

class Tile:
    def __init__(self, row, col, number, label=""):
        self.row = row
        self.col = col
        self.number = number
        self.label = label
        self.shadow_label = label
        self.border = ""
        self.canvas = None
        self.availableNumbers = []
        self.sector = []
    
    def get_label(self):
        return self.label
    
    def get_canvas(self):
        return self.canvas

    def get_number(self):
        return self.number

    def get_col(self):
        return self.col
    
    def get_row(self):
        return self.row

    def get_border(self):
        return self.border

    def get_sector(self):
        return self.sector

    def get_shadow_label(self):
        return self.shadow_label

    def get_available_numbers(self):
        return self.availableNumbers

    def set_label(self, label):
        self.label = label

    def set_shadow_label(self, shadow_label):
        self.shadow_label = shadow_label

    def set_border(self, border):
        self.border = border
    
    def set_number(self, number):
        self.number = number
        if(self.canvas != None):
            self.canvas.delete("number")
            self.canvas.create_text(50, 45, text=str(number), tag="number")
    
    def set_canvas(self, canvas):
        self.canvas = canvas
    
    def set_sector(self, sector):
        self.sector = sector

    def set_available_numbers(self, availableNumbers):
        self.availableNumbers = availableNumbers

    def show_available_numbers(self):
        print(self.availableNumbers)
        if len(self.availableNumbers) == 1:
            idx = 0
            for option in self.availableNumbers:
                if(idx == len(self.availableNumbers) - 1):
                    self.canvas.create_text(40 + (10*idx), 80, text=f"{option}")
                else:
                    self.canvas.create_text(40 + (10*idx), 80, text=f"{option},")
                idx += 1
        else:
            optionIdx = 0
            for options in self.availableNumbers:
                idx = 0
                for option in options:
                    if(idx == len(options) - 1):
                        self.canvas.create_text(40 + (10*idx), 50 + (10*optionIdx), text=f"{option}")
                    else:
                        self.canvas.create_text(40 + (10*idx), 50 + (10*optionIdx), text=f"{option},")
                    idx += 1
                optionIdx += 1
    


class Field:
    def __init__(self, dimension):
        self.dimension = dimension
        self.max_row_count = 0 # pouzite pre kontrolu ci su cisla v riadku spravne (ci sa neopakuju)
        self.tiles = [0] * dimension 
        self.availableNumbersToChoose = [0] * dimension
        for row in range(dimension):
            self.availableNumbersToChoose[row] = row + 1
            self.max_row_count += (row + 1)
            tile_row = [0] * dimension
            for col in range(dimension):
                tile_row[col] = Tile(row, col, 0)
            self.tiles[row] = tile_row
    
    def get_tile(self, row, col):
        return self.tiles[row][col]

    def get_tiles(self):
        return self.tiles

    def set_tile(self, row, col, label="", border="", number=-1, canvas=None, shadow_label=""):
        tileToUpdate = self.get_tile(row,col)
        if(len(label) != 0):
            tileToUpdate.set_label(label)
        if(len(border) != 0):
            tileToUpdate.set_border(border)
        if(number != -1):
            tileToUpdate.set_number(number)
        if(canvas != None):
            tileToUpdate.set_canvas(canvas)
        if(len(shadow_label) != 0):
            tileToUpdate.set_shadow_label(shadow_label)
    
    def is_won(self):
        for row in range(self.dimension):
            count = 0
            for col in range(self.dimension):
                count += self.get_tile(row, col).get_number()
        if count != self.max_row_count:
            return False
        
        for tileRow in self.tiles:
            for tile in tileRow:
                if not self.check_sector(tile.get_row(), tile.get_col()):
                    return False

        return True
    
    def is_unique(self, resArr, arrToAppend):
        sortedArr = arrToAppend.copy()
        sortedArr.sort()
        return resArr.count(sortedArr) == 0

    def find_combination(self, target, num_of_numbers, operand):
        resArr = []
        for combination in itertools.product(self.availableNumbersToChoose, repeat=num_of_numbers):
            sorted_comb = tuple(sorted(combination))
            if target == eval(operand.join(map(str, combination))) and sorted_comb not in resArr:
                resArr.append(sorted_comb) 
                
        return resArr 

    def set_all_tiles_to_zero(self):
        for tileRow in self.tiles:
            for tile in tileRow:
                tile.set_number(0)
    
    def find_all_available_numbers_for_sector(self, sector, tile_row, tile_col):
        label = self.get_tile(tile_row, tile_col).get_shadow_label()
        number = label.split()[0]
        if len(label.split()) == 1:
            operand = ""
        else:
            operand = label.split()[1]
        
        if operand == "":
            self.get_tile(tile_row, tile_col).set_available_numbers([int(number)])
        else:
            self.get_tile(tile_row, tile_col).set_available_numbers(self.find_combination(num_of_numbers=len(sector), operand=operand, target=int(number)))
        
        
    def get_sector(self, tile):
        visited = [[False for _ in range(self.dimension)] for _ in range(self.dimension)]
        tile_row = tile.get_row()
        tile_col = tile.get_col()
        sector = self.find_tile_sector(tile_row, tile_col, visited)
        self.get_tile(tile_row, tile_col).set_sector(sector)
        self.find_all_available_numbers_for_sector(sector, tile_row, tile_col)
        
    def find_tile_sector(self, tile_row, tile_col, visited):
        stack = [(tile_row, tile_col)]
        neighbours = []
        while stack:
            tile_row, tile_col = stack.pop()
            visited[tile_row][tile_col] = True
            neighbours.append((tile_row, tile_col))

            tile_border = self.get_tile(tile_row, tile_col).get_border()
            if "u" not in tile_border and tile_row != 0 and not visited[tile_row-1][tile_col]:
                stack.append((tile_row - 1, tile_col))
            if "l" not in tile_border and tile_col != 0 and not visited[tile_row][tile_col-1]:
                stack.append((tile_row, tile_col - 1))
            if "r" not in tile_border and tile_col != self.dimension - 1 and not visited[tile_row][tile_col + 1]:
                stack.append((tile_row, tile_col + 1))
            if "d" not in tile_border and tile_row != self.dimension - 1 and not visited[tile_row+1][tile_col]:
                stack.append((tile_row + 1, tile_col))
        
        return neighbours
    
    def sector_is_filled(self, tile_row, tile_col):
        sector_indexes = self.get_tile(tile_row, tile_col).get_sector()
        for tile_cords in sector_indexes:
            tile_row, tile_col = tile_cords
            if self.get_tile(tile_row, tile_col).get_number() == 0:
                return False
        return True

    def check_sector(self, tile_row, tile_col):
        tile = self.get_tile(tile_row, tile_col)
        sector_indexes = tile.get_sector()
        label = tile.get_shadow_label()

        if len(label.split()) == 1:
            required_number = int(tile.get_label())
            return required_number == tile.get_number()

        required_number = int(label.split()[0])
        operand = label.split()[1]
        numbers_in_tiles = []
        for tile_cords in sector_indexes:
            row, col = tile_cords
            numbers_in_tiles.append(self.get_tile(row, col).get_number())
        
        numbers_in_tiles.sort()
        availableNumbers = tile.get_available_numbers()
        sortedAvailableNumbers = []
        
        for availableCombination in availableNumbers:
            combo_list = list(availableCombination)
            combo_list.sort()
            sortedAvailableNumbers.append(combo_list)

        return numbers_in_tiles in sortedAvailableNumbers
    
    def is_valid_pick(self, row, col, chosen_num):
        # check row
        for i in range(0, self.dimension):
            if self.get_tile(row, i).get_number() == chosen_num:
                return False

        # check col
        for i in range(0, self.dimension):
            if self.get_tile(i, col).get_number() == chosen_num:
                return False
        
        # OPTIMALIZACIA: skusat budem iba validne cisla pre dany sektor
        all_available_numbers_for_sector = self.get_tile(row, col).get_available_numbers()
        if len(all_available_numbers_for_sector) == 1 and type(all_available_numbers_for_sector[0]) is not tuple:
            return True

        for one_combination in all_available_numbers_for_sector:
            list_comb = list(one_combination)
            if(chosen_num in list_comb):
                return True
        return False

        # KONIEC OPTIMALIZACIE
        #return True

    def dfs_solve_helper(self, func_to_update_window):
        start_time = time.time()
        self.set_all_tiles_to_zero()
        func_to_update_window()
        solved = self.dfs(0,0,func_to_update_window)
        print("Vyriesene: ", solved)
        end_time = time.time()
        print("Dlzka: ", end_time - start_time)

    def dfs(self, row, col, update_window):
        if(self.is_won()):
            return True
        
        next_col = 0 if col == self.dimension - 1 else col + 1
        next_row = row if next_col != 0 else row + 1
        solve_next = True if (next_col < self.dimension and next_row < self.dimension) else False

        for num_to_add in range(1, self.dimension + 1):
            if(self.is_valid_pick(row,col,num_to_add)):
                self.get_tile(row, col).set_number(num_to_add)
                update_window()
                #time.sleep(0.1)
                if(self.is_won()):
                    return True
                if(solve_next and self.dfs(next_row, next_col, update_window)):
                    return True
                self.get_tile(row, col).set_number(0)
                update_window()
        
        return False
    
    def backtracking_solve_helper(self, func_to_update_window):
        start_time = time.time()
        self.set_all_tiles_to_zero()
        func_to_update_window()
        solved = self.backtracking(0, 0, func_to_update_window)
        print("Vyriesene: ", solved)
        end_time = time.time()
        print("Dlzka: ", end_time - start_time)

    def backtracking(self, row, col, update_window):
        if self.is_won():
            return True

        next_col = 0 if col == self.dimension - 1 else col + 1
        next_row = row if next_col != 0 else row + 1
        solve_next = True if (next_col < self.dimension and next_row < self.dimension) else False

        for num_to_add in range(1, self.dimension + 1):
            if self.is_valid_pick(row, col, num_to_add):
                self.get_tile(row, col).set_number(num_to_add)
                update_window()
                if self.is_won():
                    return True
                if solve_next and self.backtracking(next_row, next_col, update_window):
                    return True
                self.get_tile(row, col).set_number(0)
                update_window()

        return False
    
    def forward_checking_helper(self, row, col, chosen_num):
        for i in range(self.dimension):
            if self.get_tile(row, i).get_number() == chosen_num or self.get_tile(i, col).get_number() == chosen_num:
                return False
        
        sector_indexes = self.get_tile(row, col).get_sector()
        for tile_cords in sector_indexes:
            tile_row, tile_col = tile_cords
            if self.get_tile(tile_row, tile_col).get_number() == chosen_num:
                return False

        return True

    def forward_checking(self, row, col, update_window):
        if self.is_won():
            return True

        next_col = 0 if col == self.dimension - 1 else col + 1
        next_row = row if next_col != 0 else row + 1
        solve_next = True if (next_col < self.dimension and next_row < self.dimension) else False

        for num_to_add in range(1, self.dimension + 1):
            if self.is_valid_pick(row, col, num_to_add) and self.forward_checking_helper(row, col, num_to_add):
                self.get_tile(row, col).set_number(num_to_add)
                update_window()
                if self.is_won():
                    return True
                if solve_next and self.forward_checking(next_row, next_col, update_window):
                    return True
                self.get_tile(row, col).set_number(0)
                update_window()

        return False

    def forward_checking_solve_helper(self, func_to_update_window):
        start_time = time.time()
        self.set_all_tiles_to_zero()
        func_to_update_window()
        solved = self.forward_checking(0, 0, func_to_update_window)
        print("Vyriesene: ", solved)
        end_time = time.time()
        print("Dlzka: ", end_time - start_time)

class ConsoleUI:
    def __init__(self, grid_dimension = 0):
        self.window = tk.Tk()
        self.window.title("KenKen")
        self.dimension = grid_dimension
        if(grid_dimension != 0):
            self.field = Field(grid_dimension)
        self.default_padding = 20

    def set_dimension(self, dimension):
        self.dimension = dimension
    
    def create_field(self):
        self.field = Field(self.dimension)

    def get_dimension_by_cell_count(self,count):
        return 100

    def add_padding_to_cell(self,cell, row, col):
        if(col == 0):
            if(row == 0):
                cell.grid(row=row, column=col, padx=(self.default_padding,0), pady=(self.default_padding,0,), sticky="nsew")
            elif(row == self.dimension - 1):
                cell.grid(row=row, column=col, pady=(0,self.default_padding), padx=(self.default_padding,0,), sticky="nsew")
            else:
                cell.grid(row=row, column=col, padx=(self.default_padding,0,), sticky="nsew")
        elif(col == self.dimension - 1):
            if(row == 0):
                cell.grid(row = row, column=col, padx=(0, self.default_padding), pady=(self.default_padding, 0,), sticky="nsew")
            elif(row == self.dimension - 1):
                cell.grid(row=row, column=col, padx=(0, self.default_padding), pady=(0, self.default_padding,), sticky="nsew")
            else:
                cell.grid(row=row, column=col, padx=(0, self.default_padding,), sticky="nsew")
        elif(row == 0):
            cell.grid(row=row, column=col, pady=(self.default_padding,0,), sticky="nsew")
        elif(row == self.dimension - 1):
            cell.grid(row=row, column=col, pady=(0,self.default_padding,), sticky="nsew")
        else:
            cell.grid(row=row, column=col, sticky="nsew")

    def add_border_to_cell(self, cell, border):
        #up
        cell.create_line(0, 0, 100, 0, fill=("black" if "u" in border else "lightgray"), width=2)
        #right
        cell.create_line(100, 0, 100, 100, fill=("black" if "r" in border else "lightgray"), width=2)
        #down
        cell.create_line(0, 100, 100, 100, fill=("black" if "d" in border else "lightgray"), width=2)
        #left
        cell.create_line(0, 0, 0, 100, fill=("black" if "l" in border else "lightgray"), width= 2)

    def create_grid(self, tilesData):
        default_dimension = self.get_dimension_by_cell_count(self.dimension)
        field_cotainer = tk.Frame(self.window)
        hashmap = {}

        #for tile in tilesData:
        #    if(tile['shadow_label'] in hashmap):
        #        hashmap[tile['shadow_label']] += 1
        #    else:
        #        hashmap[tile['shadow_label']] = 1
        #
        #availableNumbersHashMap = {}
        #
        #for label,count in hashmap.items():
        #    if(len(label.split())==1):
        #        number = label.split()[0]
        #        operand = ""
        #    else:
        #        number = label.split()[0]
        #        operand = label.split()[1]
        #    if(operand == ""):
        #        availableNumbersHashMap[label] = [number]
        #    else:
        #        print(label, count)
        #        availableNumbersHashMap[label] = self.field.find_combination(num_of_numbers=int(count), operand=operand, target=int(number))
    

        for tile in tilesData:
            row = int(tile['row'])
            col = int(tile['col'])
            canvas = tk.Canvas(field_cotainer, width=default_dimension, height=default_dimension, bg='white', highlightthickness=0)
            self.add_padding_to_cell(canvas, row, col)
            canvas.grid_propagate(False)

            self.add_border_to_cell(canvas, tile['border'])
            
            if(len(tile['label']) != 0):
                canvas.create_text(20,10, text=tile['label'])
            
            self.field.set_tile(row,col,tile['label'],tile['border'], canvas=canvas, shadow_label=tile['shadow_label'])

            #self.field.get_tile(row,col).set_available_numbers(availableNumbersHashMap[tile['shadow_label']])
            #self.field.get_tile(row,col).show_available_numbers()
        
        for tileRow in self.field.get_tiles():
            for tile in tileRow:
                self.field.get_sector(tile)
        
        field_cotainer.pack(side="left")
        self.add_control_buttons()
        self.update()
        
    def add_control_buttons(self):
        container = tk.Frame(self.window)
        dfsBtn = tk.Button(container, text="Solve using DFS", bg="#1e90ff", fg="#ffffff", command=lambda: self.field.dfs_solve_helper(self.update))
        dfsBtn.grid(row=0, column=0, pady=(0, 20))

        backtrackBtn = tk.Button(container, text="Solve using Backtracking", bg="#1e90ff", fg="#ffffff", command=lambda: self.field.backtracking_solve_helper(self.update))
        backtrackBtn.grid(row=1, column=0, pady=(0, 20))

        fwdCheckBtn = tk.Button(container, text="Solve using Forward Checking", bg="#1e90ff", fg="#ffffff", command=lambda: self.field.forward_checking_solve_helper(self.update))
        fwdCheckBtn.grid(row = 2, column=0, pady=(0, 20), padx=20)

        mainMenuBtn = tk.Button(container, text="Return to main menu", bg="#1e90ff", fg="#ffffff", command=self.main_menu)    
        mainMenuBtn.grid(row = 3, column=0, pady=(0, 20))

        container.pack(side="left")

    def set_tile(self, row, col, number):
        self.field.get_tile(row, col).set_number(number)
    
    def update(self):
        self.window.update()
        self.window.update_idletasks()

    def show_window(self):
        self.window.mainloop()
    
    def check_won(self):
        return self.field.is_won()

    def main_menu(self):
        self.clear_window()
        title = tk.Text(self.window, height=1, width=50)
        title.tag_configure("center", justify="center")
        title.insert("1.0", "Vyberte level", "center")
        title.pack(pady=10)

        dir_list = os.listdir("levels")
        level_names = filter(self.is_level_file, dir_list)
        for name in level_names:
            self.add_main_menu_btn(name)
        self.show_window()

    def add_main_menu_btn(self, level_name):
        levelBtn = tk.Button(self.window, text=level_name.split(".")[0], command=lambda: self.start_level(level_name))
        levelBtn.pack(pady=10)

    def is_level_file(self, file_name):
        if(len(file_name.split(".")) == 1):
            return False
        name = file_name.split(".")[0]
        ext = file_name.split(".")[1]
        return ext == "json" and "level" in name

    def start_level(self, level_name):
        self.clear_window()
        file = open(f"levels\{level_name}")
        level_data = json.load(file)
        file.close()

        self.set_dimension(int(level_data['dimension']))
        self.create_field()
        self.create_grid(level_data['tiles'])

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

ui = ConsoleUI()

ui.main_menu()