from patternlib.constants.patternlib_constants import ROWS5

MINROW = 3

def l_pattern(row=ROWS5):
  '''
  *
  *
  *
  *
  * * *

  This generates L - Pattern.

  To view pattern run: 'print(l_pattern.__doc__)'
  '''
  if row < MINROW:
    print("L-Pattern generation failed, number of rows has to be greater than 1...")
  else:
    for i in range(1, row+1):
      print("* " * (i//2+1)) if i==row else print('*')
