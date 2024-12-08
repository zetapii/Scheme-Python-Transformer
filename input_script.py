funcc = racket_insert("racket_insert.rkt")
scale_factor = 2  
shift_value = 3 

def transformed_quadratic(a, b, c, x):
    global funcc
    global shift_value
    return 100 * funcc(a, b, c, x) + shift_value

x_val = 4
result = transformed_quadratic(1, 2, 3, x_val)   
print(f"computed result is {result}")  
