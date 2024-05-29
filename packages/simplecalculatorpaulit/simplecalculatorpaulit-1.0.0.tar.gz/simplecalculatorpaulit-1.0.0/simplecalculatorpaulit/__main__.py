"""Main module"""
from simplecalculatorpaulit import Calculator, ScientificCalculator,StatisticsCalculator

if __name__ == '__main__':
    calculator = Calculator()
    print(calculator.add(5))
    print(calculator.subtract(3))
    print(calculator.multiply(2))
    print(calculator.divide(3))
    print(calculator.root(2))
    print(calculator.reset())

