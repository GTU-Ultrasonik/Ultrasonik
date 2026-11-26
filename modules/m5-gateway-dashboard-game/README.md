# M5 — Message Contract, Gateway, Dashboard and Game

**Team:** Mustafa Yıldız, Mert Sefa Yavuz, Efe Kaya, Ümit Gül

**Planned stack:** Python, TypeScript, C++, PlatformIO, uPlot

**Status:** scaffold only. Implementations and test commands are pending.

## Interface
- Inputs: height, status, model_height, ack, browser actions, game_in, buttons.
- Outputs: command, WebSocket data, contract, logs/exports, game_out, LED/buzzer.
- Shared protocol: [shared/contract](../../shared/contract/).

## Independent verification
Stand-ins: Mock modules, session replay, browser tests, control-board script.

Evidence: Protocol vectors, malformed data, routing, replay, graph markers, game rules. Track R5.1–R5.13 / T5.1–T5.13 from section 8 of the November 2026 project documentation. Record S/B/R levels and numeric acceptance criteria. Do not claim success before running a test.

## Layout
- src/: implementation (split language-specific projects as needed).
- tests/: module-local unit and stand-alone tests.
- standins/: mock partners and simulators.
- fixtures/: small deterministic inputs and ground truth.
- config/: example settings.
- reports/: curated test evidence.

## Run and test
The team must add exact install, run and single-command test instructions when code is implemented. No other real module may be required for stand-alone verification.
