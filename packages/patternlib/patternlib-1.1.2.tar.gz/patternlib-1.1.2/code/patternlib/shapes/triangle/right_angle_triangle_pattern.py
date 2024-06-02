from patternlib.constants.patternlib_constants import ROWS5

MINROW = 2

def right_angle_triangle_pattern(row=ROWS5):
  '''
  *
  * *
  * * *
  * * * *
  * * * * *

  This generates right-angled-triangle-Pattern made up of *.

  To view pattern run: 'print(right_angle_triangle_pattern.__doc__)'
  '''
  if row < MINROW:
    print("right-angled-triangle-Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
  else:
    for i in range(1,row+1):
      print("* " * i)
