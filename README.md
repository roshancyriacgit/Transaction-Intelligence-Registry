# Transaction Intelligence Registry (TIR)

**Transaction Intelligence Registry (TIR)** is an **open specification** (and optional reference implementation) for mapping **transaction intent** to **applicable structures, rule-packs, and execution considerations** *before* a transaction is executed.

TIR is designed as a **neutral pre-execution reference layer** compatible with India Stack principles:
- **No advice** (legal/tax/investment), no enforcement, no execution
- **Deterministic + explainable** routing (traceable to inputs and rule-pack metadata)
- **Offline-first** reference implementation (optional), with update mechanisms specified separately

## What TIR is (and is not)

**TIR is:**
- A **standard** for representing transaction intent and producing a structured pre-execution plan
- A **registry interface** for rule-packs (domain obligations, steps, filings, evidence)
- A **record format** (TIR Record) for traceability and auditability

**TIR is not:**
- Legal/tax/investment advice
- A replacement for professionals
- A binding compliance determination
- A transaction execution platform

## Repository layout

- `spec/` — TIR-STD (schemas + semantics)
- `reference/` — TIR-REF (offline desktop prototype; illustrative)
- `examples/` — sample intents, demo rule-packs, demo outputs
- `docs/` — concept note, FAQ, non-goals, comparisons, India Stack fit

## Quick start (reference prototype)

1. Install Python 3.10+
2. Run the offline desktop app:

```bat
python reference\offline-desktop\app\tir_desktop.py
```

## License

Apache-2.0 (see `LICENSE`).

## Disclaimer

TIR outputs are for structured reference only. Verify statutes, forms, timelines, and regulatory requirements with qualified professionals and primary sources.

_Last updated: 2025-12-15_
