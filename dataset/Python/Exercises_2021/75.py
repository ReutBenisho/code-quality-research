def CheckArithmeticSeries(Number):
  num = [int(x) for x in str(Number)]# make a list from the number
  n=len(num)
  if n == 1:
   return True
  num.sort()# Sort list
  d = num[1] - num[0]
  for i in range(2,n):
    if num[i] - num[i - 1] != d:
      return False
  return True