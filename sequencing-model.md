# Sequencing Model (Informative v0.1)

TIR represents execution as a **dependency-ordered list** of steps.

## Concepts
- **Step**: an action or verification checkpoint
- **Dependency**: a step that must precede another
- **Irreversibility marker**: a step after which reversal is costly (e.g., transfer, disbursement, registration)

## Policy
- TIR should surface irreversible points explicitly.
- TIR may propose checkpoints before irreversible points.
- TIR must avoid optimization claims; it can only surface routes and tradeoffs as labels.
