# Replace deprecated naive UTC timestamps

## Problem

Application code uses `datetime.utcnow()`, which produces naive datetime values
and is deprecated in current Python.

## Acceptance criteria

- Replace application uses with timezone-aware UTC values.
- Preserve existing API field names and response structure.
- Add or adjust focused tests if serialized values change.
- Run the full pytest suite and Ruff.

## Non-goals

- Do not change dependencies.
- Do not change pricing behavior.
- Do not modify generated analytics data.
- Do not standardize unrelated API error behavior.
