import turtle
import random
import thing

class World:
    # constructor
    def __init__(self, mX, mY):
        self.__maxX = mX
        self.__maxY = mY
        self.__thingList = []
        self.__grid = []

        for aRow in range(self.__maxY):
            row = []
            for aCol in range(self.__maxX):
                # append empty value:
                row.append(None)
            self.__grid.append(row)
        
        # create world turtle object:
        self.__wTurtle = turtle.Turtle()
        # create screen object:
        self.__wScreen = turtle.Screen()
        # set the screen num of cols and rows the same as grids cols and rows:
        self.__wScreen.setworldcoordinates(0, 0, self.__maxX - 1, 
                                           self.__maxY - 1)
        # add gifs to the screen object:
        self.__wScreen.addshape("Bear.gif")
        self.__wScreen.addshape("Fish.gif")
        self.__wScreen.addshape("Plant.gif")
        # hide the arrow:
        self.__wTurtle.hideturtle()
        
    def draw(self):
        # turn off turtle animation:
        self.__wScreen.tracer(0)
        # draw the grid:
        self.__wTurtle.forward(self.__maxX - 1)
        self.__wTurtle.left(90)
        self.__wTurtle.forward(self.__maxY - 1)
        self.__wTurtle.left(90)
        self.__wTurtle.forward(self.__maxX - 1)
        self.__wTurtle.left(90)
        self.__wTurtle.forward(self.__maxY - 1)
        self.__wTurtle.left(90)
        for i in range(self.__maxY - 1):
            self.__wTurtle.forward(self.__maxX - 1)
            self.__wTurtle.backward(self.__maxX - 1)
            self.__wTurtle.left(90)
            self.__wTurtle.forward(1)
            self.__wTurtle.right(90)
        self.__wTurtle.forward(1)
        self.__wTurtle.right(90)
        for i in range(self.__maxX - 2):
            self.__wTurtle.forward(self.__maxY - 1)
            self.__wTurtle.backward(self.__maxY - 1)
            self.__wTurtle.left(90)
            self.__wTurtle.forward(1)
            self.__wTurtle.right(90)
        # turn back on turtle animation
        self.__wScreen.tracer(1)

    def addThing(self, aThing, x, y):
        aThing.setX(x)
        aThing.setY(y)
        self.__grid[y][x] = aThing       #add life-form to grid
        aThing.setWorld(self)
        self.__thingList.append(aThing)  #add to list of life-forms
        aThing.appear()

    def delThing(self, aThing):
        aThing.hide()
        self.__grid[aThing.getY()][aThing.getX()] = None
        self.__thingList.remove(aThing)

    def moveThing(self, oldX, oldY, newX, newY):
        self.__grid[newY][newX] = self.__grid[oldY][oldX]
        self.__grid[oldY][oldX] = None

    def getMaxX(self):
        return self.__maxX

    def getMaxY(self):
        return self.__maxY


    def liveALittle(self):
        if self.__thingList != [ ]:
           aThing = random.randrange(len(self.__thingList))
           randomThing = self.__thingList[aThing]
           randomThing.liveALittle()
    
    # check if in the coordinates there are no things:
    def emptyLocation(self, x, y):
        if self.__grid[y][x] == None:
            return True
        else:
            return False

    def lookAtLocation(self, x, y):
        return self.__grid[y][x]

    def freezeWorld(self):
        self.__wScreen.exitonclick()
    
    # count fish
    def countFish(self):
        numOfFish = 0
        for i in range(self.__maxX):
            for j in range(self.__maxY):
                if (not self.emptyLocation(i, j)) and \
                    isinstance(self.lookAtLocation(i, j), thing.Fish):
                    numOfFish = numOfFish + 1
        return numOfFish
    
    # count bears
    def countBears(self):
        numOfBears = 0
        for i in range(self.__maxX):
            for j in range(self.__maxY):
                if (not self.emptyLocation(i, j)) and \
                    isinstance(self.lookAtLocation(i, j), thing.Bear):
                    numOfBears = numOfBears + 1
        return numOfBears
    
    # count plants
    def countPlants(self):
        numOfPlants = 0
        for i in range(self.__maxX):
            for j in range(self.__maxY):
                if (not self.emptyLocation(i, j)) and \
                    isinstance(self.lookAtLocation(i, j), thing.Plant):
                    numOfPlants = numOfPlants + 1
        return numOfPlants
    


def mainSimulation():
    numberOfBears = 10
    numberOfFish = 10
    numberOfPlants = 10
    worldLifeTime = 2500
    worldWidth = 50
    worldHeight = 25
 
    # create world class object:
    myWorld = World(worldWidth, worldHeight)
    # draw the grid:
    myWorld.draw()

    # add fish:
    for i in range(numberOfFish):
        # create fish object:
        newFish = thing.Fish()
        # set random number between 0 and max width:
        x = random.randrange(myWorld.getMaxX())
        # set random number between 0 and max height:
        y = random.randrange(myWorld.getMaxY())
        # when random generated coordinates are not empty:
        while not myWorld.emptyLocation(x, y):
            # set new random coordinates:
            x = random.randrange(myWorld.getMaxX())
            y = random.randrange(myWorld.getMaxY())
        # add fish to the random generated coordinates:
        myWorld.addThing(newFish, x, y)

    # add bears:
    for i in range(numberOfBears):
        newBear = thing.Bear()
        x = random.randrange(myWorld.getMaxX())
        y = random.randrange(myWorld.getMaxY())
        while not myWorld.emptyLocation(x, y):
            x = random.randrange(myWorld.getMaxX())
            y = random.randrange(myWorld.getMaxY())
        myWorld.addThing(newBear, x, y)

    # add plants:
    for i in range(numberOfPlants):
        newPlant = thing.Plant()
        x = random.randrange(myWorld.getMaxX())
        y = random.randrange(myWorld.getMaxY())
        while not myWorld.emptyLocation(x, y):
            x = random.randrange(myWorld.getMaxX())
            y = random.randrange(myWorld.getMaxY())
        myWorld.addThing(newPlant, x, y)

    all = []
    for i in range(worldLifeTime):
        myWorld.liveALittle()

        row = []
        numOfFish = myWorld.countFish()
        numOfBears = myWorld.countBears()
        numOfPlants = myWorld.countPlants()
        row.append(i)
        row.append(numOfFish)
        row.append(numOfBears)
        row.append(numOfPlants)
        all.append(row)
        
    myWorld.freezeWorld()

    f = open("table.txt", "a")
    for i in range(len(all)):
        row = []
        for j in range(len(all[i])):
            row.append(all[i][j])
        f.write("Time: " + str(row[0]) + "; Num of Fish:  " + str(row[1]) + "; Num of bears: " + str(row[2]) +  "; Num of plants: " + str(row[3]) + " \n")
    f.close()

mainSimulation()
