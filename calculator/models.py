# coding=utf-8

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
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
            self.get_perimeter()
        if ('Площадь', 'square') in self.metrics:
            self.get_square()
        if ('Высота', 'hight') in self.metrics:
            self.get_hight()
        if ('Сторона','side') in self.metrics:
            self.get_sides()
        if ('Объём','volume') in self.metrics:
            self.get_volume()

    def get_perimeter(self):
        self.output[('Периметр', 'perimeter')] = sum(self.sides)

    def get_square(self):
        pass

    def get_hight(self):
        pass

    def get_sides(self):
        pass

    def get_volume(self):
        pass

    @classmethod
    def get_types(cls):
        #return (('Квадрат','square'),('Круг','circle'),('Прямоугольник','rectangle'),('Треугольник','triangle'),('Трапеция','trapezoid'),('Ромб','rhomb'),('Сфера','sphere'),('Параллелепипед','paralellepiped'),('Цилиндр','cylinder'),('Конус','cone'))
        return [(shape.title, shape) for shape in cls.__subclasses__()]

class Flat(Figure):
    title = 'Плоские фигуры'
    coords = ((1,1),(1,1))

    @classmethod
    def get_types(cls):
        return super().get_types()

    def plot(sef, coords=coords):
        plt.figure()
        ax = plt.subplot(111)
        ax.set_aspect('equal')
        ax.plot([coord[0] for coord in coords],[coord[1] for coord in coords], color='teal')
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        thumb_data = base64.b64encode(buf.read()).decode('utf-8') 
        buf.close()
        return thumb_data

class Volumetric(Figure):
    title = 'Объёмные фигуры'
    coords = ((1,1,1),(1,1,1))

    @classmethod
    def get_types(cls):
        return super().get_types()

    def plot(sef, coords=coords):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        x,y,z = [coord[0] for coord in coords],[coord[1] for coord in coords], [coord[2] for coord in coords]
        ax.set_box_aspect((np.ptp(x), np.ptp(y), np.ptp(z)))
        ax.plot(x,y,z, color='teal')
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        thumb_data = base64.b64encode(buf.read()).decode('utf-8') 
        buf.close()
        return thumb_data

class Square(Flat):
    title = 'Квадрат'
    metrics = (('Периметр', 'perimeter'), ('Площадь', 'square'))

    def __init__(self, a=5):
        super().__init__()
        #self.coords = ((0,0),(a,0),(a,a),(0,a),(0,0))
        self.input[('Сторона', 'side')] = a
        self.sides = [a]*4
        self.calculate()
        self.coords = self.get_coords()

    def get_coords(self):
        a = self.input[('Сторона', 'side')]
        return ((0,0),(a,0),(a,a),(0,a),(0,0))

    def get_square(self):
        self.output[('Площадь', 'square')] = self.input[('Сторона', 'side')] ** 2

    def plot(self):
        return super().plot(self.coords)

class Rectangle(Flat):
        title = 'Прямоугольник'
        metrics = (('Периметр', 'perimeter'), ('Площадь', 'square'))
        
        def __init__(self, a=5, b=4):
            super().__init__()
            self.input = {('Сторона А', 'a_side'): a, ('Сторона Б', 'b_side'): b}
            self.coords = self.get_coords()
            self.sides = [a,b]*2
            self.calculate()

        def get_coords(self):
            a = self.input[('Сторона А', 'a_side')]
            b = self.input[('Сторона Б', 'b_side')]
            return ((0,0),(b,0),(b,a),(0,a),(0,0))

        def get_square(self):
            self.output[('Площадь', 'square')] = self.input[('Сторона А', 'a_side')] * self.input[('Сторона Б', 'b_side')]
    
        def plot(self):
            return super().plot(self.coords)

class Triangle(Flat):
        title = 'Треугольник'
        metrics = (('Периметр', 'perimeter'), ('Площадь', 'square'), ('Высота', 'hight'))

        def __init__(self, a=5, b=4, c=3):
            super().__init__()
            self.input = {('Сторона А', 'a_side'): a, ('Сторона Б', 'b_side'): b, ('Сторона В', 'c_side'): c}
            self.sides = [a,b,c]
            if not self.triangle_rule(a,b,c):
                self.calculate()
                self.coords = self.get_coords()
            else:
                self.output[('Ошибка','error')] = self.triangle_rule(a,b,c)
                self.coords = super().coords

        def get_hight(self):
            a,b,c = self.sides[:]
            p = (a + b + c)/2
            h = 2/a * np.sqrt(p * (p - a) * (p - b) * (p - c))
            self.output[('Высота', 'hight')] = h
            return h

        def get_square(self):            
            self.output[('Площадь', 'square')] = (self.sides[0] * self.get_hight())/2

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
        
class Trapezoid(Flat):
    title = 'Трапеция'
    metrics = (('Периметр', 'perimeter'), ('Площадь', 'square'), ('Сторона','side'))
    
    def __init__(self, a=5, b=4, c=3, h=3):
            super().__init__()
            self.input = {('Нижнее основание', 'low_base'): a, ('Боковая сторона', 'side'): b, ('Верхнее основание', 'high_base'): c, ('Высота', 'hight'): h}
            leg = np.sqrt(b**2 - h**2)
            check = self.check_edge(leg,h,b)
            if not check:
                d = np.sqrt((a - leg)**2 + h**2)
                self.sides = [a,b,c,d]
                self.calculate()
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

    def get_square(self):
        base1, base2, h = self.input[('Нижнее основание', 'low_base')], self.input[('Верхнее основание', 'high_base')], self.input[('Высота', 'hight')] 
        self.output[('Площадь', 'square')] = (base1 + base2)*h/2
        
    def get_sides(self):
        self.output[('Вторая боковая сторона','side')] = self.sides[-1]

    def plot(self):
            return super().plot(self.coords)

class Rhomb(Flat):
    title = 'Ромб'
    metrics = (('Периметр', 'perimeter'), ('Площадь', 'square'), ('Сторона','side'))

    def __init__(self, d1=5, d2=3):
            super().__init__()
            self.input = {('Большая диагональ', 'bg_diagonal'): max(d1, d2), ('Малая диагональ', 'sm_diagonal'): min(d1,d2)}
            self.sides = self.get_sides()
            self.calculate()
            self.coords = self.get_coords()

    def get_sides(self):
        d1, d2 = self.input.values()
        self.output[('Сторона','side')] = np.sqrt((d1/2)**2 + (d2/2)**2)
        return [np.sqrt((d1/2)**2 + (d2/2)**2)]*4

    def get_square(self):
        a,b,c = self.output[('Сторона','side')], self.input[('Большая диагональ', 'bg_diagonal')], self.input[('Малая диагональ', 'sm_diagonal')]
        triangle = Triangle(b/2,c/2,a)
        self.output[('Площадь', 'square')] = triangle.output[('Площадь', 'square')]*4

    def get_coords(self):
        d1, d2 = self.input.values()
        return ((0, d1/2), (d2/2, d1),(d2, d1/2), (d2/2,0), (0, d1/2))

    def plot(self):
            return super().plot(self.coords)

class Circle(Flat):
    title = 'Круг'
    metrics = (('Периметр', 'perimeter'), ('Площадь', 'square'))

    def __init__(self, r=5):
        super().__init__()
        self.input = {('Радиус','radius'): r}
        self.calculate()
        self.coords = self.get_coords()

    def get_perimeter(self):
        self.output[('Периметр', 'perimeter')] = 2 * self.input[('Радиус','radius')] * np.pi

    def get_square(self):
        self.output[('Площадь', 'square')] = np.pi * self.input[('Радиус','radius')]**2

    def get_coords(self):
        rd = self.input[('Радиус','radius')]
        x = np.linspace(0,rd*2,int(np.ceil(500*rd)))
        part1 = [(dot, (np.sqrt(rd**2-(dot-rd)**2) + rd)) for dot in x]
        part2 = [(dot, (-np.sqrt(rd**2-(dot-rd)**2) + rd)) for dot in x]
        return part1+part2[::-1]

    def plot(self):
        return super().plot(self.coords)

class Cube(Volumetric):
    title = 'Куб'
    metrics = (('Периметр', 'perimeter'), ('Площадь', 'square'), ('Объём','volume'))

    def __init__(self, a=5):
        super().__init__()
        self.input[('Сторона', 'side')] = a
        self.sides = [a]*12
        self.calculate()
        self.coords = self.get_coords()

    def get_coords(self):
        a = self.input[('Сторона', 'side')]
        return ((0,0,0),(a,0,0),(a,a,0),(0,a,0),(0,0,0), (0,0,a),(a,0,a),(a,0,0),(0,0,0), (0,0,a),(0,a,a),(0,a,0), (0,a,a),(a,a,a),(a,a,0), (a,a,a),(a,0,a) )

    def get_square(self):
        self.output[('Площадь', 'square')] = (self.input[('Сторона', 'side')] ** 2) * 6

    def get_volume(self):
        self.output[('Объём','volume')] = self.input[('Сторона', 'side')] ** 3

    def plot(self):
        return super().plot(self.coords)


class Parallelepiped(Volumetric):
    title = 'Параллелепипед'
    metrics = (('Периметр', 'perimeter'), ('Площадь', 'square'), ('Объём','volume'))

    def __init__(self, a=5, b=3, c=4):
        super().__init__()
        self.input = {('Ребро А', 'a_side'): a, ('Ребро Б', 'b_side'): b, ('Ребро В', 'c_side'): c}
        self.sides = [a,b,c]*4
        self.calculate()
        self.coords = self.get_coords()

    def get_coords(self):
        a,b,c = self.input.values()
        return ((0,0,0),(a,0,0),(a,b,0),(0,b,0),(0,0,0), (0,0,c),(a,0,c),(a,0,0),(0,0,0), (0,0,c),(0,b,c),(0,b,0), (0,b,c),(a,b,c),(a,b,0), (a,b,c),(a,0,c))

    def get_square(self):
        base_squares = (self.input[('Ребро А', 'a_side')] * self.input[('Ребро Б', 'b_side')]) * 2
        side_squares = (self.input[('Ребро А', 'a_side')] * self.input[('Ребро В', 'c_side')]) * 4
        self.output[('Площадь', 'square')] = base_squares + side_squares

    def get_volume(self):
        self.output[('Объём','volume')] = self.input[('Ребро А', 'a_side')] * self.input[('Ребро Б', 'b_side')] * self.input[('Ребро В', 'c_side')]

    def plot(self):
        return super().plot(self.coords)

class Pyramid(Volumetric):
    title = 'Пирамида (правильная)'
    metrics = (('Высота', 'hight'), ('Периметр', 'perimeter'), ('Площадь', 'square'), ('Объём','volume'))

    def __init__(self, c=4, l = 5, e=6):
        super().__init__()
        self.input = {('Число сторон основания', 'base_count'): c, ('Длина стороны основания', 'base_length'): l, ('Ребро', 'edge'): e}
        self.face = Triangle(l,e,e)
        try:
            self.calculate()
            self.coords = self.get_coords()
        except:
            self.coords = super().coords
            self.output = {('Ошибка','error'): 'Невозможно построить пирамиду с данным набором параметров. Пожалуста, попробуте ещё раз.'}

    def get_perimeter(self):
        count, length, edge = self.input.values()
        self.output[('Периметр основания', 'base_perimeter')] = count * length
        self.output[('Общий периметр', 'perimeter')] = count * (length + edge)

    def get_square(self):
        count, length= self.input[('Число сторон основания', 'base_count')], self.input[('Длина стороны основания', 'base_length')]
        base_square = (count * (length**2)) / (4 * np.tan(np.pi/count))
        face_square = self.face.output[('Площадь', 'square')]
        self.output[('Площадь основания', 'base_square')] = base_square
        self.output[('Общий периметр', 'perimeter')] = base_square + face_square*count

    def get_hight(self):
        count, length= self.input[('Число сторон основания', 'base_count')], self.input[('Длина стороны основания', 'base_length')]

        face_hight = self.face.output[('Высота', 'hight')]
        self.output[('Апофема', 'face_square')] = face_hight

        alpha = np.pi/count
        radius = (length/2) * np.arctan(alpha)
        pyr_hight = np.sqrt(face_hight**2 - radius**2)
        self.output[('Высота', 'hight')] = pyr_hight

    def get_volume(self):
        hight = self.output[('Высота', 'hight')]
        base = self.output[('Площадь основания', 'base_square')]
        self.output[('Объём','volume')] = (1/3)*base*hight


    def get_coords(self):
        count, length= self.input[('Число сторон основания', 'base_count')], self.input[('Длина стороны основания', 'base_length')]
        alpha = 2*np.pi/count
        radius = (length/2) * (1 / np.sin(alpha/2))
        hight = self.output[('Высота', 'hight')]
        coords = [(0,0,hight),(radius, 0, 0)]
        
        for vertex in range(count):
            coords += [(np.cos(alpha)*radius, np.sin(alpha)*radius, 0), (0,0, hight), (np.cos(alpha)*radius, np.sin(alpha)*radius, 0)]
            alpha += 2*np.pi/count

        return coords

    def plot(self):
        return super().plot(self.coords)

class Cone(Volumetric):
    title = 'Конус'
    metrics = (('Периметр', 'perimeter'), ('Площадь', 'square'), ('Объём','volume'))

    def __init__(self, h = 8, r = 4):
        super().__init__()
        self.input = {('Высота', 'hight'): h, ('Радиус','radius'): r }
        self.base = Circle(r)

        self.calculate()
        self.coords = self.get_coords()

    def get_perimeter(self):
        self.output[('Периметр основания', 'base_perimeter')] = self.base.output[('Периметр', 'perimeter')]

    def get_square(self):
        self.output[('Площадь основания', 'base_square')] = self.base.output[('Площадь', 'square')]

    def get_volume(self):
        base = self.output[('Площадь основания', 'base_square')]
        hight = self.input[('Высота', 'hight')]
        self.output[('Объём','volume')] = (1/3)*base*hight
    
    def get_coords(self):
        rd = self.input[('Радиус','radius')]
        h = self.input[('Высота', 'hight')]
        x = np.linspace(0,rd*2,int(np.ceil(500*rd)))
        part1 = [(dot, (np.sqrt(rd**2-(dot-rd)**2) + rd),0) for dot in x]
        part2 = [(dot, (-np.sqrt(rd**2-(dot-rd)**2) + rd),0) for dot in x]
        ccl = part1+part2[::-1]
        cone = []
        net = np.linspace(0,rd*2,rd*5)
        for dot in net:
            cone += [(rd,rd,h), (dot, (np.sqrt(rd**2-(dot-rd)**2) + rd),0), (rd,rd,h), (dot, (-np.sqrt(rd**2-(dot-rd)**2) + rd),0), (rd,rd,h)]
        return ccl+cone

    def plot(self):
        return super().plot(self.coords)

class Cylinder(Volumetric):
    title = 'Цилиндр'
    metrics = (('Периметр', 'perimeter'), ('Площадь', 'square'), ('Объём','volume'))

    def __init__(self, h=8, r=4):
        super().__init__()
        self.input = {('Высота', 'hight'): h, ('Радиус','radius'): r }
        self.base = Circle(r)

        self.calculate()
        self.coords = self.get_coords()

    def get_perimeter(self):
        self.output[('Периметр основания', 'base_perimeter')] = self.base.output[('Периметр', 'perimeter')]

    def get_square(self):
        self.output[('Площадь основания', 'base_square')] = self.base.output[('Площадь', 'square')]

    def get_volume(self):
        base = self.output[('Площадь основания', 'base_square')]
        hight = self.input[('Высота', 'hight')]
        self.output[('Объём','volume')] = base*hight

    def get_coords(self):
        rd = self.input[('Радиус','radius')]
        h = self.input[('Высота', 'hight')]
        x = np.linspace(0,rd*2,int(np.ceil(500*rd)))
        part1 = [(dot, (np.sqrt(rd**2-(dot-rd)**2) + rd),0) for dot in x]
        part2 = [(dot, (-np.sqrt(rd**2-(dot-rd)**2) + rd),0) for dot in x]
        ccl1 = part1+part2[::-1]
        part3 = [(dot, (np.sqrt(rd**2-(dot-rd)**2) + rd),h) for dot in x]
        part4 = [(dot, (-np.sqrt(rd**2-(dot-rd)**2) + rd),h) for dot in x]
        ccl2 = part3+part4[::-1]
        
        #net = np.linspace(0,rd*2,rd*5)
        side = []
        for i in range(len(x)*2-100):
            if i%100 == 0:
                side += [ccl1[i], ccl2[i]] + ccl2[i:i+100] + [ccl1[i+100]]

        return ccl1+ccl2+side

    def plot(self):
        return super().plot(self.coords)

class Sphere(Volumetric):
    title = 'Сфера'
    metrics = (('Периметр', 'perimeter'), ('Площадь', 'square'), ('Объём','volume'))

    def __init__(self, r=5):
        super().__init__()
        self.input = {('Радиус','radius'): r }
        self.sec = Circle(r)
        self.calculate()

    def get_perimeter(self):
        self.output[('Периметр сечения', 'sec_perimeter')] = self.sec.output[('Периметр', 'perimeter')]

    def get_square(self):
        self.output[('Площадь основания', 'base_square')] = self.sec.output[('Площадь', 'square')]

    def get_volume(self):
        return (4/3)*np.pi*(self.input[('Радиус','radius')]**3)

    def plot(self):

        rd = self.input[('Радиус','radius')]
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = rd * np.outer(np.cos(u), np.sin(v))
        y = rd * np.outer(np.sin(u), np.sin(v))
        z = rd * np.outer(np.ones(np.size(u)), np.cos(v))

        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        ax.set_box_aspect((np.ptp(x), np.ptp(y), np.ptp(z)))
        ax.plot_wireframe(x,y,z, color='teal')
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        thumb_data = base64.b64encode(buf.read()).decode('utf-8') 
        buf.close()
        return thumb_data