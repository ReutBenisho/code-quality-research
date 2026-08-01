def CalcUpperCalcLower(string):
    counter=[0,0]
    for x in range(len(string)):
      if string[x]>='a'<='z':
       counter[0]=counter[0]+1
      elif string[x]>='A'<='Z':
         counter[1]=counter[1]+ 1
    print('Number of Upper cases:'+str(counter[1]))
    print('Number of Lower cases:'+str(counter[0]))
