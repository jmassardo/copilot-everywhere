# Raw Feedback Queue

Unsorted. Collected from support tickets, sales calls, and the #orders-api Slack
channel over the last three weeks. Nobody has triaged this yet.

Used by the Product / dev-adjacent lab track.

---

**TICKET-4471** · support · 3 weeks ago
Customer says their invoice was off by a penny. They sent a screenshot. Finance
confirmed the math doesn't reconcile with their PO. Low value, but they're an
enterprise account and they're annoyed.

**SLACK** · @dana-sales · 3 weeks ago
Lost a deal partly because our API returns 200 on errors. Their integration team
said it was "a red flag for reliability." Not sure if that's the real reason but
it came up twice.

**TICKET-4488** · support · 2 weeks ago
"I placed an order for exactly $100 and didn't get the 5% bulk discount your
pricing page advertises. Ordered $100.01 the next day and got it. Is this a bug
or am I misreading the tiers?"

**SLACK** · @raj-eng · 2 weeks ago
Heads up, I tried to add a test for the pricing module and there isn't a single
one. We're shipping money code with zero coverage. Filing this here because I
don't know whose backlog it belongs on.

**TICKET-4502** · support · 2 weeks ago
Customer integration broke. They were checking for HTTP status codes to detect
failures and our customers endpoint always returns 200, so their retry logic
never fired. They ended up double-charging someone.

**SLACK** · @dana-sales · 11 days ago
Prospect asked if we support partial refunds. We don't have an endpoint for it.
How hard would that be?

**TICKET-4515** · support · 10 days ago
"Your docs say timestamps are UTC but they come back without a timezone offset.
My parser assumes local. Took me a day to figure out."

**SLACK** · @priya-eng · 9 days ago
We're going to have to deal with the deprecated datetime calls eventually.
Python 3.12 warns on them and 3.14 is going to be unpleasant.

**TICKET-4531** · support · 1 week ago
Enterprise customer wants to know why their tier discount isn't showing up
separately on the totals response. They can see a total but can't reconcile
which discount was applied.

**SLACK** · @dana-sales · 4 days ago
Second prospect this month asked about refunds. I think we need a real answer.

**TICKET-4540** · support · 3 days ago
"Deleting a customer doesn't do anything to their orders. I deleted a test
customer and their orders are still there, now pointing at nothing."

**SLACK** · @raj-eng · 2 days ago
Related to the above — we have no referential integrity between orders and
customers. It's an in-memory store so it's not catastrophic today, but if we
ever move to a real DB this becomes a data migration problem.

**INCIDENT-4552** · support escalation · today
Enterprise customer `cust-001` filtered the orders endpoint by their customer
ID and received an order belonging to `cust-002`. The unfiltered endpoint
looked normal. Support reproduced it twice. Treat this as a potential data
exposure until engineering proves otherwise.
