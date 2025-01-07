# Quickstart

Package with CRUD using SQL Server and a FastAPI local server for testing it

## Initialization

**Class:** `Operator(credentials="DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;TRUSTED_CONNECTION=yes;", database="Finances")`

Initialize the operator to utilize its CRUD methods


### Example

```
from joao_marcionilo_finances import Operator

#default
credential="""
    DRIVER={ODBC Driver 17 for SQL Server};
    SERVER=localhost;
    TRUSTED_CONNECTION=yes;
"""

operator = Operator(credential=credential)
```

### Parameters

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| `credentials` | `str` | Configure PYODBC connection string |
| `database` | `str` | Define the database custom name |

### Methods
- [`delete_periodic_transactions`](#delete-transaction-from-"incomes"-or-"expenses"): Delete a periodic transaction in the "Incomes" or "Expenses" tables
- [`delete_transaction`](#delete-transaction-from-registries): Delete a transaction
- [`get_periodic_transactions`](#fetch-"incomes"-and-"expenses"): Fetch for the proprieties of all periodic transactions of "Incomes" and "Expenses" tables
- [`get_transaction`](#fetch-registries): Fetch for the registries of all transactions
- [`patch_transaction`](#update-registries): Update the registries with the transactions in "Incomes" and "Expenses" tables that reached their date
- [`post_periodic_transactions`](#add-transaction-to-"incomes"-or-"expenses"): Add a new periodic transaction in the "Incomes" or "Expenses" tables
- [`post_transaction`](#add-transaction-to-registries): Registry a new transaction


    

## Delete transaction from "Incomes" or "Expenses"

**Method:** `Operator.delete_periodic_transactions(table:str, title:str)`

Delete a periodic transaction in the "Incomes" or "Expenses" tables


### Example

```
from joao_marcionilo_finances import Operator

operator = Operator()
operator.delete_periodic_transactions("Incomes", "Salary")
```

### Parameters

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| `table` | `str` | Table of the transaction |
| `title` | `str` | Title of the transaction |




    

## Delete transaction from registries

**Method:** `Operator.delete_transaction(identifier:int)`

Delete a transaction


### Example

```
from joao_marcionilo_finances import Operator

operator = Operator()
operator.delete_transaction(1)
```

### Parameters

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| `identifier` | `int` | ID of the transaction to delete |




    

## Fetch "Incomes" and "Expenses"

**Method:** `Operator.get_periodic_transactions()`

Fetch for the proprieties of all periodic transactions of "Incomes" and "Expenses" tables


### Example

```
from joao_marcionilo_finances import Operator

operator = Operator()
transactions = operator.get_transaction()
print(transactions)
```





### Return type: `list`
    

## Fetch registries

**Method:** `Operator.get_transaction(update=True, start=0, quantity=0)`

Fetch for the registries of all transactions


### Example

```
from joao_marcionilo_finances import Operator

operator = Operator()
registries = operator.get_transaction(start=0, quantity=20)
print(registries)
```

### Parameters

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| `update` | `bool` | Update registries before fetching |
| `start` | `int` | Define how many transactions should be omitted from the newest to oldest registries |
| `quantity` | `int` | Define a limit of transactions to return |



### Return type: `list`
    

## Update registries

**Method:** `Operator.patch_transaction()`

Update the registries with the transactions in "Incomes" and "Expenses" tables that reached their date


### Example

```
from joao_marcionilo_finances import Operator

operator = Operator()
state = operator.patch_transaction()
print(state)
```





### Return type: `str`
    

## Add transaction to "Incomes" or "Expenses"

**Method:** `Operator.post_periodic_transactions(table:str, title:str, value:str, interval:str, number:int, next_date:date, limit=-1)`

Add a new periodic transaction in the "Incomes" or "Expenses" tables


### Example

```
from datetime import date

from joao_marcionilo_finances import Operator

operator = Operator()
transactions = operator.post_periodic_transactions(
    "Salary", "999.99", "MONTH", 1, date(2024, 9, 17),
    limit=12, summary="Monthly income"
)
```

### Parameters

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| `table` | `str` | "Incomes" or "Expenses" |
| `title` | `str` | Title of the transaction. Max length 100 |
| `value` | `str` | Value of the transaction. Expenses should start with a "-". Max length 20 |
| `interval` | `str` | Define the "interval" of the SQL Server function "DATEADD" |
| `number` | `int` | Define the "number" of the SQL Server function "DATEADD" |
| `next_date` | `date` | Date of the next transaction |
| `limit` | `int` | Add a maximum number of times this transaction can be used |



### Return type: `tuple`
    

## Add transaction to registries

**Method:** `Operator.post_transaction(value:str, subtraction:bool, time="", title="", summary="")`

Registry a new transaction


### Example

```
from joao_marcionilo_finances import Operator

operator = Operator()
operator.post_transaction(
    "999.99", time="2024-09-30", title="Salary", summary="Monthly income"
)
```

### Parameters

| Parameter | Type | Description |
| --------- | ---- | ----------- |
| `value` | `str` | Value of the transaction. Max length 20 |
| `subtraction` | `bool` | True define the value as a subtraction |
| `time` | `str` | Time of the transaction. Max length 26 |
| `title` | `str` | Title of the transaction. Max length 100 |
| `summary` | `str` | Resume of the transaction. Max length 200 |




    