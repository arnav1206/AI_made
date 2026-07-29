import sys
import os

# Set path to bharat_voice2form directory
base_dir = os.path.join(os.path.dirname(__file__), "bharat_voice2form")
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

os.chdir(base_dir)

# Execute main application script
with open(os.path.join(base_dir, "app.py"), encoding="utf-8") as f:
    code = compile(f.read(), "app.py", "exec")
    exec(code, {"__file__": os.path.join(base_dir, "app.py")})
