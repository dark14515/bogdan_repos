import math


class Circle:
    def __init__(self, first=0.0, second=0.0):
        self.__first = first
        self.__second = second

    @property
    def first(self):
        return self.__first

    @first.setter
    def first(self, value):
        if value <= 0:
            raise ValueError("Радиус должен быть положительным")
        self.__first = value

    @property
    def second(self):
        return self.__second

    @second.setter
    def second(self, value):
        self.__second = value

    def read(self):
        while True:
            try:
                self.first = float(input("Введите радиус круга: "))
                break
            except ValueError as e:
                print(f"Ошибка: {e}. Попробуйте снова.")

    def display(self):
        print(f"Радиус круга: {self.first}")

    def area(self):
        return math.pi * self.first ** 2

    def circumference(self):
        return 2 * math.pi * self.first


c = Circle()
c.read()
c.display()
print(f"Площадь круга: {c.area():.2f}")
print(f"Длина окружности: {c.circumference():.2f}")