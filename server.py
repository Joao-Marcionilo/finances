"""
Local server to test the system of this API
You can test the system accessing http://127.0.0.1:8000/docs after running the code
"""

from typing import List, Annotated, Literal

import uvicorn
from fastapi import FastAPI, Query, HTTPException

import models
import system


app = FastAPI(
    title="Finances API",
    description="Local server to test the system of this API",
    version="1.0",
    contact={
        "name": "João Marcionilo",
        "email": "marcionilojob@gmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }
)


@app.get("/transactions", tags=['Registries'])
async def get_transaction(
        update: Annotated[bool | None, ...] = True,
        start: Annotated[int | None, Query(gt=-1)] = 0,
        quantity: Annotated[int | None, Query(gt=-1)] = 0
) -> List[models.TransactionReceive]:
    """Fetch for the registries of all transactions"""
    print(operator.get_transaction(update=update, start=start, quantity=quantity))
    return operator.get_transaction(update=update, start=start, quantity=quantity)


@app.post("/transactions", status_code=204, tags=['Registries'])
async def post_transaction(body: models.TransactionSend):
    """Registry a new transaction"""
    operator.post_transaction(**dict(body))


@app.delete("/transactions", status_code=204, tags=['Registries'])
async def delete_transaction(
        identifier: Annotated[int, Query(gt=0)]
):
    """Delete a transaction"""
    operator.delete_transaction(identifier)


@app.patch("/transactions", status_code=200, tags=['Registries'])
async def patch_transaction() -> models.Changed:
    """Update the registries with the transactions in 'Incomes' and 'Expenses' tables that reached their date"""
    return models.Changed(state=operator.patch_transaction())


@app.get("/periodic/transactions", tags=['Incomes and Expenses'])
async def get_periodic_transactions() -> List[models.PeriodicTransactions]:
    """Fetch for the proprieties of all periodic transactions of 'Incomes' and 'Expenses' tables"""
    return operator.get_periodic_transactions()


@app.post(
    "/periodic/transactions", tags=['Incomes and Expenses'], status_code=201,
    responses={201: {"model": models.Message}, 409: {"model": models.Message}})
async def post_periodic_transactions(body: models.PeriodicTransactions) -> models.Message:
    """Add a new periodic transaction in the 'Incomes' or 'Expenses' tables"""
    result = operator.post_periodic_transactions(**dict(body))
    if result[0] == 201:
        return models.Message(message=result[1])
    raise HTTPException(status_code=result[0], detail=result[1])


@app.delete("/periodic/transactions/", status_code=204, tags=['Incomes and Expenses'])
async def delete_periodic_transactions(table: Literal["Incomes", "Expenses"], title: str):
    """Delete a periodic transaction in the 'Incomes' or 'Expenses' tables"""
    print(table)
    operator.delete_periodic_transactions(table, title)


def run():
    global operator

    operator = system.Operator()
    uvicorn.run(app, port=8000)


if __name__ == "__main__":
    run()