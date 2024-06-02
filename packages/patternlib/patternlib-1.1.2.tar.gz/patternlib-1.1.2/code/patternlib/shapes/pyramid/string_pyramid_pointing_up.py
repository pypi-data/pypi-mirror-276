from patternlib.constants.patternlib_constants import ALPHABETS_STRING

MINROW = 2

def string_pyramid_pointing_up(string=ALPHABETS_STRING):
    '''
            A
          A   B
        A   B   C
      A   B   C   D
    A   B   C   D   E

    This generates a pyramid pointing up made up of characters in the input string.

    To view pattern run: 'print(string_pyramid_pointing_up.__doc__)'
    '''
    if len(string) < MINROW:
        print("Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
    else:
        l = list(string)
        for i in range(len(l)):
            res = ''
            for x in range(i + 1):
                res += l[x].rjust(4)
            print(res.center(4 * len(string)))