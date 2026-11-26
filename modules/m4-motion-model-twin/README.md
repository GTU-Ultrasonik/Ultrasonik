# M4 — Motion Planning, Plant Model and Digital Twin

**Team:** Adem Erkiletlioğlu, Umutcan Çetin, Mustafa Yıldız, Mert Sefa Yavuz

**Planned stack:** Python, SciPy, TypeScript, Three.js

**Status:** scaffold only. Implementations and test commands are pending.

## Interface
- Inputs: command, status, characterization dataset, rig dimensions, session/live data.
- Outputs: target_points, ack, model_height, model file, 3D view.
- Shared protocol: [shared/contract](../../shared/contract/).

## Independent verification
Stand-ins: Local target receiver, synthetic dataset with known coefficients, session files.

Evidence: Trajectory formulas, continuity, model fit, ghost-ball and twin performance. Track R4.1–R4.13 / T4.1–T4.13 from section 7 of the November 2026 project documentation. Record S/B/R levels and numeric acceptance criteria. Do not claim success before running a test.

## Layout
- src/: implementation (split language-specific projects as needed).
- tests/: module-local unit and stand-alone tests.
- standins/: mock partners and simulators.
- fixtures/: small deterministic inputs and ground truth.
- config/: example settings.
- reports/: curated test evidence.

## Run and test
The team must add exact install, run and single-command test instructions when code is implemented. No other real module may be required for stand-alone verification.
