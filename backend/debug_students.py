import traceback
import sys

print("Testing students router import...")
try:
    import app.routes.students as students_module
    print(f"  Module imported: {students_module}")
    print(f"  Module file: {students_module.__file__}")
    
    # List all module attributes
    all_attrs = dir(students_module)
    print(f"  Total attributes: {len(all_attrs)}")
    
    public_attrs = [x for x in all_attrs if not x.startswith('_')]
    print(f"  Public attributes ({len(public_attrs)}): {public_attrs}")
    
    if 'router' in all_attrs:
        print(f"  SUCCESS: router found = {students_module.router}")
    else:
        print(f"  ERROR: 'router' not in attributes")
        # Try to reload
        print("\n  Attempting manual reload...")
        import importlib
        importlib.reload(students_module)
        if hasattr(students_module, 'router'):
            print(f"  After reload: router = {students_module.router}")
        else:
            print(f"  After reload: still no router")
        
except Exception as e:
    print(f"  EXCEPTION: {e}")
    traceback.print_exc()
