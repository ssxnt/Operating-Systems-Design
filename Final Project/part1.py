# Group#: 4
# Student Names: Katie Goncalves & Sant Sumetpong

"""
    This program implements a variety of the snake
    game (https://en.wikipedia.org/wiki/Snake_(video_game_genre))
"""

import threading
import queue  # the thread-safe queue from Python standard library

from tkinter import Tk, Canvas, Button
import random, time


class Gui():
    """
        This class takes care of the game's graphic user interface (gui)
        creation and termination.
    """

    def __init__(self):
        """
            The initializer instantiates the main window and
            creates the starting icons for the snake and the prey,
            and displays the initial gamer score.
        """
        # some GUI constants
        scoreTextXLocation = 60
        scoreTextYLocation = 15
        textColour = "orange"
        # instantiate and create gui
        self.root = Tk()
        self.canvas = Canvas(self.root, width=WINDOW_WIDTH,
                             height=WINDOW_HEIGHT, bg=BACKGROUND_COLOUR)
        self.canvas.pack()
        # create starting game icons for snake and the prey
        self.snakeIcon = self.canvas.create_line(
            (0, 0), (0, 0), fill=ICON_COLOUR, width=SNAKE_ICON_WIDTH)
        self.preyIcon = self.canvas.create_rectangle(
            0, 0, 0, 0, fill=ICON_COLOUR, outline=ICON_COLOUR)
        # display starting score of 0
        self.score = self.canvas.create_text(
            scoreTextXLocation, scoreTextYLocation, fill=textColour,
            text='Your Score: 0', font=("Helvetica", "11", "bold"))
        # binding the arrow keys to be able to control the snake
        for key in ("Left", "Right", "Up", "Down"):
            self.root.bind(f"<Key-{key}>", game.whenAnArrowKeyIsPressed)

    def gameOver(self):
        """
            This method is used at the end to display a
            game over button.
        """
        gameOverButton = Button(self.canvas, text="Game Over!",
                                height=3, width=10, font=("Helvetica", "14", "bold"),
                                command=self.root.destroy)
        self.canvas.create_window(200, 100, anchor="nw", window=gameOverButton)


class QueueHandler():
    """
        This class implements the queue handler for the game.
    """

    def __init__(self):
        self.queue = gameQueue
        self.gui = gui
        self.queueHandler()

    def queueHandler(self):
        '''
            This method handles the queue by constantly retrieving
            tasks from it and accordingly taking the corresponding
            action.
            A task could be: game_over, move, prey, score.
            Each item in the queue is a dictionary whose key is
            the task type (for example, "move") and its value is
            the corresponding task value.
            If the queue.empty exception happens, it schedules
            to call itself after a short delay.
        '''
        try:
            while True:
                task = self.queue.get_nowait()
                if "game_over" in task:
                    gui.gameOver()
                elif "move" in task:
                    points = [x for point in task["move"] for x in point]
                    gui.canvas.coords(gui.snakeIcon, *points)
                elif "prey" in task:
                    gui.canvas.coords(gui.preyIcon, *task["prey"])
                elif "score" in task:
                    gui.canvas.itemconfigure(
                        gui.score, text=f"Your Score: {task['score']}")
                self.queue.task_done()
        except queue.Empty:
            gui.root.after(100, self.queueHandler)


class Game():
    '''
        This class implements most of the game functionalities.
    '''

    def __init__(self):
        """
           This initializer sets the initial snake coordinate list, movement
           direction, and arranges for the first prey to be created.
        """
        self.queue = gameQueue
        self.score = 0
        # starting length and location of the snake
        # note that it is a list of tuples, each being an
        # (x, y) tuple. Initially its size is 5 tuples.
        self.snakeCoordinates = [(495, 55), (485, 55), (475, 55),
                                 (465, 55), (455, 55)]
        # initial direction of the snake
        self.direction = "Left"
        self.gameNotOver = True
        self.createNewPrey()

    def superloop(self) -> None:
        """
            This method implements a main loop
            of the game. It constantly generates "move"
            tasks to cause the constant movement of the snake.
            Use the SPEED constant to set how often the move tasks
            are generated.
        """
        SPEED = 0.15  # speed of snake updates (sec)
        while self.gameNotOver:
            # complete the method implementation below
            while self.gameNotOver:
                self.move()
                time.sleep(SPEED)
            # pass  # remove this line from your implementation

    def whenAnArrowKeyIsPressed(self, e) -> None:
        """
            This method is bound to the arrow keys
            and is called when one of those is clicked.
            It sets the movement direction based on
            the key that was pressed by the gamer.
            Use as is.
        """
        currentDirection = self.direction
        # ignore invalid keys
        if (currentDirection == "Left" and e.keysym == "Right" or
                currentDirection == "Right" and e.keysym == "Left" or
                currentDirection == "Up" and e.keysym == "Down" or
                currentDirection == "Down" and e.keysym == "Up"):
            return
        self.direction = e.keysym

    def move(self) -> None:
        """
            This method implements what is needed to be done
            for the movement of the snake.
            It generates a new snake coordinate.
            If based on this new movement, the prey has been
            captured, it adds a task to the queue for the updated
            score and also creates a new prey.
            It also calls a corresponding method to check if
            the game should be over.
            The snake coordinates list (representing its length
            and position) should be correctly updated.
        """
        NewSnakeCoordinates = self.calculateNewCoordinates()
        # complete the method implementation below
        

    def calculateNewCoordinates(self) -> tuple:
        """
            This method calculates and returns the new
            coordinates to be added to the snake
            coordinates list based on the movement
            direction and the current coordinate of
            head of the snake.
            It is used by the move() method.
        """
        lastX, lastY = self.snakeCoordinates[-1]
        # complete the method implementation below

    def isGameOver(self, snakeCoordinates) -> None:
        """
            This method checks if the game is over by
            checking if now the snake has passed any wall
            or if it has bit itself.
            If that is the case, it updates the gameNotOver
            field and also adds a "game_over" task to the queue.
        """
        x, y = snakeCoordinates
        # complete the method implementation below

    def createNewPrey(self) -> None:
        """
            This methods picks an x and a y randomly as the coordinate
            of the new prey and uses that to calculate the
            coordinates (x - 5, y - 5, x + 5, y + 5). [you need to replace 5 with a constant]
            It then adds a "prey" task to the queue with the calculated
            rectangle coordinates as its value. This is used by the
            queue handler to represent the new prey.
            To make playing the game easier, set the x and y to be THRESHOLD
            away from the walls.
        """
        THRESHOLD = 15  # sets how close prey can be to borders
        
        # complete the method implementation below
        def is_prey_in_snake(snake_pos, prey_pos) -> bool:
            """
                checks whether or not the newly and randomly generated prey
                coordinates are located inside the snake.

                Arguments:
                    snake_pos (list): single [x, y] coordinate of snake
                    prey_pos (tuple): entire set of coordinates of prey

                Returns:
                    bool: if horizontal and vertical containment is true --> overlap!
            """
            xs, ys = snake_pos  # unpack snake and prey positions
            xp1, yp1, xp2, yp2 = prey_pos
            overlap_x = xp1 <= xs <= xp2  # check for horizontal and vertical overlapping
            overlap_y = yp1 <= ys <= yp2
            
            return overlap_x and overlap_y 
        
        prey_width = PREY_ICON_WIDTH
        prey_height = PREY_ICON_WIDTH  # initialize both x/y min and prey w/h for clarity, even if square
        x_min = THRESHOLD
        y_min = THRESHOLD
        x_max = WINDOW_WIDTH - THRESHOLD - prey_width  # spawn prey outside threshold of border
        y_max = WINDOW_HEIGHT - THRESHOLD - prey_height
        valid_prey_coords = False
        
        while not valid_prey_coords:
            x = random.randint(x_min, x_max)
            y = random.randint(y_min, y_max)
            prey_coords = (x, y, x + prey_width, y + prey_height)  # random coords are generated for prey
            inside = False
            
            for snake_coord in self.snakeCoordinates:  # iterate and check entire length of snake for any prey
                if is_prey_in_snake(snake_coord, prey_coords):  # if prey is inside snake
                    inside = True
                    break
            
            if not inside:
                valid_prey_coords = True  # prey coords are valid
                self.queue.put({"prey": prey_coords})  # new task to be performed by queue         


if __name__ == "__main__":
    # some constants for our GUI
    WINDOW_WIDTH = 500
    WINDOW_HEIGHT = 300
    SNAKE_ICON_WIDTH = 15
    # add the specified constant PREY_ICON_WIDTH here
    PREY_ICON_WIDTH = 10

    BACKGROUND_COLOUR = "aqua"  # you may change this colour if you wish
    ICON_COLOUR = "pink"  # you may change this colour if you wish

    gameQueue = queue.Queue()  # instantiate a queue object using python's queue class

    game = Game()  # instantiate the game object

    gui = Gui()  # instantiate the game user interface

    QueueHandler()  # instantiate the queue handler

    # start a thread with the main loop of the game
    threading.Thread(target=game.superloop, daemon=True).start()

    # start the GUI's own event loop
    gui.root.mainloop()
