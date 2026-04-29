import sys
from pathlib import Path

# Ensure repo root is on sys.path so `scripts` and `application` are importable.
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "application"))
