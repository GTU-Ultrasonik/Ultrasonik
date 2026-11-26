# M1 — Blower Speed Control and Safety

**Team:** Efe Kaya, Ümit Gül, Ömer Faruk Gedikli, Hamdi Enes Taşınma

**Planned stack:** C++, PlatformIO, Python

**Status:** scaffold only. Implementations and test commands are pending.

## Interface
- Inputs: fan_cmd, fan_config, speed pulses, E-stop; optional height for characterization.
- Outputs: fan_state, PWM, enable, heartbeat, characterization CSV and plots.
- Shared protocol: [shared/contract](../../shared/contract/).

## Independent verification
Stand-ins: Simulated blower, command sender/receiver, pulse generator for bench tests.

Evidence: Speed steps, command loss, corrupted frames, limits, fault latching, dataset validation. Track R1.1–R1.13 / T1.1–T1.13 from section 4 of the November 2026 project documentation. Record S/B/R levels and numeric acceptance criteria. Do not claim success before running a test.

## Layout
- src/: implementation (split language-specific projects as needed).
- tests/: module-local unit and stand-alone tests.
- standins/: mock partners and simulators.
- fixtures/: small deterministic inputs and ground truth.
- config/: example settings.
- reports/: curated test evidence.

## Run and test
The team must add exact install, run and single-command test instructions when code is implemented. No other real module may be required for stand-alone verification.
