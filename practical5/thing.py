import turtle
import random
from configparser import ConfigParser

class Thing:
    def __init__(self, graphicFile):
        self._turtle = turtle.Turtle()
        # pull up the turtle pen:
        self._turtle.up()
        # hide the turtle pen:
        self._turtle.hideturtle()
        # add visual graphic to the turtle pen:
        self._turtle.shape(graphicFile)
        #give turtle crack cocaine and make it go FAST
        self._turtle.speed("fastest")

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
        
        else: return 0 # return status code of 0 if failed to move

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
            return 0 # return status code of 0 if failed to eat
    
class Plant(Thing):
    #values assigned from config file when loading module
    BREED_TICK = None
    BREED_TRESHOLD = None

    def __init__(self):
        super().__init__("Plant.gif")

    def liveALittle(self):
        self._breedTick += Plant.BREED_TICK
        if self._breedTick >= Plant.BREED_TRESHOLD:
            self.tryToBreed()

class Bear(Animal):
    #values assigned from config file when loading module
    BREED_TICK = None
    BREED_TRESHOLD = None
    STARVE_TICK = None
    STARVE_TRESHOLD = None
    ENERGY_TICK = None
    ENERGY_DIE_TRESHOLD = None

    def __init__(self):
        super().__init__("Bear.gif")
        self.__energyTick = 5

    def liveALittle(self):
        #check if to die from low energy
        if self.__energyTick <= Bear.ENERGY_DIE_TRESHOLD:
            self._world.delThing(self)
            return

        self._breedTick += Bear.BREED_TICK
        #check if to breed
        if self._breedTick >= Bear.BREED_TRESHOLD:
            if(self.tryToBreed() == 1):
                self.__energyTick -= Bear.ENERGY_TICK

        #try to eat

        if(self.tryToEat(Fish) == 1):
            self.__energyTick += Bear.ENERGY_TICK
        else:
            self._starveTick += Bear.STARVE_TICK

        #check if to starve and die
        if self._starveTick == Bear.STARVE_TRESHOLD:  
            self._world.delThing(self)
            return
       
        #try to move
        if (self.tryToMove() == 1):
            self.__energyTick -= Bear.ENERGY_TICK


class Fish(Animal):
    #values assigned from config file when loading module
    BREED_TICK = None
    BREED_TRESHOLD = None
    STARVE_TICK = None
    STARVE_TRESHOLD = None
    ADJ_FISH_TRESHOLD = None
    
    def __init__(self):
        super().__init__("Fish.gif")

    def liveALittle(self):
        adjFish = self.getAdjFish()
        #if adjFish reaches treshold, die
        if adjFish >= Fish.ADJ_FISH_TRESHOLD:   
            self._world.delThing(self)
            return
        
        self._breedTick += Fish.BREED_TICK
        #try to breed
        if self._breedTick >= Fish.BREED_TICK:  
            self.tryToBreed()

        #try to eat
        if(self.tryToEat(Plant) == 1):
            pass
        else:
            self._starveTick += Fish.STARVE_TICK        
        
        #check if to starve and die
        if self._starveTick == Fish.STARVE_TRESHOLD:  
            self._world.delThing(self)
            return
        
        #try to move
        self.tryToMove()

    def getAdjFish(self):
        #This method checks all 8 surrounding squares
        #and checks if in those squares are other fish
        #if yes, add to adjFish count
        #then returns adjFish

        # coordinates around the fish:
        offsetList = [(-1,1), (0,1), (1,1),
                  (-1,0),        (1,0),
                  (-1,-1),(0,-1),(1,-1)]
        
        adjFish = 0  #count of the  adjacent Fish

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

        return adjFish


#read values from config 
print("[thing.py] Fetching values from config file ...")
try:
    config = ConfigParser()
    config.read("config.ini")

    Fish.BREED_TICK = config.getint("fish", "breedTick")
    Fish.BREED_TRESHOLD = config.getint("fish", "breedTreshold")
    Fish.STARVE_TICK = config.getint("fish", "starveTick")
    Fish.STARVE_TRESHOLD = config.getint("fish", "starveTreshold")
    Fish.ADJ_FISH_TRESHOLD = config.getint("fish", "adjFishThreshold")

    Bear.BREED_TICK = config.getint("bear", "breedTick")
    Bear.BREED_TRESHOLD = config.getint("bear", "breedTreshold")
    Bear.STARVE_TICK = config.getint("bear", "starveTick")
    Bear.STARVE_TRESHOLD = config.getint("bear", "starveTreshold")
    Bear.ENERGY_TICK = config.getint("bear", "energyTick")
    Bear.ENERGY_DIE_TRESHOLD = config.getint("bear", "eneryDieTreshold")

    Plant.BREED_TICK = config.getint("plant", "breedTick")
    Plant.BREED_TRESHOLD = config.getint("plant", "breedTreshold")

except Exception as e:
    print("Error:",e)
    exit()
else:
    print("SUCCESS!")

    

    
    