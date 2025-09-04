## Object oriented program to calculate the area of various shapes
## import modules
import math

## Define classes
class Shape:
    def __init__(self):
        pass
        
class Rectangle(Shape):
    def __init__(self, length, width):
        super().__init__()
        self.length = length
        self.width = width
        
    def getArea(self):
        return self.length * self.width
    
class Circle(Shape):
    def __init__(self, radius):
        super().__init__()
        self.radius = radius
        
    def getArea(self):

        return math.pi * (self.radius ** 2) 
    
class Triangle(Shape):
    def __init__(self, base, height):
        super().__init__()
        self.base = base
        self.height = height
        
    def getArea(self):
        return 0.5 * self.base * self.height    
    

## read text file
inFile = open(r"C:\A&M\GEOG676\Dickinson-online-GEOG776-fall2025\Lab3\shape.txt", "r")
lines = inFile.readlines()
inFile.close()

for line in lines:
    components = line.split(',')
    shapeName = components[0]
    if shapeName == "Rectangle":
        rect = Rectangle(int(components[1]), int(components[2]))
        print(f"The area of the rectangle with length {rect.length} and width {rect.width} is {rect.getArea():.2f}")
    elif shapeName == "Circle":
        circ = Circle(int(components[1]))
        print(f"The area of the circle with radius {circ.radius} is {circ.getArea():.2f}")
    elif shapeName == "Triangle":
        triang = Triangle(int(components[1]), int(components[2]))
        print(f"The area of the triangle with base {triang.base} and height {triang.height} is {triang.getArea():.2f}")
    else:
        print(f"Unknown shape: {shapeName}")

