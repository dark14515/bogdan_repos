class Parallelepiped:

    def __init__(self, length=1.0, width=1.0, height=1.0):
        self.__length = length
        self.__width = width
        self.__height = height

    @property
    def length(self):
        return self.__length

    @length.setter
    def length(self, value):
        if value <= 0:
            raise ValueError("Длина должна быть положительной")
        self.__length = value

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, value):
        if value <= 0:
            raise ValueError("Ширина должна быть положительной")
        self.__width = value

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, value):
        if value <= 0:
            raise ValueError("Высота должна быть положительной")
        self.__height = value

    def read(self):
        try:
            self.length = float(input("Введите длину: "))
            self.width = float(input("Введите ширину: "))
            self.height = float(input("Введите высоту: "))
        except ValueError as e:
            print(f"Ошибка: {e}")

    def display(self):
        print(f"Длина:  {self.length}")
        print(f"Ширина: {self.width}")
        print(f"Высота: {self.height}")

    def volume(self):
        return self.__length * self.__width * self.__height

    def surface_area(self):
        a, b, h = self.__length, self.__width, self.__height
        return 2 * (a * b + a * h + b * h)

if __name__ == "__main__":
    box = Parallelepiped()
    box.read()
    box.display()
    print(f"Объём:              {box.volume():.2f}")
    print(f"Площадь поверхности: {box.surface_area():.2f}")