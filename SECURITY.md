# Security Policy

## Reporting a vulnerability
If you discover a security issue, please open a private disclosure via the repository's security/advisory mechanism (preferred). If unavailable, use the repository issue tracker with minimal details and request a private channel.

## Scope
- The `spec/` directory defines schemas and semantics; security issues typically concern ambiguity or unsafe extensibility.
- The `reference/` implementation is illustrative and offline-first. It should **not** be used for production decisioning.

## Non-goals
- Handling real personal data in the repository. Do not submit real IDs, KYC docs, or transaction data in issues/PRs.
