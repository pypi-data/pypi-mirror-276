import math
from collections import Counter

class Calculator:
    """Calculator class object whose methods do addition, subtraction, multiplication, division,
    takes n root of a number and resets the stored memory to the initial value.
    """
    def __init__(self, number=0):
        """Accepts a number as initial value and if none is specified, default is 0.
        Checks if the number is int or float type and if not raises and error.
        Also converts it into a float type.
        """
        if isinstance(number, (int, float)):
            self.starting_number = float(number)
            self.result = float(number)
        else:
            raise ValueError('Value has to be a real number')

    def reset(self):
        """Resets the calculator memory to the initial value."""
        self.result = self.starting_number
        return self.result

    def add(self, number_to_add):
        """Checks if the given value is a real number.
        Adds it to the current number in calculator memory.
        """
        if isinstance(number_to_add, (int, float)):
            self.result += number_to_add
            return self.result
        else:
            raise ValueError('Value has to be a real number')

    def subtract(self, number_to_subtract):
        """Checks if the given value is a real number.
        Subtracts it from the current number in calculator memory
        """
        if isinstance(number_to_subtract, (int, float)):
            self.result -= number_to_subtract
            return self.result
        else:
            raise ValueError('Value has to be a real number')

    def multiply(self, number_to_multiply):
        """Checks if the given value is a real number.
        Multiplies the current number in calculator memory by that number.
        """
        if isinstance(number_to_multiply, (int, float)):
            self.result *= number_to_multiply
            return self.result
        else:
            raise ValueError('Value has to be a real number')

    def divide(self, number_to_divide_by):
        """Checks if the given value is a real number, after that checks if the value is 0,
        because division by zero is undifined.
        Current number in calculator memory is divided by that number.
        """
        if isinstance(number_to_divide_by, (int, float)):
            if number_to_divide_by == 0:
                raise ZeroDivisionError('Error. Can not divide by 0.')
            self.result /= number_to_divide_by
            return self.result
        else:
            raise ValueError('Value has to be a real number')

    def root(self, n_root_of_a_number):
        """Checks if the current number in memory is <0 and if the n root number is even.
        If that is the case raises an error.
        Also checks if the n root number isn't a 0 because division by zero is undefined.
        Takes n root of a current number in calculator memory.
        """
        if isinstance(n_root_of_a_number, (int, float)):
            if self.result < 0:
                raise ValueError('Can not take root out of negative numbers.')
            elif n_root_of_a_number == 0:
                raise ZeroDivisionError('Error. Can not divide by 0.')
            else:
                self.result = self.result ** (1 / n_root_of_a_number)
                return self.result
        else:
            raise ValueError('Value has to be a real number')

class ScientificCalculator(Calculator):
    """ScientificCalculator class object that inherits from the Calculator class object.
    It has additional methods for trigonometric functions, logarithms, power, and square
    root.
    """
    def sine(self):
        """Takes the sine of the current number in calculator memory."""
        self.result = math.sin(math.radians(self.result))
        return self.result

    def cosine(self):
        """Takes the cosine of the current number in calculator memory."""
        self.result = math.cos(math.radians(self.result))
        return self.result

    def tangent(self):
        """Takes the tangent of the current number in calculator memory."""
        self.result = math.tan(math.radians(self.result))
        return self.result

    def log(self, base=10):
        """Takes the logarithm of the current number in calculator memory.
        Checks if the current number is <=0 because logarithm is undefined for non-positive values.
        """
        if self.result <= 0:
            raise ValueError('Logarithm undefined for non-positive values.')
        self.result = math.log(self.result, base)
        return self.result

    def ln(self):
        """Takes the natural logarithm of the current number in calculator memory.
        Checks if the current number is <=0 because logarithm is undefined for non-positive values.
        """
        if self.result <= 0:
            raise ValueError('Logarithm undefined for non-positive values.')
        self.result = math.log(self.result)
        return self.result

    def power(self, exponent):
        """Raises the current number in calculator memory to the power of the given exponent."""
        if isinstance(exponent, (int, float)):
            self.result = self.result ** exponent
            return self.result
        else:
            raise ValueError('Exponent must be a real number')


class StatisticsCalculator(Calculator):
    """StatisticsCalculator class object that inherits from the Calculator class object.
    It has additional methods for calculating mean, median, mode, standard deviation,
    and variance of a list of numbers.
    """
    def __init__(self, numbers):
        """Accepts a list of numbers.
        Checks if all elements are real numbers and if not raises an error.
        """
        if all(isinstance(n, (int, float)) for n in numbers):
            self.numbers = numbers
        else:
            raise ValueError('All elements must be real numbers')

    def mean(self):
        """Calculates the mean of the list of numbers."""
        return sum(self.numbers) / len(self.numbers)

    def median(self):
        """Calculates the median of the list of numbers."""
        sorted_numbers = sorted(self.numbers)
        n = len(sorted_numbers)
        midpoint = n // 2

        if n % 2 == 1:
            return sorted_numbers[midpoint]
        else:
            return (sorted_numbers[midpoint - 1] + sorted_numbers[midpoint]) / 2

    def mode(self):
        """Calculates the mode of the list of numbers."""
        frequency = Counter(self.numbers)
        mode_data = frequency.most_common()
        max_count = mode_data[0][1]
        modes = [num for num, count in mode_data if count == max_count]
        if len(modes) == len(self.numbers):
            return None  # No mode found
        return modes

    def standard_deviation(self):
        """Calculates the standard deviation of the list of numbers."""
        mean = self.mean()
        variance = sum((x - mean) ** 2 for x in self.numbers) / len(self.numbers)
        return math.sqrt(variance)

    def variance(self):
        """Calculates the variance of the list of numbers."""
        mean = self.mean()
        return sum((x - mean) ** 2 for x in self.numbers) / len(self.numbers)
