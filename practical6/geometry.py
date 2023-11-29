from abc import *
class GeometricObject(ABC):
    def __init__(self):
        self.__lineColor = 'black'
        self.__lineWidth = 1
        self.__visible = False
        self.__myCanvas = None

    def setColor(self, color):  #modified to redraw visible shapes
        self.__lineColor = color
        if self.__visible:
            self.__myCanvas.drawAll()

    def setWidth(self, width):  #modified to redraw visible shapes
        self.__lineWidth = width
        if self.__visible:
            self.__myCanvas.drawAll()

    def getColor(self):
        return self.__lineColor

    def getWidth(self):
        return self.__lineWidth

    @abstractmethod
    def _draw(self):
        pass

    def setVisible(self, vFlag):
        self.__visible = vFlag

    def getVisible(self):
        return self.__visible

    def setCanvas(self, theCanvas):
        self.__myCanvas = theCanvas

    def getCanvas(self):
        return self.__myCanvas
    
class Point(GeometricObject):
    def __init__(self, x, y):
        super().__init__()
        self.__coord = (x, y)

    def getCoord(self):
        return self.__coord

    def getX(self):
        return self.__coord[0]

    def getY(self):
        return self.__coord[1]

    def _draw(self, turtle):
        turtle.goto(self.__coord[0], self.__coord[1])
       # turtle.dot(self.__lineWidth, self.__lineColor)
        turtle.dot(self.getWidth(), self.getColor())

class Line(GeometricObject):
    def __init__(self, p1, p2):
        super().__init__()
        self.__p1 = p1
        self.__p2 = p2

    def getP1(self):
        return self.__p1

    def getP2(self):
        return self.__p2

    def _draw(self, turtle):
        turtle.color(self.getColor())
        turtle.width(self.getWidth())
        turtle.up()
        turtle.goto(self.__p1.getCoord())
        turtle.down()
        turtle.goto(self.__p2.getCoord())

class Polygon(GeometricObject):
    def __init__(self, points):
        super().__init__()
        self.__points = points
        self.__doFill = False

    def fill(self):
        self.__doFill = True
    
    def _draw(self, turtle):
        turtle.color(self.getColor())
        turtle.width(self.getWidth())
        if self.__doFill: turtle.begin_fill()

        #goto starting point
        turtle.up()
        turtle.goto(self.__points[0].getCoord())
        
        #draw to all points
        turtle.down()
        for i in range(1, len(self.__points)):
            turtle.goto(self.__points[i].getCoord())

        #go back to staring point
        turtle.goto(self.__points[0].getCoord())
        if self.__doFill: turtle.end_fill()

class Triangle(Polygon):
    def __init__(self, p1, p2, p3):
        super().__init__([p1, p2, p3])

class Square(Polygon):
    def __init__(self, p1, p2):
        p3 = Point(p2.getX(), p1.getY())
        p4 = Point(p1.getX(), p2.getY())
        super().__init__([p1, p3, p2, p4])