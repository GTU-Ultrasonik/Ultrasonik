# Contributing to Ultrasonik

## Workflow
1. Choose or create an issue with module, requirement/test ID, acceptance criteria and test level.
2. Update main: `git switch main` and `git pull --ff-only`.
3. Create a short-lived branch, e.g. `git switch -c feat/m2-kalman-filter`.
4. Implement only the assigned scope. Add tests, run them locally and record evidence.
5. Stage selected files, commit in English (e.g. `feat(m2): implement height estimator`), then push with `git push -u origin feat/m2-kalman-filter`.
6. Open a PR to main, link the issue and request review from a teammate. Resolve feedback and merge only when applicable tests pass and a teammate approves. Delete the branch after merging.

Use feat/, fix/, test/, docs/ or chore/ prefixes. Avoid direct pushes to main after bootstrap. Review and test rules are team policy until technically enforced; this setup does not enable branch protection.

## Independence and interfaces
Keep each module's source, tests and mocks local. Only depend on shared/contract for common interfaces. Contract changes require M5 and affected module teams to agree, update documentation and test vectors together, and record the version. Never silently modify fixed safety limits. Separate hardware adapters from testable logic.

## Evidence and reproducibility
Use pinned dependencies and portable config. Do not commit credentials, local machine settings, generated build outputs or large raw recordings. Store curated reports and plots with requirement/test IDs, threshold, measured value, pass/fail, commit, environment and data provenance. Distinguish S/B/R; never report unrun tests as passing. Include exact reproduction commands in the module README.

Use English for technical docs, issue titles and commits. Keep PRs scoped and avoid unrelated formatting changes. Discuss shared decisions before merging.
