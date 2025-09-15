## Object oriented program to calculate the area of various shapes
## import modules
import math

## Define classes
## each child class will have its own method to calculate area

## parent class
class Shape:
    def __init__(self):
        pass

## rectangle class       
class Rectangle(Shape):
    def __init__(self, length, width):
        super().__init__()
        self.length = length
        self.width = width
        
    def getArea(self):
        return self.length * self.width

## circle class   
class Circle(Shape):
    def __init__(self, radius):
        super().__init__()
        self.radius = radius
        
    def getArea(self):

        return math.pi * (self.radius ** 2) 

## triangle class    
class Triangle(Shape):
    def __init__(self, base, height):
        super().__init__()
        self.base = base
        self.height = height
        
    def getArea(self):
        return 0.5 * self.base * self.height    
    

## read input text file
inFile = open(r"C:\A&M\GEOG676\Dickinson-online-GEOG776-fall2025\Lab3\shape.txt", "r")
lines = inFile.readlines()
inFile.close()

## process each line one at a time in the for loop
for line in lines:
    components = line.split(',')
    shapeName = components[0]
## when rectangle, calculate area with W x L
    if shapeName == "Rectangle":
        rect = Rectangle(int(components[1]), int(components[2]))
        print(f"The area of the rectangle with length {rect.length} and width {rect.width} is {rect.getArea():.2f}")
## when circle, calculate area with pi x r^2
    elif shapeName == "Circle":
        circ = Circle(int(components[1]))
        print(f"The area of the circle with radius {circ.radius} is {circ.getArea():.2f}")
## when triangle, calculate area with 0.5 x b x h
    elif shapeName == "Triangle":
        triang = Triangle(int(components[1]), int(components[2]))
        print(f"The area of the triangle with base {triang.base} and height {triang.height} is {triang.getArea():.2f}")
## if none of the three, print out message of unknown shape
    else:
        print(f"Unknown shape: {shapeName}")

