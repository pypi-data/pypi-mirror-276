# Patternlib
**Patternlib** is a python library of visual patterns such as hour glass, triangles, pyramids, alphabets and many more. It is a simple to use library to help understand some basic concepts of looping and conditional statements.

## References
1. [PyPI patternlib](https://pypi.org/project/patternlib/)
2. [Docker image](https://hub.docker.com/layers/gautamkhanapuri/patternlib/1.1.2/images/sha256-2da774cdca4cdcce5938248a39a355d6617d9b7322db890485c8f2927223cf04?context=repo)

## Installation Process
```console
$ cd /tmp
$ python3 -m venv patternenv
$ source patternenv/bin/activate
(patternenv)$ pip list
(patternenv)$ pip install -U pip
(patternenv)$ pip install patternlib
```

## Shell run (REPL)
```python
>>> import patternlib
>>> patternlib.e_pattern(9)
* * * * * 
*
*
*
* * * * * 
*
*
*
* * * * * 
>>> patternlib.sigma(5)
* * * * * 
 *        
  *       
   *      
    *     
   *      
  *       
 *        
* * * * * 
>>> patternlib.number_increasing_along_column_right_angle_triangle(5, 55)
 55 
 56  60 
 57  61  64 
 58  62  65  67 
 59  63  66  68  69
```

## Console run
```console
$ python3 eg.py
a_pattern
custom_string_right_angle_triangle
decreasing_number_pyramid_pointing_down
decreasing_number_pyramid_pointing_up
decreasing_number_triangle
e_pattern
f_pattern
h_pattern
...
...
...
v_pattern
wide_diamond
wide_string_diamond
wide_string_isosceles_triangle_pointing_up
x_pattern
z_pattern
$
$ python3 eg.py --help
usage: eg.py [-h] [-l] [-s SHOW] [-r RUN] [-p PARAM]

Helps to understand the working of patternlib

optional arguments:
  -h, --help            show this help message and exit
  -l, --list            Prints the entire list of patterns available in patternlib
  -s SHOW, --show SHOW  Displays the details of the pattern you have passed as argument
  -r RUN, --run RUN     Runs the argument you have passed with default parameters.
  -p PARAM, --param PARAM
$
$ python3 eg.py -s triangle_pointing_right

    *
    * *
    * * *
    * * * *
    * * * * *
    * * * *
    * * *
    * *
    *

    This generates a triangle pointing to the right with the fill character *

    To view pattern run: 'print(triangle_pointing_right.__doc__)'
    
**************************************************
The parameters that can be passed to the function are:
(row=5)
$
$ python3 eg.py --run z_pattern -p 3
* * * 
   *  
  *   
 *    
* * * 
**************************************************
```

## Docker run
```console
$ docker run --rm --name pattern gautamkhanapuri/patternlib:1.1.4 --show hour_glass

    *********
     *******
      *****
       ***
        *
       ***
      *****
     *******
    *********

    This generates an hour glass.

    To view pattern run: 'print(hour_glass.__doc__)'
    
**************************************************
The parameters that can be passed to the function are:
(row=5)
```
To run interactively:
```console
$ docker run --rm --name pattern -it --entrypoint /bin/bash gautamkhanapuri/patternlib:1.1.4
root@b940637a0407:/# 
```
At the prompt of #, run:
```console
root@b940637a0407:/# python /root/eg.py --run narrow_string_isosceles_triangle_pointing_up --param PATTERNLIB
         P          
        PAP         
       PATAP        
      PATTTAP       
     PATTETTAP      
    PATTERETTAP     
   PATTERNRETTAP    
  PATTERNLNRETTAP   
 PATTERNLILNRETTAP  
PATTERNLIBILNRETTAP 
**************************************************
```

