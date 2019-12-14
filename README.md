# eval_expr

This scripts takes a mathematical expression as a parameter and evaluates it.  
The results are close to that of python's `eval()` function.  

As with `eval()` division by zero is not checked for:  
The truediv function will throw a ZeroDivisionError.  


Notable differences:  
    Stacking `+` or `-` operators results in an `Illegal stacking of operators` error.  


Usage: ./eval_expr [expression]  
    -r, --recursive  solve the expression recursively  

```shell
./eval_expr "3+2"
    5
./eval_expr "3--2"
    5
./eval_expr "3+(2-4)*3"
    -3
./eval_expr "1+(((3+2)*2))"
    11
./eval_expr "1234*(56-2)"
    66636
```
