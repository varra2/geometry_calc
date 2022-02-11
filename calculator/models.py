from django.db import models
import matplotlib.pyplot as plt
import io
from PIL import Image
import base64
import numpy as np

class Figure():
    input = dict()
    output = dict()

    def __init__(self):
        title = None

class Square(Figure):
    def __init__(self, a):
        super().__init__()
        self.title = 'Квадрат'
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
        buf.close()
        return thumb_data

class Rectangle(Figure):
        def __init__(self, a, b):
            super().__init__()
            self.title = 'Прямоугольник'
            self.input[('Сторона А', 'a_side')] = a
            self.input[('Сторона Б', 'b_side')] = b
            self.output[('Периметр', 'perimeter')] = (a + b)*2
            self.output[('Площадь', 'square')] = a*b

        def plot(self):
            a = self.input[('Сторона А', 'a_side')]
            b = self.input[('Сторона Б', 'b_side')]
            fig = plt.figure()
            ax = plt.subplot(111)
            ax.set_aspect('equal')
            ax.plot([0,b,b,0,0],[0,0,a,a,0])
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            thumb_data = base64.b64encode(buf.read()).decode('utf-8') 
            buf.close()
            return thumb_data

class Triangle(Figure):
        def __init__(self, a, b, c):
            super().__init__()
            self.title = 'Прямоугольник'
            self.input[('Сторона А', 'a_side')] = a
            self.input[('Сторона Б', 'b_side')] = b
            self.input[('Сторона В', 'c_side')] = c
            self.output[('Периметр', 'perimeter')] = a + b + c
            p = (a + b + c)/2
            h = 2/a * np.sqrt(p * (p - a) * (p - b) * (p - c))
            self.output[('Высота', 'hight')] = h
            self.output[('Площадь', 'square')] = a * h

        def plot(self):
            a = self.input[('Сторона А', 'a_side')]
            b = self.input[('Сторона Б', 'b_side')]
            c = self.input[('Сторона В', 'c_side')]
            h = self.output[('Высота', 'hight')]
            coords = ((0,0), (a,0), (np.sqrt(b**2-h**2), h), (0,0))
            ax = plt.subplot(111)
            ax.set_aspect('equal')
            ax.plot([coord[0] for coord in coords],[coord[1] for coord in coords])
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            thumb_data = base64.b64encode(buf.read()).decode('utf-8') 
            plt.clf()
            buf.close()
            return thumb_data