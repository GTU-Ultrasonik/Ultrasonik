# M2 — Vision and Height Estimation

**Team:** Ömer Faruk Gedikli, Hamdi Enes Taşınma, Rüya Koçak, Yusuf Batuhan Işık

**Planned stack:** Python, OpenCV, NumPy

**Status:** scaffold only. Implementations and test commands are pending.

## Interface
- Inputs: Camera frames, command, calibration marks and profiles.
- Outputs: height (serial/UDP), ack, calibration file and measured camera delay.
- Shared protocol: [shared/contract](../../shared/contract/).

## Independent verification
Stand-ins: Synthetic/recorded video, mock serial and UDP receivers, known ball heights.

Evidence: Raw vs filtered plots, accuracy, dropped frames, glare, plausibility, restart. Track R2.1–R2.13 / T2.1–T2.13 from section 5 of the November 2026 project documentation. Record S/B/R levels and numeric acceptance criteria. Do not claim success before running a test.

## Layout
- src/: implementation (split language-specific projects as needed).
- tests/: module-local unit and stand-alone tests.
- standins/: mock partners and simulators.
- fixtures/: small deterministic inputs and ground truth.
- config/: example settings.
- reports/: curated test evidence.

## Run and test
The team must add exact install, run and single-command test instructions when code is implemented. No other real module may be required for stand-alone verification.
