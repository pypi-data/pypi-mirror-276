from patternlib.constants.patternlib_constants import ROWS5

MINROW = 3

def h_pattern(row=ROWS5):
  '''
  *   *
  *   *
  * * *
  *   *
  *   *

  This generates H - Pattern.

  To view pattern run: 'print(h_pattern.__doc__)'
  '''
  if row < MINROW:
    print("H-Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
  else:
    for i in range(1, row + 1):
      print("* " * (row // 2 + 1)) if i in [row // 2 + 1] else print('* ' + '  ' * (row // 2 - 1) + '* ')

