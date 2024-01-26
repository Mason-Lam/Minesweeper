from tkinter import *
from tkinter import messagebox
import random


class MinesweeperCell(Label):
    """represents a minesweeper cell"""

    def __init__(self, master, coord):
        """cell=MinesweeeperCell(master,coord)->MinesweeperCell
        creates a blank minesweeper cell with a coordinate"""
        Label.__init__(self, master, height=1, width=2, text='',
                       bg='white', font=('Arial', 18), relief=RAISED)
        self.flagged = False  # attribute to store whether square is flagged
        self.reveal = False  # attribute to store whether the square is exposed
        self.coord = coord  # attribute to store the location of the square
        self.number = 0  # attribute to store the number of bombs
        self.bind('<Button-1>', self.expose)  # exposes the square when left-clicked
        self.bind('<Button-3>', self.flag)  # flags or un-flags a square when right-clicked

    def expose(self, event):
        """MinesweeperCell.expose(event)->None
        exposes a square if it is not flagged or
        already revealed"""
        # checks if the square is not revealed or flagged
        if not self.is_revealed() and not self.is_flagged():
            self['relief'] = SUNKEN
            # checks if the number is not a bomb
            if self.get_number() != 10:
                colormap = ['light gray', 'blue', 'darkgreen', 'red', 'purple', 'maroon', 'cyan', 'black', 'dim gray']
                self['bg'] = 'light gray'  # changes the background of the square
                self['fg'] = colormap[self.number]  # changes the color of the text
                self['text'] = self.number  # changes the text to the number
                self.reveal = True  # changes the reveal attribute to True
                self.master.exposed += 1  # alerts the Minesweeper grid a square has been exposed
                self.master.win()  # runs the minesweeper grid win function to check for a win
                if self.get_number() == 0:
                    self.master.blank(self.coord)
            else:
                self.master.lose()  # class the minesweeper grid lose function to tell the user they lost

    def flag(self, event):
        """Marks the square as a bomb"""
        # if statement to check if the square is not revealed
        if not self.is_revealed():
            # if statement to check if the square is already flagged
            if not self.is_flagged():
                # checks if the user has already flagged the amount of bombs on the grid
                if self.master.get_bombs() > 0:
                    self['text'] = 'F'  # changes the text to an asterisk
                    self.flagged = True  # changes the flagged attribute to True
                    self.master.numBombs -= 1  # alerts the grid that the user has flagged
            else:
                self['text'] = ''  # changes the text to a blank
                self.flagged = False  # changes the flagged attribute to False
                self.master.numBombs += 1  # alerts the grid the user has un-flagged a bomb
            self.master.bombLabel['text'] = str(self.master.get_bombs())  # updates the bomb label

    def is_flagged(self):
        """Checks if the cell is flagged"""
        return self.flagged

    def is_revealed(self):
        """Checks if the cell is revealed"""
        return self.reveal

    def get_number(self):
        """MinesweeperCell.get_number()->int
        returns the number of bombs next to a cell"""
        return self.number


class MinesweeperGrid(Frame):
    """object for a Minesweeper grid"""

    def __init__(self, master, width, height, bombs):
        """grid=MinesweeperGrid(master,width,height,bombs)->MinesweeperGrid
        creates a Minesweeper Grid with the dimension width*height and a number
        of bombs"""
        Frame.__init__(self, master, bg='white')  # initializes the grid as a frame
        self.grid()

        # for loops to add lines in between each row and column
        for column in range(1, width * 2 - 1, 2):
            self.columnconfigure(column, minsize=1)
        for row in range(1, height * 2 - 1, 2):
            self.rowconfigure(row, minsize=1)

        self.cells = {}  # dictionary to store each cell
        # for loop that cycles the length of width
        for column in range(width):
            # for loop that cycles the length of height
            for row in range(height):
                self.cells[(row, column)] = MinesweeperCell(self, (row, column))  # creates a new MinesweeperCell
                self.cells[(row, column)].grid(row=2 * row, column=2 * column)  # grids the new cell

        self.numBombs = bombs  # attribute to store the number of bombs minus the number of cells flagged
        self.area = width * height - bombs # attribute to store the area of the grid minus bombs
        self.exposed = 0  # stores the number of squares exposed by the user
        count = bombs  # counting variable equal to the number of bombs
        self.BombList = []  # list to store the coordinates of each bomb
        # while loop that runs until each bomb has been added
        while count > 0:
            bomb = (random.randrange(0, height), random.randrange(0, width))
            # if statement to check if the cell chosen is already a bomb
            if self.cells[bomb].number != 10:
                self.cells[bomb].number = 10  # changes the cell value to a bomb
                self.BombList.append(bomb)  # adds the cell to the bomb list
                count -= 1
        # for loop that cycles through each bomb
        for bomb in self.BombList:
            # for loop that cycles through each cell
            for cell in self.cells:
                # if statement to check if the cell is not a bomb and is next to a bomb
                if self.cells[cell].get_number() != 10 and MinesweeperGrid.nearby(bomb, cell):
                    self.cells[cell].number += 1
        self.bombLabel = Label(self, text=str(bombs), font=('impact', 24),
                               bg='white')  # creates a label to display the number of bombs
        self.bombLabel.grid(row=(height * 2) + 1, columnspan=width * 2)
        # solve button
        Button(self, text='Solve', font=('impact', 16), command=self.solve).grid(row=(height * 2) + 2,
                                                                                 columnspan=width * 2)
        # reset button
        self.height = height
        self.width = height
        Button(self, text='Reset', font=('impact', 16), command=self.reset).grid(row=(height * 2) + 3,
                                                                                 columnspan=width * 2)

    @staticmethod
    def nearby(one, two):
        """Checks if the two cells are adjacent"""
        return (abs(one[0] - two[0]) == 1 or abs(one[0] - two[0]) == 0) and (
                abs(one[1] - two[1]) == 1 or abs(one[1] - two[1]) == 0)

    def blank(self, coord):
        """function that exposes all squares
        within one unit of a coordinate"""
        # for that cycles through each cell
        for cell in self.cells:
            # if statement to check if the cells are adjacent
            if self.nearby(coord, cell):
                self.cells[cell].expose('<Button-1>')  # exposes the cell

    def lose(self):
        """Alerts the user they lost"""
        # for loop that cycles through each bomb's coord
        for bomb in self.BombList:
            # checks if the bomb is not flagged
            if not self.cells[bomb].is_flagged():
                # highlights the bomb and reveals it
                self.cells[bomb]['text'] = '*'
                self.cells[bomb]['bg'] = 'red'
        # for loop that changes every cells' reveal attribute to true
        for cell in self.cells:
            self.cells[cell].reveal = True
        messagebox.showerror('Minesweeper', 'KABOOM! You lose.', parent=self)  # creates a message box
        self.master.destroy()
        setup_minesweeper()

    def win(self):
        """Checks for a win and alerts
        the user if so"""
        # checks if the number of squares exposed is equal to the area
        if self.exposed == self.area:
            messagebox.showinfo('Minesweeper', 'Congratulations -- you won!', parent=self)  # creates a message box
            # set each bombs reveal attribute to true
            for bomb in self.BombList:
                self.cells[bomb].reveal = True
            self.master.destroy()
            setup_minesweeper()

    def get_bombs(self):
        """Returns the current number of boms
        minus the squares flagged"""
        return self.numBombs

    def solve(self):
        """Solves a minesweeper Grid"""
        # for loop that cycles through each bomb
        for bomb in self.BombList:
            # checks if the bomb is not flagged
            if not self.cells[bomb].is_flagged():
                # highlights the bomb and reveals it
                self.cells[bomb].flag('<Button-2>')

        for cell in self.cells:
            # checks for bomb
            if self.cells[cell].get_number() != 10:
                # checks for flag
                if self.cells[cell].is_flagged():
                    self.cells[cell].flag('<Button-2>')
                self.cells[cell].expose('<Button-1>')

    def reset(self):
        """Resets the Minesweeper Grid with the same
        width length and bomb settings"""
        # sets each cell as not being revealed
        for cell in self.cells:
            self.cells[cell].reveal = False
            if self.cells[cell].is_flagged():
                self.cells[cell].flag('<Button-2>')
            self.cells[cell].number = 0
            self.cells[cell]['relief'] = RAISED
            self.cells[cell]['text'] = ''
            self.cells[cell]['bg'] = 'white'
            self.cells[cell]['fg'] = 'black'
        self.BombList = []
        # resets the bomb locations
        count = self.numBombs
        while count > 0:
            bomb = (random.randrange(0, self.height), random.randrange(0, self.width))
            # if statement to check if the cell chosen is already a bomb
            if self.cells[bomb].number != 10:
                self.cells[bomb].number = 10  # changes the cell value to a bomb
                self.BombList.append(bomb)  # adds the cell to the bomb list
                count -= 1
        # for loop that cycles through each bomb
        for bomb in self.BombList:
            # for loop that cycles through each cell
            for cell in self.cells:
                # if statement to check if the cell is not a bomb and is next to a bomb
                if self.cells[cell].get_number() != 10 and self.nearby(bomb, cell):
                    self.cells[cell].number += 1
        self.exposed = 0
        self.bombLabel['text'] = str(self.get_bombs())


class MinesweeperMenu(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, bg='white')  # initializes the grid as a frame
        self.grid()
        # self.master = master
        self.width = IntVar()
        self.height = IntVar()
        self.bombs = IntVar()
        self.width.set(24)
        self.height.set(20)
        self.bombs.set(99)

        Label(self, text="Width").grid(row=0, column=0, padx=(100, 0), pady=(50, 10))
        Label(self, text="Height").grid(row=1, column=0, padx=(100, 0), pady=(0, 10))
        Label(self, text="Bombs").grid(row=2, column=0, padx=(100, 0))
        Entry(self, textvariable=self.width).grid(row=0, column=1, padx=(0, 100), pady=(50, 10))
        Entry(self, textvariable=self.height).grid(row=1, column=1, padx=(0, 100), pady=(0, 10))
        Entry(self, textvariable=self.bombs).grid(row=2, column=1, padx=(0, 100), pady=(0, 10))

        Button(self, text="Initialize Game", command=self.init_game).grid(row=3, column=0, padx=(100, 0), pady=(0, 50))

    def init_game(self):
        if self.bombs.get() > self.width.get() * self.height.get() - 9:
            messagebox.showerror('Minesweeper Menu', 'Invalid Input', parent=self.master)
            return
        self.master.destroy()
        play_minesweeper(self.width.get(), self.height.get(), self.bombs.get())


def play_minesweeper(width, height, bombs):
    """Plays a game of minesweeper with a specified
    width, height, and bombs in the grid"""
    root = Tk()
    root.title('Minesweeper')
    minesweeper = MinesweeperGrid(root, width, height, bombs)
    minesweeper.mainloop()


def setup_minesweeper():
    root = Tk()
    root.title('Minesweeper Menu')
    minesweeper_menu = MinesweeperMenu(root)
    minesweeper_menu.mainloop()


# play_minesweeper(10, 10, 10)
setup_minesweeper()
