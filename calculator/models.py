from django.db import models
import matplotlib.pyplot as plt
import io
from PIL import Image
import base64

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

