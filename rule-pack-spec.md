# Rule Pack Specification (TIR-RP v0.1)

A **rule pack** is a machine-readable bundle that:
- declares scope and provenance,
- describes trigger conditions (non-interpretive),
- outputs obligations, sequencing items, and filings touchpoints.

## Required top-level fields
- `rule_pack_id` (string)
- `version` (semantic version)
- `scope` (national/state/sector)
- `provenance` (source attribution + verification date)
- `rules` (array)

## Rule object (minimum)
Each rule must include:
- `id`
- `title`
- `domain`
- `trigger`
- `applies_if` (structured conditions; no interpretive statements)
- `references` (source metadata)
- `steps` (ordered considerations)
- `forms` (authority/form/timing where known)
- `risk_flags` (labels; not conclusions)
- `disclaimer_level` (illustrative|reference)

## Non-goals
- The rule pack must not provide advice or binding determinations.
- Timelines must be marked “verify” unless sourced precisely.

See `examples/demo-rule-packs/` for illustrative bundles.
