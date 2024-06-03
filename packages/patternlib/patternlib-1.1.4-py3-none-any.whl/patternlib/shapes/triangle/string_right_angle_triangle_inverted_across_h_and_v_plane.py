from patternlib.constants.patternlib_constants import STD_STRING1

MINROW = 2

def string_right_angle_triangle_inverted_across_h_and_v_plane(string=STD_STRING1):
    '''
     P Y T H O N
       P Y T H O
         P Y T H
           P Y T
             P Y
               P
    To view pattern run: 'print(string_right_angle_triangle_inverted_across_h_and_v_plane.__doc__)'
    '''
    if len(string) < MINROW:
        print("Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
    else:
        l = list(string)
        for i in range(len(l) - 1, -1, -1):
            res = ''
            for x in range(i + 1):
                res += l[x].rjust(2)
            print(res.rjust(2 * len(string)))