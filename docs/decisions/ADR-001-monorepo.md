# ADR-001: Monorepo layout

Status: initial team setup decision; review if needed.

Use one repository with five module directories and one shared message contract. This simplifies shared-interface updates, cross-module review and integration. The trade-off is shared repository access and the need for disciplined directory boundaries; team membership alone does not restrict write access to individual folders. Module stand-alone builds and tests remain independent. No change to the project module definitions.
