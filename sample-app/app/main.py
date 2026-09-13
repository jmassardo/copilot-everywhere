from fastapi import FastAPI

from app.routers import customers, orders

app = FastAPI(
    title="Orders Service",
    description="Workshop sample app for the Copilot Everywhere lab.",
    version="0.3.0",
)

app.include_router(orders.router)
app.include_router(customers.router)


@app.get("/health")
def health():
    return {"status": "ok"}
