def are_two_numbers_equal(a, b):
  try:
    c = 1 / (a - b)
  except ArithmeticError as e:
    return True

  return False


is_equal = are_two_numbers_equal(1, 1)
print(is_equal)
