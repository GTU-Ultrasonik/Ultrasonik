"""One command for M3 (R3.13) -> reports/generated/report_<os>_<time>.md

    python tests/run_all.py                 # everything below (run from the module folder)
    python tests/run_all.py --no-firmware   # skip the ESP32 build (no toolchain download)

Steps: 1. firmware build (esp32, esp32_simball)
       2. native C tests, including the closed-loop simulation (test_ctrl: R3.8, R3.9, R3.11)
       3. Python tests: HIL simulator against the virtual board, over the same serial
          frames and UDP JSON as the real board (R3.7, R3.10, R3.13)

Same on Windows and Linux. Test names carry the requirement ID
(test_R3_5b_... -> R3.5), so the report lists every M3 requirement with its
tests, pass/fail, and the ones not covered yet. It also records the commit and
environment, the HIL measurements against their limits, and (with matplotlib)
one plot per HIL scenario in reports/generated/plots/.

Everything here is S level on the virtual board: tests that need the real board
(R3.3) or the rig (R3.12) are reported as not run.
"""
from __future__ import annotations

import json
import os
import platform
import re
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports" / "generated"

REQUIREMENTS = {
    "R3.1": ("PID computes exactly as designed", "S"),
    "R3.2": ("States and reset sequence as in the table", "S"),
    "R3.3": ("Every height used within 5 ms with Wi-Fi active (HIL)", "S"),
    "R3.4": ("fan_cmd at least every 10 ms, new sequence number", "S"),
    "R3.5": ("Fault within 200 ms without a new real measurement", "S"),
    "R3.6": ("Raw fallback without jump; at most 5 bridged", "S"),
    "R3.7": ("Targets played on time despite network delay", "S"),
    "R3.8": ("Holds and moves the simulated ball", "S"),
    "R3.9": ("Gains robust to +-30 % model error and bad data", "S"),
    "R3.10": ("Commands checked; safety limits locked; game only in game mode", "S"),
    "R3.11": ("M1 fault / fan_state lost / E-stop -> fault; stuck-ball warning", "S"),
    "R3.12": ("Holds the real ball", "R"),
    "R3.13": ("Runs alone on Windows and Linux", "S"),
}
REQ_RE = re.compile(r"R(\d)_(\d+)")


def run(cmd: list[str], cwd: Path) -> int:
    print("$", " ".join(cmd), flush=True)
    return subprocess.call(cmd, cwd=cwd)


def parse_junit(path: Path, suite: str) -> list[tuple[str, str, bool, str]]:
    if not path.exists():
        return [(suite, "<no result file>", False, "test run did not produce a report")]
    out = []
    for case in ET.parse(path).iter("testcase"):
        fail = case.find("failure") if case.find("failure") is not None else case.find("error")
        msg = (fail.get("message") or fail.text or "").strip().splitlines()[0][:120] if fail is not None else ""
        out.append((case.get("classname") or suite, case.get("name", "?"), fail is None, msg))
    return out


# requirement, scenario, value key, limit, comparison, unit  (limits from T3.x, Section 6)
HIL_CHECKS = [
    ("R3.5", "camera_loss", "fault_after_ms", 200.0, "<=", "ms to Fault, no new real height"),
    ("R3.6", "bridged_only", "fault_after_ms", 200.0, "<=", "ms to Fault, bridged heights only"),
    ("R3.7", "targets", "target_err_max_mm", 5.0, "<=", "mm, board target vs sent, delay <= 150 ms"),
    ("R3.8", "step", "overshoot_mm", 50.0, "<", "mm overshoot, 30 -> 50 cm step"),
    ("R3.8", "step", "settle_s", 4.0, "<=", "s settled within +-2 cm"),
    ("R3.8", "step", "mean_err_mm", 20.0, "<=", "mm mean error after the step"),
    ("R3.8", "step", "p2p_mm", 30.0, "<=", "mm oscillation after the step"),
    ("R3.9", "hold_bad_data", "mean_err_mm", 30.0, "<=", "mm mean error, 5 mm noise, 5 % drops"),
    ("R3.9", "hold_bad_data", "p2p_mm", 50.0, "<=", "mm oscillation, 5 mm noise, 5 % drops"),
    ("R3.11", "m1_fault", "fault_after_ms", 100.0, "<=", "ms to Fault after an M1 fault"),
    ("R3.11", "estop", "fault_after_ms", 100.0, "<=", "ms to Fault after the E-stop"),
    ("R3.11", "fan_state_lost", "fault_after_ms", 110.0, "<=", "ms to Fault, fan_state lost (100 ms + one frame)"),
]


def git_info() -> str:
    try:
        sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True,
                             text=True).stdout.strip()
        dirty = subprocess.run(["git", "status", "--porcelain", "--", "."], cwd=ROOT, capture_output=True,
                               text=True).stdout.strip()
        return f"{sha}{' + uncommitted changes' if dirty else ''}" if sha else "unknown"
    except OSError:
        return "unknown"


def main() -> int:
    build_fw = "--no-firmware" not in sys.argv[1:]
    REPORTS.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    osname = platform.system().lower()
    c_xml = REPORTS / f"native_{osname}.xml"
    py_xml = REPORTS / f"python_{osname}.xml"

    rc_fw = None
    if build_fw:
        rc_fw = run([sys.executable, "-m", "platformio", "run", "-e", "esp32", "-e", "esp32_simball"], ROOT)
    rc_c = run([sys.executable, "-m", "platformio", "test", "-e", "native",
                "--junit-output-path", str(c_xml)], ROOT)
    (REPORTS / f"hil_virtual_{osname}.json").unlink(missing_ok=True)  # never report a stale run
    rc_py = run([sys.executable, "-m", "pytest", "-q", "tests/python", f"--junitxml={py_xml}"], ROOT)

    results = parse_junit(c_xml, "native") + parse_junit(py_xml, "python")
    by_req: dict[str, list] = defaultdict(list)
    for r in results:
        m = REQ_RE.search(r[1])
        by_req[f"R{m.group(1)}.{m.group(2)}" if m else "other"].append(r)

    lines = [
        f"# M3 test report — {stamp}",
        "",
        f"- Commit: {git_info()}",
        f"- System: {platform.system()} {platform.release()} · Python {platform.python_version()}",
        "- Level: S (software and virtual board). B and R tests are not part of this run.",
        f"- Firmware build (esp32, esp32_simball): "
        f"{'skipped' if rc_fw is None else 'PASS' if rc_fw == 0 else 'FAIL'}",
        f"- Native C tests: {'PASS' if rc_c == 0 else 'FAIL'} · Python tests: {'PASS' if rc_py == 0 else 'FAIL'}",
        "",
        "| Req | Level | Requirement | Tests | Result |",
        "|---|---|---|---|---|",
    ]
    for rid, (text, level) in REQUIREMENTS.items():
        tests = by_req.get(rid, [])
        if not tests:
            status = "not run (needs the board, HIL)" if level == "S" else "not run (rig, integration)"
        else:
            status = "PASS" if all(t[2] for t in tests) else "FAIL"
        lines.append(f"| {rid} | {level} | {text} | {len(tests)} | {status} |")

    hil = REPORTS / f"hil_virtual_{osname}.json"
    if hil.exists():
        lines += ["", "## HIL simulator, virtual board", "",
                  "| Scenario | Board state | Mean error mm | Peak-to-peak mm | Overshoot mm | Settled s "
                  "| Target vs sent max mm | Fault after ms | Cause | Fault until Reset | Acks | Status msgs "
                  "| Bad JSON | CRC errors |",
                  "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]

        def cell(v):
            return "-" if v is None else v

        for name, r in json.loads(hil.read_text(encoding="utf-8")).items():
            lines.append(f"| {name} | {r['final_state']} | {cell(r['mean_err_mm'])} | {cell(r['p2p_mm'])} | "
                         f"{cell(r.get('overshoot_mm'))} | {cell(r.get('settle_s'))} | "
                         f"{cell(r.get('target_err_max_mm'))} | {cell(r.get('fault_after_ms'))} | "
                         f"{cell(r.get('fault_cause'))} | {cell(r.get('in_fault_until_reset'))} | "
                         f"{len(r.get('acks', []))} | {r.get('status_msgs', 0)} | {r.get('bad_json', 0)} | "
                         f"{r['crc_errors']} |")
        lines += ["", "Mean error in the targets scenario is the ball's tracking error without "
                  "feed-forward (M4's job, R4.7); T3.7 is the target column."]

        hil_res = json.loads(hil.read_text(encoding="utf-8"))
        lines += ["", "## Measured against the limits (HIL, virtual board)", "",
                  "| Req | Scenario | Measured | Limit | Result |", "|---|---|---|---|---|"]
        for rid, scen, key, limit, op, what in HIL_CHECKS:
            v = (hil_res.get(scen) or {}).get(key)
            ok = v is not None and (v <= limit if op == "<=" else v < limit)
            lines.append(f"| {rid} | {scen} | {'-' if v is None else v} {what} | {op} {limit:g} | "
                         f"{'PASS' if ok else 'FAIL' if v is not None else 'not run'} |")

        try:  # one plot per scenario; matplotlib is optional (demo only)
            os.environ.setdefault("MPLBACKEND", "Agg")
            sys.path.insert(0, str(ROOT / "standins" / "hil"))
            import live_plot

            plots = REPORTS / "plots"
            plots.mkdir(exist_ok=True)
            lines += ["", "## Plots", ""]
            for name, r in hil_res.items():
                src = Path(r.get("log", ""))
                if src.exists():
                    png = plots / f"{name}_{osname}.png"
                    live_plot.save_png(src, png, f"M3 HIL - {name} - virtual board - {osname}")
                    lines.append(f"- {name}: plots/{png.name}")
        except Exception as e:  # noqa: BLE001 - the report must still be written
            lines += ["", f"Plots skipped: {e}"]

    lines += ["", "## All test cases", "", "| Suite | Test | Result | Message |", "|---|---|---|---|"]
    for suite, name, ok, msg in results:
        lines.append(f"| {suite} | {name} | {'PASS' if ok else 'FAIL'} | {msg} |")

    report = REPORTS / f"report_{osname}_{stamp}.md"
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nreport: {report}")
    return 0 if rc_c == 0 and rc_py == 0 and rc_fw in (None, 0) else 1


if __name__ == "__main__":
    sys.exit(main())
