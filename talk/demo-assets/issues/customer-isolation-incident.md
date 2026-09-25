# Customer filter may expose another customer's orders

## Report

Support reproduced `GET /orders?customer_id=cust-001` returning an order owned
by `cust-002`. The unfiltered endpoint appears normal. Treat this as a potential
customer-data exposure.

## Required outcome

- Investigate and reproduce before changing production code.
- Add a regression test proving every returned order belongs to the requested
  customer.
- Make the smallest safe fix.
- Run the focused test, full suite, and Ruff.

## Non-goals

- Do not change pricing behavior.
- Do not standardize unrelated API errors.
- Do not refactor storage beyond the incident's root cause.
