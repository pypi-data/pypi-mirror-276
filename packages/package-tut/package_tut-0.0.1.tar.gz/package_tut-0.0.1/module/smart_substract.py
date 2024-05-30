def smart_subtract(a: int, b: int) -> int:
    """
      Subtracts the lesser of two integers from the greater.

      Parameters:
      a (int): First integer.
      b (int): Second integer.

      Returns:
      int: The result of the subtraction of the lesser integer from the greater integer.
      """
    if a > b:
        return a - b
    else:
        return b - a
