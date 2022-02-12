import matplotlib.pyplot as plt
import io
from PIL import Image
import base64

class Figure:
    input = dict()
    output = dict()

    def __init__(self):
        title = None

class Square(Figure):
    title = 'Квадрат'
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


#myfig = Square(10)
#myfig.plot()

print([(cls.title, cls) for cls in Figure.__subclasses__()])