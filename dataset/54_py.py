import sys


class Test:

  def func(self, data: float):
    if abs(data) < 1e-9:
      print("Error: Division by zero", file=sys.stderr)
      return

    raw_result = 100.0 / data

    if raw_result > 2147483647 or raw_result < -2147483648:
      print("Error: Result exceeds integer range", file=sys.stderr)
      return

    result = int(raw_result)
    print(f"result: {result}")