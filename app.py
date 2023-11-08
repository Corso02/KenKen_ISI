import tkinter as tk

class Tile:
    def __init__(self, row, col, number, label=""):
        self.row = row
        self.col = col
        self.number = number
        self.label = label
    
    def get_label(self):
        return self.label

class Field:
    def __init__(self, dimension):
        self.tiles = [0] * dimension 
        for row in range(dimension):
            tile_row = [0] * dimension
            for col in range(dimension):
                if(col == 0):
                    tile_row[col] = Tile(row, col, 0, "3")
                else:
                    tile_row[col] = Tile(row, col, 0)
            self.tiles[row] = tile_row
    
    def get_tile(self, row, col):
        return self.tiles[row][col]


class ConsoleUI:
    def __init__(self, grid_dimension):
        self.window = tk.Tk()
        self.dimension = grid_dimension
        self.field = Field(grid_dimension)
        self.default_padding = 20

    def get_dimension_by_cell_count(self,count):
        if(count > 5):
            return 50
        elif(count >= 3):
            return 75

    def add_padding_to_cell(self,cell, row, col):
        if(col == 0):
            if(row == 0):
                cell.grid(row=row, column=col, padx=(self.default_padding,0), pady=(self.default_padding,0))
            elif(row == self.dimension - 1):
                cell.grid(row=row, column=col, pady=(0,self.default_padding), padx=(self.default_padding,0))
            else:
                cell.grid(row=row, column=col, padx=(self.default_padding,0))
        elif(col == self.dimension - 1):
            if(row == 0):
                cell.grid(row = row, column=col, padx=(0, self.default_padding), pady=(self.default_padding, 0))
            elif(row == self.dimension - 1):
                cell.grid(row=row, column=col, padx=(0, self.default_padding), pady=(0, self.default_padding))
            else:
                cell.grid(row=row, column=col, padx=(0, self.default_padding))
        elif(row == 0):
            cell.grid(row=row, column=col, pady=(self.default_padding,0))
        elif(row == self.dimension - 1):
            cell.grid(row=row, column=col, pady=(0,self.default_padding))
        else:
            cell.grid(row=row, column=col)

    def create_grid(self):
        default_dimension = self.get_dimension_by_cell_count(self.dimension)
        for i in range(self.dimension):
            for j in range(self.dimension):
                frame = tk.Frame(self.window, width=default_dimension, height=default_dimension, relief="solid", borderwidth=2, highlightbackground="black")
                self.add_padding_to_cell(frame, i, j)
                frame.grid_propagate(False)
                if(len(self.field.get_tile(i,j).get_label()) != 0):
                    label = tk.Label(frame, compound=tk.CENTER, text=self.field.get_tile(i,j).get_label())
                    label.grid(row = i, column= j, sticky=tk.NSEW)
                   
        self.window.mainloop()

""" ui = ConsoleUI(5)
ui.create_grid() """

window = tk.Tk()
window.geometry("400x400")

canvas = tk.Canvas(window, width=100, height=100, bg='white', highlightthickness=0)
canvas.grid(row=0, column=0, padx=(20, 0), pady=(20,0), sticky="nsew")
canvas.grid_propagate(False)

canvas.create_text(10,10, text="18 *")

# Nakresli čiaru na pravej strane
canvas.create_line(100, 0, 100, 100, fill='black', width=2)

# Nakresli čiaru na dolna strane
canvas.create_line(0, 100, 100, 100, fill='lightgray', width=2)

#lava ciara
canvas.create_line(0, 0, 0, 100, fill="black", width= 2)

#horna ciara
canvas.create_line(0, 0, 100, 0, fill="black", width=2)

#######################################################################

canvas = tk.Canvas(window, width=100, height=100, bg='white', highlightthickness=0)
canvas.grid(row=0, column=1, pady=(20,0), sticky="nsew")
canvas.grid_propagate(False)

canvas.create_text(10,10, text="2 /")

#prava
canvas.create_line(100, 0, 100, 100, fill='lightgray', width=2)
#dolna
canvas.create_line(0, 100, 100, 100, fill='black', width=2)
#lava
canvas.create_line(0, 0, 0, 100, fill="black", width= 2)
#horna
canvas.create_line(0, 0, 100, 0, fill="black", width=2)

#######################################################################

canvas = tk.Canvas(window, width=100, height=100, bg='white', highlightthickness=0)
canvas.grid(row=0, column=2, pady=(20,0), padx=(0, 20), sticky="nsew")
canvas.grid_propagate(False)

#prava
canvas.create_line(100, 0, 100, 100, fill='black', width=2)
#dolna
canvas.create_line(0, 100, 100, 100, fill='black', width=2)
#lava
canvas.create_line(0, 0, 0, 100, fill="lightgray", width= 2)
#horna
canvas.create_line(0, 0, 100, 0, fill="black", width=2)

########################################################################

canvas = tk.Canvas(window, width=100, height=100, bg='white', highlightthickness=0)
canvas.grid(row=1, column=0, padx=(20,0), sticky="nsew")
canvas.grid_propagate(False)

#prava
canvas.create_line(100, 0, 100, 100, fill='lightgray', width=2)

#dolna
canvas.create_line(0, 100, 100, 100, fill='black', width=2)

#lava
canvas.create_line(0, 0, 0, 100, fill="black", width= 2)

#horna
canvas.create_line(0, 0, 100, 0, fill="lightgray", width=2)


########################################################################

canvas = tk.Canvas(window, width=100, height=100, bg='white', highlightthickness=0)
canvas.grid(row=1, column=1, sticky="nsew")
canvas.grid_propagate(False)

#prava
canvas.create_line(100, 0, 100, 100, fill='black', width=2)

#dolna
canvas.create_line(0, 100, 100, 100, fill='black', width=2)

#lava
canvas.create_line(0, 0, 0, 100, fill="lightgray", width= 2)

#horna
canvas.create_line(0, 0, 100, 0, fill="black", width=2)

########################################################################

canvas = tk.Canvas(window, width=100, height=100, bg='white', highlightthickness=0)
canvas.grid(row=1, column=2, padx=(0,20), sticky="nsew")
canvas.grid_propagate(False)

canvas.create_text(10, 10, text="2 -")

#prava
canvas.create_line(100, 0, 100, 100, fill='black', width=2)

#dolna
canvas.create_line(0, 100, 100, 100, fill='lightgray', width=2)

#lava
canvas.create_line(0, 0, 0, 100, fill="black", width= 2)

#horna
canvas.create_line(0, 0, 100, 0, fill="black", width=2)

########################################################################

canvas = tk.Canvas(window, width=100, height=100, bg='white', highlightthickness=0)
canvas.grid(row=2, column=0, padx=(20,0), sticky="nsew")
canvas.grid_propagate(False)

canvas.create_text(10,10, text="1 -")

#prava
canvas.create_line(100, 0, 100, 100, fill='lightgray', width=2)

#dolna
canvas.create_line(0, 100, 100, 100, fill='black', width=2)

#lava
canvas.create_line(0, 0, 0, 100, fill="black", width= 2)

#horna
canvas.create_line(0, 0, 100, 0, fill="black", width=2)


########################################################################

canvas = tk.Canvas(window, width=100, height=100, bg='white', highlightthickness=0)
canvas.grid(row=2, column=1, sticky="nsew")
canvas.grid_propagate(False)

#prava
canvas.create_line(100, 0, 100, 100, fill='black', width=2)

#dolna
canvas.create_line(0, 100, 100, 100, fill='black', width=2)

#lava
canvas.create_line(0, 0, 0, 100, fill="lightgray", width= 2)

#horna
canvas.create_line(0, 0, 100, 0, fill="black", width=2)

########################################################################

canvas = tk.Canvas(window, width=100, height=100, bg='white', highlightthickness=0)
canvas.grid(row=2, column=2, padx=(0,20), sticky="nsew")
canvas.grid_propagate(False)

#prava
canvas.create_line(100, 0, 100, 100, fill='black', width=2)

#dolna
canvas.create_line(0, 100, 100, 100, fill='black', width=2)

#lava
canvas.create_line(0, 0, 0, 100, fill="black", width= 2)

#horna
canvas.create_line(0, 0, 100, 0, fill="lightgray", width=2)



""" 
canvas = tk.Canvas(window, width=100, height=100, bg='green')
canvas.grid(row=0, column=1, padx=(20, 0), pady=(20,0))
canvas.grid_propagate(False)

# Nakresli čiaru na pravej strane
canvas.create_line(102, 0, 102, 102, fill='red', width=3)

# Nakresli čiaru na dolnej strane
canvas.create_line(0, 102, 102, 102, fill='yellow', width=3) """


window.mainloop()