# SimpleCalculatorPauLit

SimpleCalculatorPauLit is a Python-based calculator module designed to perform a variety of arithmetic, scientific, and statistical calculations. This module is designed to be simple to use and integrate into larger projects, providing robust and reusable functions for a wide range of mathematical operations.

Project was created for Component Based Software Engineering module in Kaunas University of Technology.

## Features

- Basic Arithmetic Operations: Addition, subtraction multiplication, and division.
- Scientific Functions: Sine, cosine, tangent, logarithm (base 10), natural logarithm, and power functions.
- Statistical Functions: Mean, median, mode, standard deviation, and variance.
- Error Handling: Proper error handling for invalid operations such as division by zero or invalid inputs.

## Installation

You can install SimpleCalculatorPauLit using pip:

```sh
pip install simplecalculatorpaulit
```

## Usage

### Basic Usage

#### Calculator class

```python
>>> from simplecalculatorpaulit import Calculator

# Initialize the calculator with a starting number (default is 0)
>>> calc = Calculator(5)

# Perform basic arithmetic operations
>>> print(calc.add(10))        # Output: 15.0
>>> print(calc.subtract(3))    # Output: 12.0
>>> print(calc.multiply(2))    # Output: 24.0
>>> print(calc.divide(4))      # Output: 6.0
>>> print(calc.root(2))        # Output: 2.449489742783178
>>> print(calc.reset())        # Output: 5.0
```

### Scientific Usage

#### ScientificCalculator class

```python
>>> from simplecalculatorpaulit import ScientificCalculator

# Initialize the scientific calculator with a starting number (default is 0)
>>> sci_calc = ScientificCalculator(30)

# Perform scientific calculations
>>> print(sci_calc.sine())         # Output: 0.5 (approx)
>>> print(sci_calc.cosine())       # Output: 0.866 (approx)
>>> print(sci_calc.tangent())      # Output: 0.577 (approx)
>>> print(sci_calc.log())          # Output: 1.477 (approx)
>>> print(sci_calc.ln())           # Output: 3.401 (approx)
>>> print(sci_calc.power(3))       # Output: 27000.0
```

### Scientific Usage

#### ScientificCalculator class

```python
>>> from simplecalculatorpaulit import StatisticsCalculator

# Initialize the statistics calculator with a list of numbers
>>> stats_calc = StatisticsCalculator([1, 2, 2, 3, 4])

# Perform statistical calculations
>>> print(stats_calc.mean())                  # Output: 2.4
>>> print(stats_calc.median())                # Output: 2.0
>>> print(stats_calc.mode())                  # Output: [2]
>>> print(stats_calc.standard_deviation())    # Output: 1.019803902718557
>>> print(stats_calc.variance())              # Output: 1.04

```

## API Reference

### Calculator Class

- **init(self, number=0)**: Initializes the calculator with an optional starting number.
- **reset(self)**: Resets the calculator to the initial value.
- **add(self, number_to_add)**: Adds a number to the current memory.
- **subtract(self, number_to_subtract)**: Subtracts a number from the current memory.
- **multiply(self, number_to_multiply)**: Multiplies the current memory by a number.
- **divide(self, number_to_divide_by)**: Divides the current memory by a number.
- **root(self, n_root_of_a_number)**: Takes the n-th root of the current memory.

### ScientificCalculator Class (inherits from Calculator)

- **sine(self)**: Calculates the sine of the current memory value.
- **cosine(self)**: Calculates the cosine of the current memory value.
- **tangent(self)**: Calculates the tangent of the current memory value.
- **log(self, base=10)**: Calculates the logarithm of the current memory value to the specified base.
- **ln(self)**: Calculates the natural logarithm of the current memory value.
- **power(self, exponent)**: Raises the current memory value to the power of the given exponent.

### StatisticsCalculator Class (inherits from Calculator)

- **init(self, numbers)**: Initializes the calculator with a list of numbers for statistical calculations.
- **mean(self)**: Calculates the mean of the list of numbers.
- **median(self)**: Calculates the median of the list of numbers.
- **mode(self)**: Calculates the mode of the list of numbers.
- **standard_deviation(self)**: Calculates the standard deviation of the list of numbers.
- **variance(self)**: Calculates the variance of the list of numbers.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any bugs, features, or documentation improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](https://choosealicense.com/licenses/mit/) file for details.
