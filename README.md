# Scheme-Python Transformer

## Overview

The **Scheme-Python Transformer** is a modular Python project designed to dynamically transform Python scripts containing `racket_insert` calls. These calls are placeholders that reference a Scheme-Like code. The transformer parses the Python code, replaces `racket_insert` calls with their corresponding Python Abstract Syntax Tree (AST) equivalents derived from the Scheme-Like code, and executes the transformed Python script seamlessly.

## Requirements

- **Python 3.8+**
- **Dependencies:**
  - `astunparse` (for converting AST back to Python code)
## Installation

1. **Clone the Repository**

   ```bash
    git clone https://github.com/zetapi/racket-python-transformer.git
    cd racket-python-transformer
    ```
2. **Activate Virtual Environment**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

3. **Install Dependencies**
   ```bash
   pip install astunparse
   ```

## Usage
Prepare Your Racket Code

- Ensure that you have a Racket script ready for insertion into your Python code. This script should contain functions or expressions that are meant to be evaluated within the Python environment.

### Example: Create a file named racket_insert.rkt :

```bash
(define (square x)
  (* x x))
```

Prepare Your Python Script with racket_insert Calls

Your Python script should contain racket_insert("<file_name>.rkt") calls at locations where you want to insert Racket code.

Example: Create file named input_script.py 

```bash
funcc = racket_insert("racket_insert.rkt")
scale_factor = 2  
shift_value = 3 

def transformed_quadratic(a, b, c, x):
    global funcc
    global shift_value
    return 100 * funcc(a, b, c, x) + shift_value

x_val = 4
result = transformed_quadratic(1, 2, 3, x_val)   
print(result)  
```

To run the transformer, use the following command:

```bash 
python main.py input_script.py
```
Replace input_script.py with the path to your Python script containing racket_insert calls.

The transformer will parse your Python script, substitute racket_insert calls with the corresponding Python representations of the Racket code, and execute the transformed script. You should see the output from your print statements in the console.

