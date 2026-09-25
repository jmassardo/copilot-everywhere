# Apply advertised discounts at exact tier boundaries

## Problem

Orders at exactly $100, $200, and $500 miss the advertised discount because
`discount_rate_for` uses a strict comparison.

## Acceptance criteria

- Exactly 10,000 cents receives the 5% tier.
- Exactly 20,000 cents receives the 10% tier.
- Exactly 50,000 cents receives the 15% tier.
- One cent below each boundary retains the lower tier.
- Focused tests cover every boundary.
- The full pytest suite and Ruff pass.

## Non-goals

- Do not change rounding behavior.
- Do not change monetary representation.
- Do not change API error behavior.
- Do not refactor unrelated pricing code.
