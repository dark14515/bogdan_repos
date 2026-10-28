class AverageCalculator:

    def get_average(self, *args):
        if not args:
            return None
        return sum(args) / len(args)

def main():
    calculator = AverageCalculator()
    numbers = []

    print("Введите числа (пустая строка - завершение):")

    while True:
        user_input = input("Число: ").strip()
        if user_input == "":
            break
        numbers.append(float(user_input))

    average = calculator.get_average(*numbers)

    if average is None:
        print("Вы не ввели ни одного числа.")
    else:
        print(f"Среднее значение: {average}")


if __name__ == "__main__":
    main()