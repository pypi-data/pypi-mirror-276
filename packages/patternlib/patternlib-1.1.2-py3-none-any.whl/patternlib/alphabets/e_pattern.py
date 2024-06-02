from patternlib.constants.patternlib_constants import ROWS5

MINROW = 3

def e_pattern(row=ROWS5):
  '''
  * * *
  *
  * * *
  *
  * * *

  This generates E - Pattern.

  To view pattern run: 'print(e_pattern.__doc__)'
  '''
  if row < MINROW:
    print("E-Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
  else:
    for i in range(1, row+1):
      print("* " * (row//2+1)) if i in [1,row, row//2+1] else print('*')


