# eval_expr
  
Usage: ./eval_expr [expression]  

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
