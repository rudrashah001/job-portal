import sys
import traceback

print("Checking module-level execution errors...\n")

files = [
    'app/routes/jobs.py',
    'app/routes/students.py',
    'app/routes/recruiters.py',
    'app/routes/admin.py',
]

for fpath in files:
    print(f"Testing {fpath}:")
    try:
        with open(fpath, 'r') as f:
            code_text = f.read()
        
        # Try to compile
        compile(code_text, fpath, 'exec')
        print(f"  Syntax: OK")
        
        # Try to exec (this should fail if there are import errors in the module)
        namespace = {}
        exec(code_text, namespace)
        
        if 'router' in namespace:
            print(f"  Execution: OK, router defined")
        else:
            print(f"  Execution: OK, but NO router defined")
            print(f"  Top-level names: {[k for k in namespace.keys() if not k.startswith('_')]}")
            
    except SyntaxError as e:
        print(f"  SYNTAX ERROR: {e}")
    except Exception as e:
        print(f"  EXEC ERROR: {type(e).__name__}: {e}")
    print()
