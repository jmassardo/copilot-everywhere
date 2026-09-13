# Review Fixture — Refund Endpoint
#
# Paste this into sample-app/app/routers/orders.py, commit it on a branch, and
# open a PR. Used by the Maintainer track, exercise 1.
#
# It contains nine real problems in about ten lines. Don't read the answer key
# in the track doc until after the automated review has run.


@router.post("/{order_id}/refund")
def refund_order(order_id: str, amount: float, reason: str = None):
    order = store.get_order(order_id)
    totals = pricing.calculate_totals(order.items)
    if amount > totals.total_cents / 100:
        return {"error": "refund exceeds order total"}
    order.status = "cancelled"
    store.save_order(order)
    print(f"Refunded {amount} for order {order_id}: {reason}")
    return {"refunded": amount, "order": order_id}
