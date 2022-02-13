from django.db import models
import matplotlib.pyplot as plt
import io
from PIL import Image
import base64
import numpy as np

class Figure():
    metrics = set()
    coords = ((1,1),(1,1))

    def __init__(self):
            self.input = dict()
            self.output = dict()
            self.sides = []
    
    def get_coords(self):
        pass

    def calculate(self):
        if ('Периметр', 'perimeter') in self.metrics:
            self.perimeter()
        if ('Площадь', 'square') in self.metrics:
            self.square()
        if ('Высота', 'hight') in self.metrics:
            self.hight()
        if ('Сторона','side') in self.metrics:
            self.get_sides()

    def perimeter(self):
        self.output[('Периметр', 'perimeter')] = sum(self.sides)

    def square(self):
        pass

    def hight(self):
        pass

    def get_sides(self):
        pass

    @classmethod
    def get_types(cls):
        #return (('Квадрат','square'),('Круг','circle'),('Прямоугольник','rectangle'),('Треугольник','triangle'),('Трапеция','trapezoid'),('Ромб','rhomb'),('Сфера','sphere'),('Параллелепипед','paralellepiped'),('Цилиндр','cylinder'),('Конус','cone'))
        return [(shape.title, shape) for shape in cls.__subclasses__()]

    def plot(sef, coords=coords):
            plt.figure()
            ax = plt.subplot(111)
            ax.set_aspect('equal')
            ax.plot([coord[0] for coord in coords],[coord[1] for coord in coords])
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            thumb_data = base64.b64encode(buf.read()).decode('utf-8') 
            buf.close()
            return thumb_data



class Square(Figure):
    title = 'Квадрат'
    metrics = (('Периметр', 'perimeter'), ('Площадь', 'square'))

    def __init__(self, a=5):
        super().__init__()
        #self.coords = ((0,0),(a,0),(a,a),(0,a),(0,0))
        self.input[('Сторона', 'side')] = a
        self.sides = [a]*4
        super().calculate()
        self.coords = self.get_coords()

    def get_coords(self):
        a = self.input[('Сторона', 'side')]
        return ((0,0),(a,0),(a,a),(0,a),(0,0))

    def square(self):
        self.output[('Площадь', 'square')] = self.input[('Сторона', 'side')] ** 2

    def plot(self):
        return super().plot(self.coords)

class Rectangle(Figure):
        title = 'Прямоугольник'
        metrics = (('Периметр', 'perimeter'), ('Площадь', 'square'))
        
        def __init__(self, a=5, b=4):
            super().__init__()
            self.input = {('Сторона А', 'a_side'): a, ('Сторона Б', 'b_side'): b}
            self.coords = self.get_coords()
            self.sides = [a,b]*2
            super().calculate()

        def get_coords(self):
            a = self.input[('Сторона А', 'a_side')]
            b = self.input[('Сторона Б', 'b_side')]
            return ((0,0),(b,0),(b,a),(0,a),(0,0))

        def square(self):
            self.output[('Площадь', 'square')] = self.input[('Сторона А', 'a_side')] * self.input[('Сторона Б', 'b_side')]
    
        def plot(self):
            return super().plot(self.coords)

class Triangle(Figure):
        title = 'Треугольник'
        metrics = (('Периметр', 'perimeter'), ('Площадь', 'square'), ('Высота', 'hight'))

        def __init__(self, a=5, b=4, c=3):
            super().__init__()
            self.input = {('Сторона А', 'a_side'): a, ('Сторона Б', 'b_side'): b, ('Сторона В', 'c_side'): c}
            self.sides = [a,b,c]
            if not self.triangle_rule(a,b,c):
                super().calculate()
                self.coords = self.get_coords()
            else:
                self.output[('Ошибка','error')] = self.triangle_rule(a,b,c)
                self.coords = super().coords

        def hight(self):
            a,b,c = self.sides[:]
            p = (a + b + c)/2
            h = 2/a * np.sqrt(p * (p - a) * (p - b) * (p - c))
            self.output[('Высота', 'hight')] = h
            return h

        def square(self):            
            self.output[('Площадь', 'square')] = (self.sides[0] * self.hight())/2

        def get_coords(self):
            a,b = self.sides[0], self.sides[1]
            h = self.output[('Высота', 'hight')]
            return ((0,0), (a,0), (np.sqrt(b**2-h**2), h), (0,0))

        @staticmethod
        def triangle_rule(a,b,c):
            sides = [a,b,c]
            for i in range(3):
                rest = sum(sides[:i]+sides[i+1:])
                if sides[i] >= rest:
                    line = f'введённые Вами стороны не проходят проверку на соотношение сторон: длина стороны {sides[i]} беольше либо равна сумме длин других сторон {rest}. Пожалуйста, попробуйте ещё раз с другими значениями.'
                    return line
            return False 

        def plot(self):
            return super().plot(self.coords)
        
class Trapezoid(Figure):
    title = 'Трапеция'
    metrics = (('Периметр', 'perimeter'), ('Площадь', 'square'))
    
    def __init__(self, a=5, b=4, c=3, h=3):
            super().__init__()
            self.input = {('Нижнее основание', 'low_base'): a, ('Боковая сторона', 'side'): b, ('Верхнее основание', 'high_base'): c, ('Высота', 'hight'): h}
            leg = np.sqrt(b**2 - h**2)
            check = self.check_edge(leg,h,b)
            if not check:
                d = np.sqrt((a - leg)**2 + h**2)
                self.sides = [a,b,c,d]
                super().calculate()
                self.coords = self.get_coords()
            else:
                self.coords = super().coords
                self.output[('Ошибка','error')] = check

    @staticmethod
    def check_edge(leg, hight, side):
        if hight > side:
            return 'длина высоты не может превышать длину боковой стороны. Пожалуйста, попробуйте ещё раз с другими входными данными.'
        else:
            return Triangle.triangle_rule(leg,hight,side)

    def get_coords(self):
        a,b,c = self.sides[:3]
        h = self.input[('Высота', 'hight')]
        return ((0,0), (np.sqrt(b**2 - h**2), h), (c + np.sqrt(b**2 - h**2), h), (a,0), (0,0))

    def square(self):
        base1, base2, h = self.input[('Нижнее основание', 'low_base')], self.input[('Верхнее основание', 'high_base')], self.input[('Высота', 'hight')] 
        self.output[('Площадь', 'square')] = (base1 + base2)*h/2
        
    def plot(self):
            return super().plot(self.coords)

class Rhomb(Figure):
    title = 'Ромб'
    metrics = (('Периметр', 'perimeter'), ('Площадь', 'square'), ('Сторона','side'))

    def __init__(self, d1=5, d2=3):
            super().__init__()
            self.input = {('Большая диагональ', 'bg_diagonal'): max(d1, d2), ('Малая диагональ', 'sm_diagonal'): min(d1,d2)}
            self.sides = self.get_sides()
            super().calculate()
            self.coords = self.get_coords()

    def get_sides(self):
        d1, d2 = self.input.values()
        self.output[('Сторона','side')] = np.sqrt((d1/2)**2 + (d2/2)**2)
        return [np.sqrt((d1/2)**2 + (d2/2)**2)]*4

    def square(self):
        a,b,c = self.output[('Сторона','side')], self.input[('Большая диагональ', 'bg_diagonal')], self.input[('Малая диагональ', 'sm_diagonal')]
        triangle = Triangle(b/2,c/2,a)
        self.output[('Площадь', 'square')] = triangle.output[('Площадь', 'square')]*4

    def get_coords(self):
        d1, d2 = self.input.values()
        return ((0, d1/2), (d2/2, d1),(d2, d1/2), (d2/2,0), (0, d1/2))

    def plot(self):
            return super().plot(self.coords)
