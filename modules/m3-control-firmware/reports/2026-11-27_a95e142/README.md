# M3 verification run — 2026-11-27, commit a95e142

Produced with `python tests/run_all.py` from `modules/m3-control-firmware/` on a clean checkout of
commit `a95e142`, once on Windows 11 (Python 3.13) and once on Linux (Ubuntu 24.04 under WSL2, Python 3.12).

| | Windows | Linux |
|---|---|---|
| Firmware build (esp32, esp32_simball) | PASS | PASS |
| Native C tests (Unity) | PASS | PASS |
| Python tests (contract, HIL on the virtual board, M2 stand-in) | 17 passed | 17 passed |

- `report_windows.md`, `report_linux.md`: requirement table, HIL measurements against their limits,
  every test case. The HIL measurements are identical on both systems (fixed random seeds).
- `plots/`: one plot per HIL scenario (true height, height sent to the board, board target, blower speed, state).

Level: **S only**, software and the virtual board (`standins/vboard`, the same `src/core` code as the
firmware). **Not run:** R3.3 and every test on the real ESP32 board (not delivered yet); B and R tests (R3.12).
GitHub Actions results for this commit are not part of this folder.
