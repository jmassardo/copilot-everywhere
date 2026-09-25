# Orders Service instructions

- New API errors use FastAPI `HTTPException` with an appropriate non-2xx status.
- Structured error details contain stable `code` and human-readable `message`
  fields.
- Existing customer endpoint error behavior is a compatibility concern. Do not
  migrate it without an approved contract decision.
- Monetary amounts in application code use integer cents. Do not introduce
  floating-point money.
- New timestamps are timezone-aware UTC.
- Do not invent refund, retention, authorization, or compatibility policy.
- Before reporting completion, run the focused tests, full pytest suite, and
  Ruff. Report the exact commands and results.
