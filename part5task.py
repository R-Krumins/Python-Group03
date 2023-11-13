import turtle
import random

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
                    isinstance(self.lookAtLocation(i, j), Fish):
                    numOfFish = numOfFish + 1
        return numOfFish
    
    # count bears
    def countBears(self):
        numOfBears = 0
        for i in range(self.__maxX):
            for j in range(self.__maxY):
                if (not self.emptyLocation(i, j)) and \
                    isinstance(self.lookAtLocation(i, j), Bear):
                    numOfBears = numOfBears + 1
        return numOfBears
    
    # count plants
    def countPlants(self):
        numOfPlants = 0
        for i in range(self.__maxX):
            for j in range(self.__maxY):
                if (not self.emptyLocation(i, j)) and \
                    isinstance(self.lookAtLocation(i, j), Plant):
                    numOfPlants = numOfPlants + 1
        return numOfPlants
    
class Plant:
    def __init__(self):
        self.__turtle = turtle.Turtle()
        # pull up the turtle pen:
        self.__turtle.up()
        # hide the turtle pen:
        self.__turtle.hideturtle()
        # make the fish gif to be the turtle pen:
        self.__turtle.shape("Plant.gif")

        # set the turtle postitions:
        self.__xPos = 0
        self.__yPos = 0
        # set world to empty:
        self.__world = None

        self.__breedTick = 0

    def setX(self, newX):
        self.__xPos = newX

    def setY(self, newY):
        self.__yPos = newY

    def getX(self):
        return self.__xPos

    def getY(self):
        return self.__yPos

    def setWorld(self, aWorld):
        self.__world = aWorld

    def appear(self):
        self.__turtle.goto(self.__xPos, self.__yPos)
        self.__turtle.showturtle()

    def hide(self):
        self.__turtle.hideturtle()


    def liveALittle(self):
        self.__breedTick = self.__breedTick + 1
        if self.__breedTick >= 5:
            self.tryToBreed()


    def tryToBreed(self):
        offsetList = [(-1,1), (0,1), (1,1),
                      (-1,0),        (1,0),
                      (-1,-1),(0,-1),(1,-1)]
        # get a random coordinate around a fish:
        randomOffsetIndex = random.randrange(len(offsetList))
        randomOffset = offsetList[randomOffsetIndex]
        nextX = self.__xPos + randomOffset[0]
        nextY = self.__yPos + randomOffset[1]
        # check if not off the grid:
        while not (0 <= nextX < self.__world.getMaxX() and \
                   0 <= nextY < self.__world.getMaxY() ):
            # get a random coordinate around a fish:
            randomOffsetIndex = random.randrange(len(offsetList))
            randomOffset = offsetList[randomOffsetIndex]
            nextX = self.__xPos + randomOffset[0]
            nextY = self.__yPos + randomOffset[1]

        # add new child fish if coordinate is empty:
        if self.__world.emptyLocation(nextX, nextY):
           childThing = Plant()
           self.__world.addThing(childThing, nextX, nextY)
           self.__breedTick = 0     #reset breedTick

class Fish:
    def __init__(self):
        self.__turtle = turtle.Turtle()
        # pull up the turtle pen:
        self.__turtle.up()
        # hide the turtle pen:
        self.__turtle.hideturtle()
        # make the fish gif to be the turtle pen:
        self.__turtle.shape("Fish.gif")

        # set the turtle postitions:
        self.__xPos = 0
        self.__yPos = 0
        self.__world = None

        self.__breedTick = 0
        self.__starveTick = 0

    def setX(self, newX):
        self.__xPos = newX

    def setY(self, newY):
        self.__yPos = newY

    def getX(self):
        return self.__xPos

    def getY(self):
        return self.__yPos

    def setWorld(self, aWorld):
        self.__world = aWorld

    def appear(self):
        self.__turtle.goto(self.__xPos, self.__yPos)
        self.__turtle.showturtle()

    def hide(self):
        self.__turtle.hideturtle()

    def move(self, newX, newY):
        self.__world.moveThing(self.__xPos, self.__yPos, newX, newY)
        self.__xPos = newX
        self.__yPos = newY
        self.__turtle.goto(self.__xPos, self.__yPos)

    def liveALittle(self):
        # coordinates around the fish:
        offsetList = [(-1,1), (0,1), (1,1),
                      (-1,0),        (1,0),
                      (-1,-1),(0,-1),(1,-1)]
        adjFish = 0  #count adjacent Fish
        for offset in offsetList:
            newX = self.__xPos + offset[0]
            newY = self.__yPos + offset[1]
            # check if the coordinate is in the grid:
            if 0 <= newX < self.__world.getMaxX()  and \
                  0 <= newY < self.__world.getMaxY():
                # if coordinate is not empty then note that there is a fish
                if (not self.__world.emptyLocation(newX, newY)) and \
                    isinstance(self.__world.lookAtLocation(newX, newY), Fish):
                    adjFish = adjFish + 1

        if adjFish >= 2:   #if 2 or more adjacent Fish, die
            self.__world.delThing(self)
        else:
            # increase breedtick by 1:
            self.__breedTick = self.__breedTick + 1
            if self.__breedTick >= 12:  #if alive 12 or more ticks, breed
                self.tryToBreed()

        self.tryToEat()           #try to eat
        
        if self.__starveTick == 30:  #if not eaten for 30 ticks, die
            self.__world.delThing(self)
        else:
            self.tryToMove()

    def tryToBreed(self):
        offsetList = [(-1,1), (0,1), (1,1),
                      (-1,0),        (1,0),
                      (-1,-1),(0,-1),(1,-1)]
        # get a random coordinate around a fish:
        randomOffsetIndex = random.randrange(len(offsetList))
        randomOffset = offsetList[randomOffsetIndex]
        nextX = self.__xPos + randomOffset[0]
        nextY = self.__yPos + randomOffset[1]
        # check if not off the grid:
        while not (0 <= nextX < self.__world.getMaxX() and \
                   0 <= nextY < self.__world.getMaxY() ):
            # get a random coordinate around a fish:
            randomOffsetIndex = random.randrange(len(offsetList))
            randomOffset = offsetList[randomOffsetIndex]
            nextX = self.__xPos + randomOffset[0]
            nextY = self.__yPos + randomOffset[1]

        # add new child fish if coordinate is empty:
        if self.__world.emptyLocation(nextX, nextY):
           childThing = Fish()
           self.__world.addThing(childThing, nextX, nextY)
           self.__breedTick = 0     #reset breedTick

    def tryToMove(self):
        offsetList = [(-1,1), (0,1), (1,1),
                      (-1,0),        (1,0),
                      (-1,-1),(0,-1),(1,-1)]
        randomOffsetIndex = random.randrange(len(offsetList))
        randomOffset = offsetList[randomOffsetIndex]
        nextX = self.__xPos + randomOffset[0]
        nextY = self.__yPos + randomOffset[1]
        while not(0 <= nextX < self.__world.getMaxX() and \
                  0 <= nextY < self.__world.getMaxY() ):
            randomOffsetIndex = random.randrange(len(offsetList))
            randomOffset = offsetList[randomOffsetIndex]
            nextX = self.__xPos + randomOffset[0]
            nextY = self.__yPos + randomOffset[1]
        # move to the coordinate if empty
        if self.__world.emptyLocation(nextX, nextY):
           self.move(nextX, nextY)
    
    def tryToEat(self):
        offsetList = [(-1,1), (0,1) ,(1,1),
                      (-1,0),        (1,0),
                      (-1,-1),(0,-1),(1,-1)]
        adjPrey = []     #create list of adjacent prey
        for offset in offsetList:
            newX = self.__xPos + offset[0]
            newY = self.__yPos + offset[1]
            if 0 <= newX < self.__world.getMaxX() and \
               0 <= newY < self.__world.getMaxY():
                # check if a plant is nearby:
                if (not self.__world.emptyLocation(newX, newY)) and  \
		          isinstance(self.__world.lookAtLocation(newX, newY), Plant):
                    # add the location of a plant:
                    adjPrey.append(self.__world.lookAtLocation(newX, newY))

        if len(adjPrey) > 0:  #if any plants are adjacent, pick random plant to eat
            randomPrey = adjPrey[random.randrange(len(adjPrey))]
            preyX = randomPrey.getX()
            preyY = randomPrey.getY()

            self.__world.delThing(randomPrey)  #delete the plant
            self.move(preyX, preyY)            #move to the plants location
            self.__starveTick = 0
        else:
            self.__starveTick = self.__starveTick + 1    # increase starveTick

class Bear:
    def __init__(self):
        self.__turtle = turtle.Turtle()
        self.__turtle.up()
        self.__turtle.hideturtle()
        self.__turtle.shape("Bear.gif")

        self.__xPos = 0
        self.__yPos = 0
        self.__world = None

        self.__starveTick = 0
        self.__breedTick = 0
        self.__energyTick = 5

    def setX(self, newX):
        self.__xPos = newX

    def setY(self, newY):
        self.__yPos = newY

    def getX(self):
        return self.__xPos

    def getY(self):
        return self.__yPos

    def setWorld(self, aWorld):
        self.__world = aWorld

    def appear(self):
        self.__turtle.goto(self.__xPos, self.__yPos)
        self.__turtle.showturtle()

    def hide(self):
        self.__turtle.hideturtle()

    def move(self, newX, newY):
        self.__world.moveThing(self.__xPos, self.__yPos, newX, newY)
        self.__xPos = newX
        self.__yPos = newY
        self.__turtle.goto(self.__xPos, self.__yPos)

    def tryToBreed(self):
        offsetList = [(-1,1), (0,1), (1,1),
                      (-1,0),        (1,0),
                      (-1,-1),(0,-1),(1,-1)]
        randomOffsetIndex = random.randrange(len(offsetList))
        randomOffset = offsetList[randomOffsetIndex]
        nextX = self.__xPos + randomOffset[0]
        nextY = self.__yPos + randomOffset[1]
        while not (0 <= nextX < self.__world.getMaxX() and \
                   0 <= nextY < self.__world.getMaxY() ):
            randomOffsetIndex = random.randrange(len(offsetList))
            randomOffset = offsetList[randomOffsetIndex]
            nextX = self.__xPos + randomOffset[0]
            nextY = self.__yPos + randomOffset[1]

        if self.__world.emptyLocation(nextX, nextY):
           childThing = Bear()
           self.__world.addThing(childThing, nextX, nextY)
           self.__breedTick = 0     #reset breedTick
           self.__energyTick = self.__energyTick - 1    # decrease energyTick

    def tryToMove(self):
        offsetList = [(-1,1), (0,1), (1,1),
                      (-1,0),        (1,0),
                      (-1,-1),(0,-1),(1,-1)]
        randomOffsetIndex = random.randrange(len(offsetList))
        randomOffset = offsetList[randomOffsetIndex]
        nextX = self.__xPos + randomOffset[0]
        nextY = self.__yPos + randomOffset[1]
        while not(0 <= nextX < self.__world.getMaxX() and \
                  0 <= nextY < self.__world.getMaxY() ):
            randomOffsetIndex = random.randrange(len(offsetList))
            randomOffset = offsetList[randomOffsetIndex]
            nextX = self.__xPos + randomOffset[0]
            nextY = self.__yPos + randomOffset[1]

        if self.__world.emptyLocation(nextX, nextY):
           self.move(nextX, nextY)
           self.__energyTick = self.__energyTick - 1    # decrease energyTick

    def liveALittle(self):

        if self.__energyTick == 0:  #if energy gets to 0, die
            self.__world.delThing(self)

        self.__breedTick = self.__breedTick + 2
        if self.__breedTick >= 8:  #if alive 8 or more ticks, breed
            self.tryToBreed()

        self.tryToEat()

        if self.__starveTick == 10:  #if not eaten for 10 ticks, die
            self.__world.delThing(self)
        else:
            self.tryToMove()
    

    def tryToEat(self):
        offsetList = [(-1,1), (0,1) ,(1,1),
                      (-1,0),        (1,0),
                      (-1,-1),(0,-1),(1,-1)]
        adjPrey = []     #create list of adjacent prey
        for offset in offsetList:
            newX = self.__xPos + offset[0]
            newY = self.__yPos + offset[1]
            if 0 <= newX < self.__world.getMaxX() and \
               0 <= newY < self.__world.getMaxY():
                # check if a fish is nearby:
                if (not self.__world.emptyLocation(newX, newY)) and  \
		          isinstance(self.__world.lookAtLocation(newX, newY), Fish):
                    # add the location of a fish:
                    adjPrey.append(self.__world.lookAtLocation(newX, newY))

        if len(adjPrey) > 0:  #if any Fish are adjacent, pick random Fish to eat
            randomPrey = adjPrey[random.randrange(len(adjPrey))]
            preyX = randomPrey.getX()
            preyY = randomPrey.getY()

            self.__world.delThing(randomPrey)  #delete the Fish
            self.move(preyX, preyY)            #move to the Fishs location
            self.__starveTick = 0
            self.__energyTick = self.__energyTick + 1    # increase energyTick
        else:
            self.__starveTick = self.__starveTick + 1

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
        newFish = Fish()
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
        newBear = Bear()
        x = random.randrange(myWorld.getMaxX())
        y = random.randrange(myWorld.getMaxY())
        while not myWorld.emptyLocation(x, y):
            x = random.randrange(myWorld.getMaxX())
            y = random.randrange(myWorld.getMaxY())
        myWorld.addThing(newBear, x, y)

    # add plants:
    for i in range(numberOfPlants):
        newPlant = Plant()
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
