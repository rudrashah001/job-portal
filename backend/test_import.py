import traceback
import sys

try:
    print("Python path:", sys.path[:3])
    print("Importing app.main...")
    from app.main import app
    print("SUCCESS: app imported successfully")
    print(f"app type: {type(app)}")
    print(f"app title: {app.title}")
except Exception as e:
    print(f"ERROR importing app: {e}")
    traceback.print_exc()
