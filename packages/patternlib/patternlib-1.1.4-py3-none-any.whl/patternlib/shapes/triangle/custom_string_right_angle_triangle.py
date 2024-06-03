from patternlib.constants.patternlib_constants import STD_STRING1

MINROW = 2

def custom_string_right_angle_triangle(input_string=STD_STRING1):
    '''
    P
    P Y
    P Y T
    P Y T H
    P Y T H O
    P Y T H O N

    To view pattern run: 'print(custom_string_right_angle_triangle.__doc__)'
    '''
    if len(input_string) < MINROW:
        print("Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
    else:
        index_count = 0
        while index_count < len(input_string):
            print(" ".join(char.upper() for char in input_string[0: index_count + 1]))
            index_count += 1