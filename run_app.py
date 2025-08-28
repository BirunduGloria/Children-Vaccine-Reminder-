#!/usr/bin/env python3
"""
Children Vaccine Reminder App Launcher

This script launches the main CLI application.
Run this file to start the vaccine reminder app.
"""

import sys
import os

# Add the lib directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

if __name__ == "__main__":
    try:
        from cli import main
        main()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please make sure you have installed all dependencies:")
        print("  pipenv install")
        print("  pipenv shell")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

