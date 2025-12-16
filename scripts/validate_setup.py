#!/usr/bin/env python3
"""
Script to validate the setup and dependencies.
"""

import sys
import importlib

def check_import(module_name):
    """Check if a module can be imported."""
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False

def main():
    """Validate setup."""
    print("🔍 Validating Investment Agent setup...")
    
    required_modules = [
        'streamlit',
        'agno',
    ]
    
    all_ok = True
    for module in required_modules:
        if check_import(module):
            print(f"✅ {module}")
        else:
            print(f"❌ {module} - NOT FOUND")
            all_ok = False
    
    if all_ok:
        print("\n✅ All dependencies are installed!")
        return 0
    else:
        print("\n❌ Some dependencies are missing. Run: pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())

