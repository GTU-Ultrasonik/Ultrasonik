# M3 — Control Firmware

**Team:** Rüya Koçak, Yusuf Batuhan Işık, Adem Erkiletlioğlu, Umutcan Çetin

**Stack:** C (hardware-free core) and C++ (ESP32 glue) with PlatformIO; Python for the HIL simulator and reports.

**Status:** S-level requirements R3.1, R3.2 and R3.4–R3.11, R3.13 pass on Windows and Linux with the
module's own stand-ins (native tests and HIL against a virtual board). **Not run yet:** R3.3 and every
test on the real ESP32 board (board not delivered yet), all B and R tests (R3.12). Nothing in this
folder has been flashed to a board.

## Interface
- Inputs: height (serial, M2), fan_state (serial, M1), target_points (UDP, M4), game_out (serial, game board), command (UDP, M5).
- Outputs: fan_cmd (serial, M1), status and ack (UDP, M5/M4). Not implemented yet: fan_config, game_in and the game-board serial link.
- Shared protocol: [shared/contract](../../shared/contract/) is still a draft (issue #1). **The frame
  payload layouts (`src/core/contract/`) and the JSON field names (`src/core/m3_core/m3_net.h`) used here
  are provisional and local to M3.** They follow the documented content of each message and will be
  replaced by the frozen shared contract. No shared file is changed by this module.

## Layout
| Path | Contents |
|---|---|
| `platformio.ini` | Builds: `native` (tests), `esp32` (control board), `esp32_simball` (same firmware with a simulated ball inside) |
| `src/core/m3_core/` | Hardware-free control logic: PID, state machine, height gate, target buffer, command checks, stuck-ball warning, network messages, plant model |
| `src/core/contract/` | Serial frame codec (CRC16/CCITT-FALSE, sessions, sequence numbers); payload layouts provisional |
| `src/firmware/` | ESP32 glue: control task on core 1; rx and Wi-Fi/UDP tasks on core 0; `m3_config.h` |
| `tests/native/` | Unity tests, one folder per suite; names carry the requirement ID (`test_R3_5_...`) |
| `tests/python/` | Contract mirror, HIL scenarios against the virtual board, M2 stand-in check |
| `tests/run_all.py` | The single command (R3.13) |
| `standins/hil/` | HIL simulator playing M1, M2, M4 and the M5 operator; live plot |
| `standins/vboard/` | Virtual board: the same `src/core` code behind stdin/stdout, so the HIL simulator runs without a board |
| `standins/m2/` | M2 stand-in filter for the tests (weaker than M2's own R2.4/R2.5 limits) |
| `standins/tuning/` | Gain search over R3.9 and T3.8 |
| `fixtures/` | Contract test vectors (C and Python produce the same bytes) |
| `config/` | `hil_config.example.json` (copy to `hil_config.json` for your ports; that copy is not committed) |
| `reports/` | Curated reports and plots; `reports/generated/` is local output and not committed |

`src/core` never calls hardware; time is always passed in. PlatformIO's folders are renamed in
`platformio.ini` because the repository `.gitignore` ignores every `lib/` folder.

## Run and test (Windows and Linux)
Requirements: Python 3.11+, `gcc` on PATH (MinGW-w64 on Windows). From this folder:

```
python -m pip install -r requirements.txt
python tests/run_all.py                # firmware build + native tests + HIL on the virtual board + report
python tests/run_all.py --no-firmware  # skip the ESP32 build (no toolchain download)
```

The report goes to `reports/generated/report_<os>_<time>.md`: commit and environment, every
requirement with its tests and result, the HIL measurements against their limits, and one plot per
scenario (`reports/generated/plots/`). The first firmware build downloads the ESP32 toolchain.
CI: `.github/workflows/m3-control-firmware.yml` runs the same command on `ubuntu-latest` and `windows-latest`.

### HIL simulator without a board
```
# Linux / Git Bash
gcc -O2 -std=gnu11 -Isrc/core/contract -Isrc/core/m3_core standins/vboard/vboard.c src/core/contract/*.c src/core/m3_core/*.c -lm -o vboard
# Windows PowerShell
gcc -O2 -std=gnu11 -Isrc/core/contract -Isrc/core/m3_core standins/vboard/vboard.c (Get-ChildItem src\core\contract\*.c, src\core\m3_core\*.c).FullName -lm -o vboard

python standins/hil/hil_sim.py --virtual ./vboard --scenario step --plot
python standins/hil/live_plot.py reports/generated/hil_step_virtual_<time>.csv   # redraw a saved run
```

Scenarios: `hold`; `step` (launch to 500 mm, down to 300 mm, measured 30 → 50 cm step; T3.8);
`targets` (M4 wave, clock offset, random network delay up to 150 ms; T3.7); `commands` (live changes
and refusals while flying; T3.10); failures `camera_loss`, `bridged_only`, `m1_fault`, `estop`,
`fan_state_lost` (failure at 10 s, cause cleared at 11 s, Reset/Start at 12 s; T3.2, T3.5, T3.6, T3.11).
Every run starts the board with JSON Reset and Start commands, as M5 would. `--plot` needs matplotlib.

### HIL with the real board
Same commands without `--virtual`. Copy `config/hil_config.example.json` to `config/hil_config.json`
and set the ports and the board IP. Wiring (all 3.3 V, common ground):
- board USB → computer: height link and flashing
- USB–UART adapter TX → GPIO16 (RX2), RX ← GPIO17 (TX2), GND: M1 link (fan_cmd / fan_state)
- second adapter on GPIO26/27: game-board link (firmware side not written yet)

Do not connect the adapters' 3.3 V/5 V pins; the board is powered from its USB. Wi-Fi name and password:
`src/firmware/wifi_secrets.h` (not committed), see `src/firmware/m3_config.h`.

Flash: `pio run -e esp32_simball -t upload` (simulated ball inside the board) or `pio run -e esp32 -t upload`.

## Network messages (UDP 5005, JSON; provisional field names)
- in: `command` (M5) → checked, applied, one `ack` per command to the sender; `target_points` (M4) → target buffer
- out: `status` at 30 Hz to the gateway (5010) and M4 (5006), broadcast by default
- a repeated `request_id` is answered with the same ack and not applied twice
- JSON is parsed on core 0; only structs reach the control task (R3.3)
- `status.diag`: `lat_max_us` (height received → fan_cmd written, worst case), `lat_over_5ms`,
  `heights_lost`, `net_bad` — the R3.3 measurement uses these on the real board

## Requirement traceability
| Req | Level | Tests | Issue | State |
|---|---|---|---|---|
| R3.1 PID | S | `test_pid` | #13 | pass (native) |
| R3.2 states, reset | S | `test_fsm`, HIL failure scenarios | #14 | pass (native, virtual board) |
| R3.3 height → fan_cmd ≤ 5 ms with Wi-Fi | S (board) | — | #15 | **not run**, needs the board; instrumentation in `status.diag` |
| R3.4 fan_cmd every 10 ms | S | `test_ctrl` | #15 | pass (native); board timing not run |
| R3.5, R3.6 timeout, raw fallback, bridged | S | `test_height_gate`, `test_ctrl`, HIL | #16 | pass (native, virtual board) |
| R3.7, R3.10 targets, commands | S | `test_target_buffer`, `test_command`, `test_net`, HIL | #17 | pass (native, virtual board) |
| R3.8, R3.9 hold, step, robustness | S | `test_ctrl`, HIL, `standins/tuning` | #18 | pass (native, virtual board) |
| R3.11 faults, stuck ball | S | `test_ctrl`, `test_stuck`, HIL | #19 | pass (native, virtual board) |
| R3.12 real ball | R | — | #21 | not run (rig) |
| R3.13 Windows and Linux | S | `tests/run_all.py`, CI | #20 | pass locally on both; board HIL not run |

## Control decisions
- **Gains** kp 1.8, ki 0.8, kd 0.5 (`standins/tuning/tune_gains.c`): R3.9 worst case over 27 model
  corners × 3 heights: mean 3.2 mm, swing 20.6 mm; T3.8 step: overshoot 40 mm, settled in 3.4 s.
  A middle choice: kd 0.7 was slightly better on M2's filtered height but swung up to 120 mm on raw heights only.
- **Target ramp** 250 mm/s (`target_rate_mm_s`): a step command becomes a ramp; after the launch the ramp
  starts at the ball and catches a ball that is already ahead. M4 waves (≤ 190 mm/s) are not changed.
- **M2 stand-in sends a filtered height** as M2 does, with a filter that is deliberately weaker than M2's
  own pass conditions (R2.5: 0.62 > 0.5; R2.4: 6.5 > 5 mm RMS; R2.10: lag 6 ms), checked in `tests/python/test_m2_standin.py`.
- **Stuck-ball warning (T3.11b):** the 3.5 s are counted from the moment all conditions hold
  (wanted speed ≥ 90 % of n_max), team decision 25.11.2026. With the current gains the speed reaches
  90 % about 26 s after the ball sticks.
- **Launch push** starts at 1.15 × hover and rises at 2000 rpm/s up to n_max until the ball lifts,
  so the ball lifts even when the hover speed is 30 % off the model.

## Known limits
- Without the filtered height (raw only, 5 mm noise) the ball is held but swings 60–90 mm (reported by
  the R3.6 test, not a pass condition). Safety is unaffected.
- After a launch to 300 mm the ball rises to about 480 mm before settling (about 2 mm at 500 mm).
  First real flights: launch to a mid height (about 500 mm), keep targets within 400–600 mm, E-stop at
  hand; soften `launch_ramp_rpm_s` once M4's fitted hover speed is known (R3.12).
- When the computer opens the board's USB port, the ESP32 may reset (DTR/RTS). It then starts in
  Fault, as on any restart; Reset and Start bring it back.

## Next
- Flash the board; HIL on the real board; R3.3: 10 min with Wi-Fi traffic, `lat_max_us` ≤ 5000, `heights_lost` = 0
- Game-board link (Serial1): game_in at 30 Hz, game_out → `m3_command_game_out`; `fan_config`
- HIL: repeated frame numbers, new M2 session, 10 bridged → only 5 used (native tests exist)
- Adopt the frozen shared contract (issue #1) for payload layouts and JSON names
