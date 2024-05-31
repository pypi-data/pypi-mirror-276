# tanjiro/maths.py

def add(*numbers):
    """
    Add multiple numbers together.

    Parameters:
    numbers (int or float): A variable number of numeric arguments to add.

    Returns:
    int or float: The sum of all provided numbers.

    Usage:
    ------
    from tanjiro import maths
    result = maths.add(22, 3893, 45, 10)
    print(result)  # Output: 3970
    """
    return sum(numbers)
