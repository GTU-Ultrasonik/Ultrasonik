"""Validate repository scaffolding, not module correctness."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULES = (
    "m1-blower-control", "m2-vision-estimation", "m3-control-firmware",
    "m4-motion-model-twin", "m5-gateway-dashboard-game",
)
required = ["README.md", "CONTRIBUTING.md", "shared/contract/protocol.md",
            "hardware/README.md", "tests/integration/README.md",
            "config/system.example.json"]
for module in MODULES:
    base = f"modules/{module}"
    required.append(f"{base}/README.md")
    required.extend(f"{base}/{name}" for name in
                    ("src", "tests", "standins", "fixtures", "config", "reports"))
missing = [name for name in required if not (ROOT / name).exists()]
if missing:
    raise SystemExit("Missing repository paths: " + ", ".join(missing))
with (ROOT / "config/system.example.json").open(encoding="utf-8") as handle:
    json.load(handle)
print("Repository layout and example JSON: PASS")
print("Module verification: not performed by this check.")
