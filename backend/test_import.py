import sys
sys.path.insert(0, '.')

try:
    from app.schemas.log import LogCreate
    print("Import successful!")
    print(f"LogCreate: {LogCreate}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    
    # Try to debug
    print("\nTrying to import the module directly...")
    try:
        import app.schemas.log as log_module
        print(f"Module contents: {dir(log_module)}")
    except Exception as e2:
        print(f"Error importing module: {e2}")
        traceback.print_exc()
