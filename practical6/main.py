import turtle
from geometry import *

class Canvas:
    def __init__(self, w, h):
        self.__visibleObjects = []   #list of shapes to draw
        self.__turtle = turtle.Turtle()
        self.__screen = turtle.Screen()
        self.__screen.setup(width = w, height = h)
        self.__turtle.hideturtle()

    def drawAll(self):
        self.__turtle.reset()
        self.__turtle.up()
        self.__screen.tracer(0)
        for shape in self.__visibleObjects: #draw all shapes in order
            shape._draw(self.__turtle)
        self.__screen.tracer(1)
        self.__turtle.hideturtle()

    def addShape(self, shape):
        self.__visibleObjects.append(shape)

    def draw(self, gObject):
        gObject.setCanvas(self)
        gObject.setVisible(True)
        self.__turtle.up()
        self.__screen.tracer(0)
        gObject._draw(self.__turtle)
        self.__screen.tracer(1)
        self.addShape(gObject)

    def exitOnClick(self):
        self.__screen.exitonclick()


def test2():
    myCanvas = Canvas(500, 500)
    # line1 = Line(Point(-100, -100), Point(100, 100))
    # line2 = Line(Point(-100, 100), Point(100, -100))
    # line1.setWidth(4)    
    # myCanvas.draw(line1)
    # myCanvas.draw(line2)
    # line1.setColor('red')
    # line2.setWidth(4)

    triangle = Triangle(Point(-100, -100), Point(0, -100), Point(0, 0))
    triangle.setColor("blue")
    triangle.setWidth(4)
    myCanvas.draw(triangle)

    square = Square(Point(50, 50), Point(150, 150))
    square.fill()
    myCanvas.draw(square)


    myCanvas.exitOnClick()


test2()

