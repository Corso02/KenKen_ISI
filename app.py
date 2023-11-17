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
    
    def get_label(self):
        return self.label
    
    def get_canvas(self):
        return self.canvas

    def get_number(self):
        return self.number

    def set_label(self, label):
        self.label = label

    def set_border(self, border):
        self.border = border
        self.set_neighbours()
    
    def set_number(self, number):
        self.number = number
        if(self.canvas != None):
            self.canvas.create_text(50, 45, text=str(number))
    
    def set_canvas(self, canvas):
        self.canvas = canvas

    def set_neighbours(self):
        self.neighbours = ""
        if("d" not in self.border):
            self.neighbours += "d"
        if("l" not in self.border):
            self.neighbours += "l"
        if("r" not in self.border):
            self.neighbours += "r"
        if("u" not in self.border):
            self.neighbours += "u"
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
    
    def is_won(self):
        for row in range(self.dimension):
            count = 0
            for col in range(self.dimension):
                count += self.get_tile(row, col).get_number()
        if count != self.max_row_count:
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

    def dfs_solve(self, func_to_update_window):
        for i in range(3):
            self.get_tile(0,0).canvas.create_text(50,50, text=str(i), tag="text")
            func_to_update_window()
            time.sleep(0.5)
            self.get_tile(0,0).canvas.delete("text")

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

        for tile in tilesData:
            if(tile['shadow_label'] in hashmap):
                hashmap[tile['shadow_label']] += 1
            else:
                hashmap[tile['shadow_label']] = 1
        
        availableNumbersHashMap = {}
        
        for label,count in hashmap.items():
            if(len(label.split())==1):
                number = label.split()[0]
                operand = ""
            else:
                number = label.split()[0]
                operand = label.split()[1]
            if(operand == ""):
                availableNumbersHashMap[label] = [number]
            else:
                availableNumbersHashMap[label] = self.field.find_combination(num_of_numbers=int(count), operand=operand, target=int(number))
        
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

            self.field.get_tile(row,col).set_available_numbers(availableNumbersHashMap[tile['shadow_label']])
            #self.field.get_tile(row,col).show_available_numbers()
        field_cotainer.pack(side="left")
        self.add_control_buttons()
        self.update()
        
    def add_control_buttons(self):
        container = tk.Frame(self.window)
        dfsBtn = tk.Button(container, text="Solve using DFS", bg="#1e90ff", fg="#ffffff", command=lambda: self.field.dfs_solve(self.update))
        dfsBtn.grid(row=0, column=0, pady=(0, 20))

        backtrackBtn = tk.Button(container, text="Solve using Backtracking", bg="#1e90ff", fg="#ffffff")
        backtrackBtn.grid(row=1, column=0, pady=(0, 20))

        fwdCheck = tk.Button(container, text="Solve using Forward Checking", bg="#1e90ff", fg="#ffffff")
        fwdCheck.grid(row = 2, column=0, pady=(0, 20), padx=20)

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




