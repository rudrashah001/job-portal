import traceback
import sys

print("Testing each router import individually...\n")

routers = ['jobs', 'students', 'recruiters', 'admin']

for router_name in routers:
    try:
        module = __import__(f'app.routes.{router_name}', fromlist=[router_name])
        print(f"OK: app.routes.{router_name} imports OK")
        if hasattr(module, 'router'):
            print(f"    HAS 'router' attribute")
        else:
            print(f"    NO 'router' attribute - ERROR")
    except Exception as e:
        print(f"FAIL: app.routes.{router_name} - {e}")
        traceback.print_exc()
        print()

print("\nNow testing main app import...")
try:
    from app.main import app
    print(f"OK: app.main.app imported: {app}")
except Exception as e:
    print(f"FAIL: app.main - {e}")
    traceback.print_exc()
