from patternlib.constants.patternlib_constants import STD_STRING1

MINROW = 2

def string_right_angle_triangle(string=STD_STRING1):
    '''
    P
    P Y
    P Y T
    P Y T H
    P Y T H O
    P Y T H O N

    To view pattern run: 'print(string_right_angle_triangle.__doc__)'
    '''
    if len(string) < MINROW:
        print("Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
    else:
        l = list(string)
        for i in range(len(l)):
            res = ''
            for x in range(i + 1):
                res += l[x].rjust(2)
            print(res.ljust(2 * len(string)))