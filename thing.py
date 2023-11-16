import turtle
import random

class Thing:
    def __init__(self, graphicFile):
        self._turtle = turtle.Turtle()
        # pull up the turtle pen:
        self._turtle.up()
        # hide the turtle pen:
        self._turtle.hideturtle()
        # add visual graphic to the turtle pen:
        self._turtle.shape(graphicFile)

        # set the turtle postitions:
        self._xPos = 0
        self._yPos = 0
        # set world to empty:
        self._world = None

        self._breedTick = 0

    def setX(self, newX):
        self._xPos = newX

    def setY(self, newY):
        self._yPos = newY

    def getX(self):
        return self._xPos

    def getY(self):
        return self._yPos

    def setWorld(self, aWorld):
        self._world = aWorld

    def appear(self):
        self._turtle.goto(self._xPos, self._yPos)
        self._turtle.showturtle()

    def hide(self):
        self._turtle.hideturtle()

    def tryToBreed(self):
        offsetList = [(-1,1), (0,1), (1,1),
                      (-1,0),        (1,0),
                      (-1,-1),(0,-1),(1,-1)]
        # get a random coordinate around a thing:
        randomOffsetIndex = random.randrange(len(offsetList))
        randomOffset = offsetList[randomOffsetIndex]
        nextX = self._xPos + randomOffset[0]
        nextY = self._yPos + randomOffset[1]
        # check if not off the grid:
        while not (0 <= nextX < self._world.getMaxX() and \
                   0 <= nextY < self._world.getMaxY() ):
            # get a random coordinate around a thing:
            randomOffsetIndex = random.randrange(len(offsetList))
            randomOffset = offsetList[randomOffsetIndex]
            nextX = self._xPos + randomOffset[0]
            nextY = self._yPos + randomOffset[1]

        # add new child thing if coordinate is empty:
        if self._world.emptyLocation(nextX, nextY):
           childThing = type(self)()
           self._world.addThing(childThing, nextX, nextY)
           self._breedTick = 0     #reset breedTick
           return 1 # return status code of 1 if successfuly breaded


class Animal(Thing):
    def __init__(self, graphicFile):
        super().__init__(graphicFile)
        self._starveTick = 0

    def move(self, newX, newY):
        self._world.moveThing(self._xPos, self._yPos, newX, newY)
        self._xPos = newX
        self._yPos = newY
        self._turtle.goto(self._xPos, self._yPos)

    def tryToMove(self):
        offsetList = [(-1,1), (0,1), (1,1),
                      (-1,0),        (1,0),
                      (-1,-1),(0,-1),(1,-1)]
        randomOffsetIndex = random.randrange(len(offsetList))
        randomOffset = offsetList[randomOffsetIndex]
        nextX = self._xPos + randomOffset[0]
        nextY = self._yPos + randomOffset[1]
        while not(0 <= nextX < self._world.getMaxX() and \
                  0 <= nextY < self._world.getMaxY() ):
            randomOffsetIndex = random.randrange(len(offsetList))
            randomOffset = offsetList[randomOffsetIndex]
            nextX = self._xPos + randomOffset[0]
            nextY = self._yPos + randomOffset[1]
        # move to the coordinate if empty
        if self._world.emptyLocation(nextX, nextY):
           self.move(nextX, nextY)
           return 1 # return status code of 1 if successfuly moved

    def tryToEat(self, validPrey):
        offsetList = [(-1,1), (0,1) ,(1,1),
                      (-1,0),        (1,0),
                      (-1,-1),(0,-1),(1,-1)]
        adjPrey = []     #create list of adjacent prey
        for offset in offsetList:
            newX = self._xPos + offset[0]
            newY = self._yPos + offset[1]
            if 0 <= newX < self._world.getMaxX() and \
               0 <= newY < self._world.getMaxY():
                # check if a valid prey is nearby:
                if (not self._world.emptyLocation(newX, newY)) and  \
		          isinstance(self._world.lookAtLocation(newX, newY), validPrey):
                    # add the location of prey:
                    adjPrey.append(self._world.lookAtLocation(newX, newY))

        if len(adjPrey) > 0:  #if any prey are adjacent, pick random prey to eat
            randomPrey = adjPrey[random.randrange(len(adjPrey))]
            preyX = randomPrey.getX()
            preyY = randomPrey.getY()

            self._world.delThing(randomPrey)  #delete the prey
            self.move(preyX, preyY)            #move to the preys location
            self._starveTick = 0
            return 1 # return status code of 1 if successfuly ate
        else:
            self._starveTick = self._starveTick + 1    # increase starveTick
    
class Plant(Thing):
    def __init__(self):
        super().__init__("Plant.gif")

    def liveALittle(self):
        self._breedTick = self._breedTick + 1
        if self._breedTick >= 5:
            self.tryToBreed()

class Bear(Animal):
    def __init__(self):
        super().__init__("Bear.gif")
        self.__energyTick = 5

    def liveALittle(self):

        if self.__energyTick <= 0:  #if energy gets to 0 or below, die
            self._world.delThing(self)
            return

        self._breedTick = self._breedTick + 2
        if self._breedTick >= 8:  #if alive 8 or more ticks, breed
            if(self.tryToBreed() == 1):
                self.__energyTick = self.__energyTick - 1  # decrease energyTick
            

        if(self.tryToEat(Fish) == 1):
            self.__energyTick = self.__energyTick + 1 # increase energyTick

        if self._starveTick == 10:  #if not eaten for 10 ticks, die
            self._world.delThing(self)
            return
        else:
            if (self.tryToMove() == 1):
               self.__energyTick = self.__energyTick - 1    # decrease energyTick 


class Fish(Animal):
    def __init__(self):
        super().__init__("Fish.gif")

    def liveALittle(self):
        # coordinates around the fish:
        offsetList = [(-1,1), (0,1), (1,1),
                      (-1,0),        (1,0),
                      (-1,-1),(0,-1),(1,-1)]
        adjFish = 0  #count adjacent Fish
        for offset in offsetList:
            newX = self._xPos + offset[0]
            newY = self._yPos + offset[1]
            # check if the coordinate is in the grid:
            if 0 <= newX < self._world.getMaxX()  and \
                  0 <= newY < self._world.getMaxY():
                # if coordinate is not empty then note that there is a fish
                if (not self._world.emptyLocation(newX, newY)) and \
                    isinstance(self._world.lookAtLocation(newX, newY), Fish):
                    adjFish = adjFish + 1

        if adjFish >= 2:   #if 2 or more adjacent Fish, die
            self._world.delThing(self)
            return
        else:
            # increase breedtick by 1:
            self._breedTick = self._breedTick + 1
            if self._breedTick >= 12:  #if alive 12 or more ticks, breed
                self.tryToBreed()

        self.tryToEat(Plant)           #try to eat
        
        if self._starveTick == 30:  #if not eaten for 30 ticks, die
            self._world.delThing(self)
        else:
            self.tryToMove()
    
    