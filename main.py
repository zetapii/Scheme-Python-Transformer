from transformer import parse_combined_racket_python
import sys

if __name__ == "__main__":
    
    input_script = sys.argv[1]
    
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_script.py>")
        sys.exit(1)

    # Run the parser/transformer on an input Python file
    # The Python file can have the 'racket_insert("<file_name>.rkt")' calls, <file_name>.rkt should have Scheme-Like code
    
    parse_combined_racket_python('input_script.py')