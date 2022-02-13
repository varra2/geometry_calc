import matplotlib.pyplot as plt
import io
from PIL import Image
import base64

class Figure:
    input = dict()
    output = dict()
    metrics = set()


    def __init__(self):
        title = None
        sides = []

    @classmethod
    def get_types(cls):
        #return (('Квадрат','square'),('Круг','circle'),('Прямоугольник','rectangle'),('Треугольник','triangle'),('Трапеция','trapezoid'),('Ромб','rhomb'),('Сфера','sphere'),('Параллелепипед','paralellepiped'),('Цилиндр','cylinder'),('Конус','cone'))
        return [(shape.title, shape) for shape in cls.__subclasses__()]

    def calculate(self):
        if ('Периметр', 'perimeter') in self.metrics:
            self.perimeter()
        if ('Площадь', 'square') in self.metrics:
            self.square()

    def perimeter(self):
        self.output[('Периметр', 'perimeter')] = sum(self.sides)

    def square(self):
        pass

class Square(Figure):
    title = 'Квадрат'

    def __init__(self, a):
        super().__init__()
        #self.title = 'Квадрат'
        self.input[('Сторона', 'side')] = a
        self.sides = [a]*4
        #self.output[('Периметр', 'perimeter')] = a*4
        #self.output[('Площадь', 'square')] = a ** 2
        super().calculate()

    def square(self):
        self.output[('Площадь', 'square')] = self.input[('Сторона', 'side')] ** 2

    def plot(self):
        a = self.input[('Сторона', 'side')]
        fig = plt.figure()
        ax = plt.subplot(111)
        ax.set_aspect('equal')
        ax.plot([0,a,a,0,0],[0,0,a,a,0])
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        thumb_data = base64.b64encode(buf.read()).decode('utf-8') 
        print(thumb_data)
        buf.close()
        #plt.savefig('example.png')

class Nriangle(Figure):
    title = 'Треугольник'
    def __init__(self, a):
        super().__init__()
        #self.title = 'Квадрат'
        self.input[('Сторона', 'side')] = a
        self.output[('Периметр', 'perimeter')] = a*4
        self.output[('Площадь', 'square')] = a ** 2

    def plot(self):
        a = self.input[('Сторона', 'side')]
        fig = plt.figure()
        ax = plt.subplot(111)
        ax.set_aspect('equal')
        ax.plot([0,a,a,0,0],[0,0,a,a,0])
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        thumb_data = base64.b64encode(buf.read()).decode('utf-8') 
        print(thumb_data)
        buf.close()
        #plt.savefig('example.png')


myfig = Square(10)
myfig.plot()