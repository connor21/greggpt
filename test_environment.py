"""Test script to validate environment setup."""
import sys
import importlib

REQUIRED_PACKAGES = [
    "black",
    "pydantic",
    "fastapi",
    "sqlalchemy",
    "sqlmodel"
]

def test_imports():
    """Test that all required packages can be imported."""
    failed = []
    for package in REQUIRED_PACKAGES:
        try:
            importlib.import_module(package)
            print(f"✓ {package} imported successfully")
        except ImportError:
            failed.append(package)
            print(f"✗ Failed to import {package}")

    if failed:
        print("\nERROR: Failed to import packages:", ", ".join(failed))
        sys.exit(1)
    print("\nSUCCESS: All packages imported successfully")
    sys.exit(0)

if __name__ == "__main__":
    test_imports()
