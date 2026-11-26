# GitHub automation

## Active baseline
repository-ci.yml checks the repository directory structure and example JSON on Windows and Ubuntu, on pull requests and pushes to main. It does **not** test module functionality.

Run locally from repository root: `python scripts/check_repository.py`.

## Module CI onboarding (pending)
Each team must add a reproducible, hardware-free test entry point, pinned dependencies and an actual workflow/job covering its software tests on both Windows and Ubuntu. Firmware native logic, synthetic data, protocol vectors, simulations and browser checks belong in hosted CI as applicable. Tests requiring physical boards, cameras, instruments or the complete rig run separately and their evidence is retained. Do not substitute skipped or dummy tests for passing results. Link requirement IDs and upload generated test reports and plots when available. Record board/HIL tests separately even if classified S by the course documentation.

Issue and PR templates are available. Do not claim full module CI coverage until all five teams have added and verified real tests.
