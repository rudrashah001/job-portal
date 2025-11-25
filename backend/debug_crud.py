import sys
import app.crud

print(f"crud file: {app.crud.__file__}")
print(f"crud dict keys: {list(app.crud.__dict__.keys())[:20]}")

if hasattr(app.crud, "create_user"):
    print("HAS create_user")
else:
    print("NO create_user")
    
# Check file size
import os
fsize = os.path.getsize(app.crud.__file__)
print(f"File size: {fsize} bytes")
