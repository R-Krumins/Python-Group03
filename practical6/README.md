# Practical #6: Drawing shapes on canvas

## Tasks

[a] Rewrite the Point class, but rather than storing the coordinate information
as separate numbers, store the coordinates as a tuple.

[b] Implement additional Polygon convenience classes such as Triangle, Rectangle, and Octagon. The polygon convenience classes simply inherit from Polygon and set up the point list for the predefined shape.

## Solution

First we migrated all code pertaining to geometry and shapes to it's own file geometry.py.

Second, in Canvas we created exitOnClick() method so we can forestall window closure.

### Task A

in Point class:

> deleted x and y variables  
> created tuple called coord (x, y)

inside the class, when we need to access X - type self.\_\_coord[0], when we need to access Y - type self.\_\_coord[1]

### Task B

Created class Polygon that has:

> list of all its points  
> fill method, to specify that shape needs to be filled on draw  
> draw method implementation

Created Triangle and Square classes, that mainly defines parameter signature (how many points are needed), however there is additional logic for Square.

Square only needs two points as parameter (two opposite points), because it can compute the other two out of 4 points.
