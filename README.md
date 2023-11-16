## Python-pw5

## TASK: Using Visual Studio Code environment write Python program with latter mentioned requirements.

5.2.1. Use Fish and Bear simulated world and the accordant code (Fish, Bear, Plant and World
classes) introduced in our lecture material (i.e. 5.2. Part material).

[a]
Modify the
mainSimulation function to create two lists. One list will keep track of the number of fish that
are alive in each time unit, and the other will keep track of the number of bears. When the
simulation is done, this data should be written to a file. The file should have three columns: one
column for the time, one for the number of fish, and one for the number of bears.

[b]
Two events
can cause a Bear to die: starvation and energy level dropping to 0. Develop accordant energy
representing instance variable in class Bear and set the initial energy level (i.e. integer). Update
accordingly class Bear to decrease energy level if bear is breeding or moving, and increase
energy level if bear is eating. Bear is dead if energy level drops below 0.

Load all the necessary classes and run the Fish and Bear simulation. In description document
include runtime screenshots of above solutions.

# The Solution

## Inheretince implementation

The original code base had a lot of redudency, so we reduced the code size by 30% by implimenting inheritence. We identified the code shared by Plant, Bear and Fish class and consolidate it.

Creating the following code hierarchy:

> Thing -> Plant  
> Thing -> Animal -> Bear  
> Thing -> Animal -> Fish

However this approach came in conflict with Bear energy functinonality. The bear class needed to know the result of tryToEat(), tryToBreed() and tryToMove() that is located in the parent class Animal in order to decide if to increase or decrease energy.

The solution was to this problem was to make it so that the aforementioned methods return status code 1 for success (ie. if successfuly breaded, return 1). Thus the bear or any other child class can use this information for internal logic.

<img width="847" alt="Screenshot 2023-11-13 at 19 45 46" src="https://github.com/danieladupusamezgaile/Python-pw5/assets/113204311/b36dcdef-8c30-4b14-83b9-9050f37e10b9">
