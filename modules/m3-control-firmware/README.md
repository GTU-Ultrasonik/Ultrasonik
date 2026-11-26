# M3 — Control Firmware

**Team:** Rüya Koçak, Yusuf Batuhan Işık, Adem Erkiletlioğlu, Umutcan Çetin

**Planned stack:** C++, PlatformIO, Python

**Status:** scaffold only. Implementations and test commands are pending.

## Interface
- Inputs: height, fan_state, target_points, game_out, command.
- Outputs: fan_cmd, fan_config, game_in, status, ack.
- Shared protocol: [shared/contract](../../shared/contract/).

## Independent verification
Stand-ins: Built-in simulated ball/blower, HIL simulator, game-board script.

Evidence: PID reference values, state transitions, timeout, hold/step/wave and robustness plots. Track R3.1–R3.13 / T3.1–T3.13 from section 6 of the November 2026 project documentation. Record S/B/R levels and numeric acceptance criteria. Do not claim success before running a test.

## Layout
- src/: implementation (split language-specific projects as needed).
- tests/: module-local unit and stand-alone tests.
- standins/: mock partners and simulators.
- fixtures/: small deterministic inputs and ground truth.
- config/: example settings.
- reports/: curated test evidence.

## Run and test
The team must add exact install, run and single-command test instructions when code is implemented. No other real module may be required for stand-alone verification.
