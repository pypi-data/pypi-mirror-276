from patternlib.constants.patternlib_constants import ALPHABETS_STRING

MINROW = 2

def wide_string_diamond(string=ALPHABETS_STRING):
    '''
            A
          A B A
        A B C B A
      A B C D C B A
    A B C D E D C B A
      A B C D C B A
        A B C B A
          A B A
            A

    This generates a wide diamond made of alphabets.

    To view pattern run: 'print(wide_string_diamond.__doc__)'
    '''
    if len(string) < MINROW:
        print("Pattern generation failed, number of rows has to be greater than %d..." % MINROW)
    else:
        newstring = (' '.join(list(string)))
        for i in range(0, 2 * len(string), 2):
            a = newstring[0: i + 2]
            b = newstring[i - (len(newstring) + 2):: -1] if i < (2 * len(string) - 2) else newstring[i - (
                        len(newstring) + 1):: -1]
            print((a + b).center(2 * len(newstring)))
        for i in range(len(newstring) - 2, -1, -2):
            print((newstring[0: i + 1] + newstring[i - (len(newstring) + 3):: -1]).center(2 * len(newstring)))

