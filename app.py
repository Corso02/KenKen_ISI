import tkinter as tk
import json
import time
import itertools
from array import array
import os
from tkinter import ttk

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
        self.sector_len = 0
        self.availableNumbersBeforeRemoval = []
    
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

    def get_sector_len(self):
        return self.sector_len

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
        self.sector_len = len(sector)
    
    def set_available_numbers(self, availableNumbers):
        self.availableNumbers = availableNumbers
        self.availableNumbersBeforeRemoval = array('i')

        for number in availableNumbers:
            self.availableNumbersBeforeRemoval.append(number)

    def show_available_numbers(self):
        self.canvas.delete("numbers")
        optionIdx = 0
        for option in self.availableNumbers:
            idx = 0
            self.canvas.create_text(40 + (10*idx), 65 + (10*optionIdx), text=f"{option}", tag="numbers")
            idx += 1
            optionIdx += 1
            
    def remove_number_from_available_numbers(self, num_to_remove):
        if num_to_remove in self.availableNumbers:
            self.availableNumbers.remove(num_to_remove)
    
    def add_number_to_available_numbers(self, num_to_add):
        if num_to_add in self.availableNumbersBeforeRemoval and num_to_add not in self.availableNumbers:
            self.availableNumbers.append(num_to_add)

class Field:
    def __init__(self, dimension):
        self.dimension = dimension
        self.tiles = [0] * dimension 
        self.availableNumbersToChoose = [0] * dimension
        self.dfs_visited_tiles_count = 0
        self.fwd_visited_tiles_count = 0
        self.backtracking_visited_tiles_count = 0
        self.dfs_backtrack_count = 0
        self.backtracking_backtrack_count = 0
        self.fwd_backtrack_count = 0
        for row in range(dimension):
            self.availableNumbersToChoose[row] = row + 1
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
    
    def show_available_numbers_all_tiles(self):
        for tileRow in self.tiles:
            for tile in tileRow:
                tile.show_available_numbers()

    def is_won(self):
        
        # skontrolujem či sú v každom riadku jedinečné čísla
        for tile_row in self.tiles:
            row_nums = set([tile.get_number() for tile in tile_row])
            if len(row_nums) != self.dimension:
                return False
        
        # skontrolujem či sú v každom stĺpci jedinečné čísla
        for col in range(len(self.tiles)):
            col_data = set([row[col].get_number() for row in self.tiles])
            if(len(col_data) != self.dimension):
                return False

        # skontrolujem či sú jednotlivé sektory správne vyplnené
        for tileRow in self.tiles:
            for tile in tileRow:
                if not self.check_sector(tile.get_row(), tile.get_col()):
                    return False

        return True

    def set_all_tiles_to_zero(self):
        for tileRow in self.tiles:
            for tile in tileRow:
                tile.set_number(0)
                
    def is_unique(self, resArr, arrToAppend):
        sortedArr = arrToAppend.copy()
        sortedArr.sort()
        return resArr.count(sortedArr) == 0

    def find_combination(self, target, num_of_numbers, operand):
        resTuples = []
        # prejdem všetkými možnými kombináciami čísle z dosupných čísel
        for combination in itertools.product(self.availableNumbersToChoose, repeat=num_of_numbers):
            # kombináciu si zotriedim
            sorted_comb = tuple(sorted(combination)) 
            # keď kombinácia ešte nebola pridaná do výslednych kombinacii a je s tými číslami a daným operandom získať výsledok, tak ho pridam do výsledných kombinácií
            if sorted_comb not in resTuples and target == eval(operand.join(map(str, combination))):
                resTuples.append(sorted_comb)
        
        # vytvorim si set, kde pridam všetky čísla zo ziskaných kombinácií, set zaručí to, že sa nebudú čísla opakovať
        resArr = set()
        for arr in resTuples:
            for number in arr:
                resArr.add(number)
        # vratim si jedinečné čísla ako list        
        return list(resArr)
    
    def find_all_available_numbers_for_sector(self, sector, tile_row, tile_col):
        label = self.get_tile(tile_row, tile_col).get_shadow_label()
        number = label.split()[0]
        if len(label.split()) == 1:
            operand = ""
        else:
            operand = label.split()[1]
        
        # ak daný sektor nemá operand, tak to znamená, že jediné číslo, ktoré možem použiť je číslo sektora
        if operand == "":
            self.get_tile(tile_row, tile_col).set_available_numbers([int(number)])
        else: # inak zavolám funckiu, ktorá mi nájde všetky čísla pre daný sektor
            self.get_tile(tile_row, tile_col).set_available_numbers(self.find_combination(num_of_numbers=len(sector), operand=operand, target=int(number)))
        
    def get_sector(self, tile):
        tile_row = tile.get_row()
        tile_col = tile.get_col()
        sector = self.find_tile_sector(tile_row, tile_col)
        self.get_tile(tile_row, tile_col).set_sector(sector)
        self.find_all_available_numbers_for_sector(sector, tile_row, tile_col)
        
    def find_tile_sector(self, tile_row, tile_col):
        # udržiavam si informácie o tom či som dané poličko už nenavštívil
        visited = set()
        stack = [(tile_row, tile_col)]
        neighbours = [] # výsledok
        while stack:
            tile = stack.pop() # vyberiem si záznam zo stacku
            if tile in visited: continue # ak som dané políčko už navštívil, tak sa vrátim späť na začiatok cyklu
            visited.add(tile) # pridám si súradnice polička do visited
            tile_row, tile_col = tile # vyberiem si súradnice
            neighbours.append((tile_row, tile_col)) # pridám ich do výsledného poľa

            tile_border = self.get_tile(tile_row, tile_col).get_border() #získam si hranice daného políčka

            #na základe ohraničení pridám susedné políčka, ktoré ešte neboli navštívené
            if "u" not in tile_border and tile_row != 0 and (tile_row-1,tile_col) not in visited:
                stack.append((tile_row - 1, tile_col))
            if "l" not in tile_border and tile_col != 0 and (tile_row,tile_col-1) not in visited:
                stack.append((tile_row, tile_col - 1))
            if "r" not in tile_border and tile_col != self.dimension - 1 and (tile_row,tile_col + 1) not in visited:
                stack.append((tile_row, tile_col + 1))
            if "d" not in tile_border and tile_row != self.dimension - 1 and (tile_row+1,tile_col) not in visited:
                stack.append((tile_row + 1, tile_col))
        #vrátim súradnice každého políčka v danom sektore
        return neighbours
    
    def sector_is_filled(self, tile_row, tile_col):
        # kontrola či je celý sektor naplnený
        sector_indexes = self.get_tile(tile_row, tile_col).get_sector()
        for tile_cords in sector_indexes:
            tile_row, tile_col = tile_cords
            if self.get_tile(tile_row, tile_col).get_number() == 0:
                return False
        return True

    def check_sector(self, tile_row, tile_col):
        # kontrola správnosti vyplnenia sektoru
        tile = self.get_tile(tile_row, tile_col)
        sector_indexes = tile.get_sector()
        label = tile.get_shadow_label()

        # daný sektor má iba jedno políčko, takže overujem zadané číslo
        if len(label.split()) == 1:
            required_number = int(tile.get_label())
            return required_number == tile.get_number()

        # vyberiem si číslo a operand
        required_number = int(label.split()[0]) 
        operand = label.split()[1]

        # vyberiem si čísla z každého políčka v sektore
        numbers_in_tiles = []
        for tile_cords in sector_indexes:
            row, col = tile_cords
            numbers_in_tiles.append(self.get_tile(row, col).get_number())

        # vytvorím si všetky permutácie čísel v políčku a následne skontrolujem či daná kombinácia je schopná s daným operandom vrátiť očakávaný výsledok
        combinations = itertools.permutations(numbers_in_tiles)
        for combination in combinations:
            if operand == "/" and 0 in combination: return False
            if eval(operand.join(map(str, combination))) == required_number:
                return True

        return False

    def is_valid_pick(self, row, col, chosed_num):
        # skontrolujem či sa dané číslo už nenachádza v riadku
        for i in range(0, col):
            if self.get_tile(row, i).get_number() == chosed_num:
                return False
        
        #  skontrolujem či sa dané číslo už nenachádza v stĺpci
        for i in range(0, row):
            if self.get_tile(i, col).get_number() == chosed_num:
                return False
        
        return True

    def backtracking_solve_helper(self, func_to_update_window, func_to_add_results, func_to_update_text):
        start_time = time.time() # zapneme časovač aby sme vedeli ako dlho hľadal alogritmus riešenie 
        self.set_all_tiles_to_zero() # vynulujem herné pole
        func_to_update_window()
        self.backtracking_visited_tiles_count = 0 # zresetujem počet navštívených políčok pre algoritmus
        self.backtracking_backtrack_count = 0 # zresetujem počet backtracking 
        solved = self.backtracking(0,0,func_to_update_window, func_to_update_text) # zavolám funkciu pre alogritmus
        end_time = time.time() # zastavím časovač
        solve_time = end_time - start_time # vypočítam si počet sekúnd, ktoré potreboval algoritmus na vyriešenie
        func_to_add_results("Backtracking", self.backtracking_visited_tiles_count, solve_time, solved, 1, self.backtracking_backtrack_count) # vypíšem výsledky
        func_to_update_window()
 

    def backtracking(self, row, col, update_window, update_text):
        if(self.is_won()): # overím či herné pole nie je vo výhernej konfigurácii
            return True
        
        # vypočítam si súradnice dalšieho políčka a určím si či tie súradnice sú vrámci herného poľa
        next_col = 0 if col == self.dimension - 1 else col + 1
        next_row = row if next_col != 0 else row + 1
        solve_next = True if (next_col < self.dimension and next_row < self.dimension) else False

        # inkrementujem počet navštívených políčok
        self.backtracking_visited_tiles_count += 1
        update_text(self.backtracking_visited_tiles_count)
        # budem postupne skúšať čísla od 1 po N 
        for num_to_add in range(1, self.dimension + 1):
            # overím či to číslo neporušuje základné pravidlá hry (čísla sa nesmú opakovať v riadku ani v stĺpci)
            if(self.is_valid_pick(row,col,num_to_add)):
                # ak je to vporiadku tak nastavím políčko na dané číslo
                self.get_tile(row, col).set_number(num_to_add)
                update_window()
                # skontrolujem či som práve touto zmenou nedostal výhernú konfiguráciu
                if(self.is_won()):
                    return True
                # ak mám riešiť následjúce políčko tak rekurzívne zavolám túto funckiu so súradnicami dalšieho políčka, ak bude herné pole vyriešené postupne tak vrátim True
                # a postupne vyjdem z rekurzie
                if(solve_next and self.backtracking(next_row, next_col, update_window, update_text)):
                    return True
                # dané číslo, pre dané políčko nie je vo výhernej konfigurácii, takže nastavím políčko na 0 a pokračujem ďalej v hľadaní
                self.get_tile(row, col).set_number(0)
                
                update_window()
        # nenašiel som správne riešnie, musím sa vrátiť naspäť
        self.backtracking_backtrack_count += 1
        return False

    def dfs_solve_helper(self, func_to_update_window, func_to_add_results, func_to_update_text):
        start_time = time.time()
        self.set_all_tiles_to_zero()
        func_to_update_window()
        self.dfs_visited_tiles_count = 0
        self.dfs_backtrack_count = 0
        solved = self.dfs(0,0,func_to_update_window, func_to_update_text)
        end_time = time.time()
        solve_time = end_time - start_time
        func_to_add_results("DFS", self.dfs_visited_tiles_count, solve_time, solved, 0, self.dfs_backtrack_count)
        func_to_update_window()
        
    def dfs(self, row, col, update_window, update_text):
        # skontrolujem či už nemám výhernú kombináciu
        if(self.is_won()):
            return True
        # vypočítam si súradnice dalšieho políčka a určím si či tie súradnice sú vrámci herného poľa
        next_col = 0 if col == self.dimension - 1 else col + 1
        next_row = row if next_col != 0 else row + 1
        solve_next = True if (next_col < self.dimension and next_row < self.dimension) else False

        # inkrementujem počet navštívených políčok
        self.dfs_visited_tiles_count += 1  
        update_text(self.dfs_visited_tiles_count)
        # postupne vyskúšam všetky čísla od 1 po N
        for num_to_add in range(1, self.dimension + 1):
            # vrámci DFS algoritmu nekontrolujem pravidlá pri vkladaní čísel, skúšam všetky dotsupné možnosti pokiaľ nenarazím na výhernú kombináciu
            self.get_tile(row, col).set_number(num_to_add)
           
            update_window()
            # skontrolujem či som zmenou čísla nezískal výhernú konfiguráciu
            if(self.is_won()):
                return True
            # ak mám riešiť následjúce políčko tak rekurzívne zavolám túto funckiu so súradnicami dalšieho políčka, ak bude herné pole vyriešené postupne tak vrátim True
            # a postupne vyjdem z rekurzie
            if(solve_next and self.dfs(next_row, next_col, update_window, update_text)):
                return True
            # s daným číslom nebolo nájdené riešenie, takže zresetujem políčko a pokračujem ďalej v cykle
            self.get_tile(row, col).set_number(0)
            
            update_window()
        # riešenie nebolo nájdené, musím sa vrátiť o jedno rekurzívne volanie späť
        self.dfs_backtrack_count += 1
        return False

    def forward_checking_solve_helper(self, func_to_update_window, func_to_add_results, func_to_update_text):
        start_time = time.time()
        self.set_all_tiles_to_zero()
        func_to_update_window()
        self.fwd_visited_tiles_count = 0
        self.fwd_backtrack_count = 0
        solved = self.forward_checking(0, 0, func_to_update_window, func_to_update_text)
        end_time = time.time()
        solve_time = end_time - start_time
        func_to_add_results("Forward check", self.fwd_visited_tiles_count, solve_time, solved, 2, self.fwd_backtrack_count)
        func_to_update_window()
    
    def forward_checking(self, row, col, update_window, update_text):
        # skontrolujem či už nemám výhernú kombináciu
        if self.is_won():
            return True

        # vypočítam si súradnice dalšieho políčka a určím si či tie súradnice sú vrámci herného poľa
        next_col = 0 if col == self.dimension - 1 else col + 1
        next_row = row if next_col != 0 else row + 1
        solve_next = True if (next_col < self.dimension and next_row < self.dimension) else False
        
        # inkrementujem počet navštívených políčok
        self.fwd_visited_tiles_count += 1
        update_text(self.fwd_visited_tiles_count)

        # postupne vyskúšam všetky čísla od 1 po N
        for num_to_add in range(1, self.dimension + 1):
            # overím si či dané číslo, v danom políčku spĺňa pravidlá hry a zároveň skontrolujem či by som po pridaní nespôsobil konflikt v niektorých z ostatných políčok v danom
            # riadku a stĺpci
            if self.is_valid_pick(row, col, num_to_add) and self.forward_check_pick(row, col, num_to_add):
                # nastavím číslo ktoré nespôsobuje konflikty a neporušuje pravidlá na dané políčko
                self.get_tile(row, col).set_number(num_to_add)
                
                # zadané číslo odstraním z dostupných čísel z políčok v danom riadku a danom stĺpci
                self.fwd_remove_available_numbers(row, col, num_to_add)
                update_window()
                # skontrolujem či som zmenou čísla nezískal výhernú konfiguráciu
                if self.is_won():
                    return True
                # ak mám riešiť následjúce políčko tak rekurzívne zavolám túto funckiu so súradnicami dalšieho políčka, ak bude herné pole vyriešené postupne tak vrátim True
                # a postupne vyjdem z rekurzie
                if solve_next and self.forward_checking(next_row, next_col, update_window, update_text):
                    return True

                # s daným číslom nebolo nájdené riešenie
                # vrátim číslo do dostupných čísel pre ostatné políčka v danom riadku a danom stĺpci
                self.revert_forward_check_pick(row, col, num_to_add)
                # zresetujem dané políčko
                self.get_tile(row, col).set_number(0)
                update_window()

        # riešenie nebolo možné nájst, musím sa vrátiť o rekurzívne volanie späť
        self.fwd_backtrack_count += 1
        return False
            
    def forward_check_pick(self, row, col, num_to_assign):

        # vezmem si všetky dostupné čísla pre dané políčko a skontrolujem či číslo, ktoré by sme chceli zadať sa nachádza v poli dostupných čísel
        available_numbers_tile = self.get_tile(row, col).get_available_numbers()
        if num_to_assign not in available_numbers_tile: return False

        # skontrolujem či nejakému políčku v riadku nevyradím poslednú možnosť
        for i in range(col + 1, self.dimension):
            tile = self.get_tile(row, i)
            tile_available_numbers = tile.get_available_numbers()
            if num_to_assign in tile_available_numbers: 
                if(len(tile_available_numbers) == 1): return False # po odstránení by neboli dostupné žiadne iné čísla

        
         #skontrolujem či nejakému políčku v stĺpci nevyradím poslednú možnosť
        for i in range(row + 1, self.dimension):
            tile = self.get_tile(i, col)
            tile_available_numbers = tile.get_available_numbers()
            if num_to_assign in tile_available_numbers:
                if(len(tile_available_numbers) == 1):
                    return False # nie su dostupné žiadne iné čísla po odstranení

        # všekto ok
        return True

    def fwd_remove_available_numbers(self, row, col, num):
        # odstránim čísla z poľa dostupných čísel pre každé políčko v danom riadku a stĺpci
        for i in range(col + 1, self.dimension):
            self.get_tile(row, i).remove_number_from_available_numbers(num)
        
        for i in range(row + 1, self.dimension):
            self.get_tile(i, col).remove_number_from_available_numbers(num)

    def revert_forward_check_pick(self, row, col, num_to_assign):
        # vrátim odstranené čísla z poľa dostupných čísel pre každé políčko v danom riadku a stĺpci
        for i in range(col + 1, self.dimension):
            tile = self.get_tile(row, i)
            tile.add_number_to_available_numbers(num_to_assign)
        
        for i in range(row + 1, self.dimension):
            tile = self.get_tile(i, col)
            tile.add_number_to_available_numbers(num_to_assign)
        
            
class UI:
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
        # na základe umiestnenia políčka mu nastavím padding
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
        #nakreslím ohraničenia
        
        #hore
        cell.create_line(0, 0, 100, 0, fill=("black" if "u" in border else "lightgray"), width=2)
        #doprava
        cell.create_line(100, 0, 100, 100, fill=("black" if "r" in border else "lightgray"), width=2)
        #dole
        cell.create_line(0, 100, 100, 100, fill=("black" if "d" in border else "lightgray"), width=2)
        #doľava
        cell.create_line(0, 0, 0, 100, fill=("black" if "l" in border else "lightgray"), width= 2)
	
	
    def create_grid(self, tilesData):
        default_dimension = self.get_dimension_by_cell_count(self.dimension)
        field_cotainer = tk.Canvas(self.window)

        # vyvtorím si políčka na základe dát zo súboru
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
        
        # každému políčku nájdem jeho sektor
        for tileRow in self.field.get_tiles():
            for tile in tileRow:
                self.field.get_sector(tile)
        
        field_cotainer.grid(row = 0, column=0, columnspan=1)
        self.add_control_buttons() # pridám tlačidlá 
        self.add_text_container() # prídám text, ktorý sa bude aktualizovať počas bežania algoritmov
        self.update() # aktualizujem tk okno
        
    def add_control_buttons(self):
        container = tk.Frame(self.window)
        dfsBtn = tk.Button(container, text="Solve using DFS", bg="#1e90ff", fg="#ffffff", command=lambda: self.field.dfs_solve_helper(self.update, self.add_text_res, self.set_metric_text))
        dfsBtn.grid(row=0, column=0, pady=(0, 20))

        backtrackBtn = tk.Button(container, text="Solve using Backtracking", bg="#1e90ff", fg="#ffffff", command=lambda: self.field.backtracking_solve_helper(self.update, self.add_text_res, self.set_metric_text))
        backtrackBtn.grid(row=1, column=0, pady=(0, 20))

        fwdCheck = tk.Button(container, text="Solve using Forward Checking", bg="#1e90ff", fg="#ffffff", command=lambda: self.field.forward_checking_solve_helper(self.update, self.add_text_res, self.set_metric_text))
        fwdCheck.grid(row = 2, column=0, pady=(0, 20), padx=20)

        mainMenuBtn = tk.Button(container, text="Return to main menu", bg="#1e90ff", fg="#ffffff", command=self.main_menu)    
        mainMenuBtn.grid(row = 3, column=0, pady=(0, 20))
		
		
        default_bg = self.window.cget("bg")
        default_relief = "flat"
        self.metric_text = tk.Text(container, width=40, height=1, bg=default_bg, relief=default_relief)
        self.metric_text.configure(state='disabled')
        self.metric_text.grid(row = 4, column = 0, pady=(0,20))
        self.metric_text.tag_configure("center", justify="center")

        container.grid(row = 0, column=1, columnspan=1)
		
    def set_metric_text(self, num_to_set):
        self.metric_text.configure(state='normal')
        self.metric_text.delete("1.0", 'end')
        self.metric_text.insert("1.0", f"Počet navštívených políčok: {num_to_set}", "center")
        self.metric_text.configure(state='disabled')

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

    def add_text_container(self):
        self.text_container = tk.Frame(self.window)
        self.text_container.grid(row=0, column=2, columnspan=1)

    def add_text_res(self, name, count, time, solved, col, backtrack_count):
        # pridám výsledky algoritmu na obrazovku
        default_bg = self.window.cget("bg")
        default_relief = "flat"
        container = tk.Frame(self.text_container)
        window_width = 30 #self.window.winfo_width()//10


        divider = tk.Text(container, width=window_width, height=1, bg=default_bg, relief=default_relief)
        divider.tag_configure("center", justify="center")
        divider.insert("1.0", f"{'-'*window_width}", "center")
        divider.grid(row=0, column=0)
        divider.config(state="disabled")
            
        name_widget = tk.Text(container, width=40, height=1, bg=default_bg, relief=default_relief)
        name_widget.tag_configure("center", justify="center")
        name_widget.insert("1.0", name, "center")
        name_widget.grid(row=1, column=0)
        name_widget.config(state="disabled")

        solved_widget = tk.Text(container, width=40, height=1, bg=default_bg, relief=default_relief)
        solved_widget.tag_configure("left", justify="left")
        solved_widget.insert("1.0", f"Vyriešené: {solved}", "left")
        solved_widget.grid(row=2, column=0)
        solved_widget.config(state="disabled")

        count_widget = tk.Text(container, width=40, height=1, bg=default_bg, relief=default_relief)
        count_widget.tag_configure("left", justify="left")
        count_widget.insert("1.0", f"Navštívené políčka: {count}", "left")
        count_widget.grid(row=3, column=0)
        count_widget.config(state="disabled")

        backtrack_count_widget = tk.Text(container, width=40, height=1, bg=default_bg, relief=default_relief)
        backtrack_count_widget.tag_configure("left", justify="left")
        backtrack_count_widget.insert("1.0", f"Počet backtracking operácií: {backtrack_count}", "left")
        backtrack_count_widget.grid(row = 4, column=0)
        backtrack_count_widget.config(state="disabled")

        time_widget = tk.Text(container, width=40, height=1, bg=default_bg, relief=default_relief)
        time_widget.tag_configure("left", justify="left")
        time_widget.insert("1.0", f"Čas: {time}", "left")
        time_widget.grid(row=5, column=0)
        time_widget.config(state="disabled")

        container.grid(row=col, column=0, padx=10)
        
       


ui = UI()

ui.main_menu()




