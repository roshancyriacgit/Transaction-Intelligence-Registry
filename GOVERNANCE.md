# Governance

## Purpose
Transaction Intelligence Registry (TIR) is designed as a **neutral pre-execution reference standard**. It standardises representation of transaction intent and the surfacing of applicable considerations via versioned rule packs.

## Neutrality and non-authoritativeness
- TIR does **not** provide legal/tax/investment advice.
- TIR does **not** make binding determinations.
- TIR outputs are structured references that require verification against primary sources and professional judgment.

## Maintainer responsibilities
Maintainers must ensure:
- clarity of schema and semantics
- backwards-compatible evolution where possible
- removal or rejection of content that implies advice, enforcement, or binding determinations
- provenance and traceability requirements for rule packs

## Decision-making
- Changes to `spec/` require maintainer review and consensus.
- Breaking changes require a major version increment and a migration note.

## Rule pack provenance
Any rule pack submitted must include:
- source type (statute/regulator/circular/industry practice)
- source identifiers (where available)
- date of last verification
- scope (national/state/sector)
- disclaimer level (illustrative vs production-grade)

## Public-interest posture
TIR is intended for open, public-interest use. Commercial implementations are permitted under Apache-2.0 but must not misrepresent outputs as advice.

_Last updated: 2025-12-15_
