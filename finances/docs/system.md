# App's System

CRUD operations in SQL Server for a personal finances app

## Initialization

**Class:** `Operator(**credential, **database)`

Initialize the `Operator` to utilize its CRUD methods

### Example

```
from Joao-Marcionilo-finances.system import Operator

operator = Operator()
```

### Parameters

| Parameter    | Type   | Description                                             |
|--------------|--------|---------------------------------------------------------|
| **credential | string | Configure the connection credentials of the SQL         |
| **database   | string | Define the database custom name. Default = `"Finances"` |


### Methods

- `config`: Configure the credentials of the database and its name
- `get_transaction`: Fetch for the registries of all transactions
- `post_transaction`: Registry a new transaction
- `delete_transaction`: Delete a transaction
- `patch_transaction`: Update the registries with the transactions in "Incomes" and "Expenses" tables that reached their date
- `get_periodic_transactions`: Fetch for the proprieties of all periodic transactions of "Incomes" and "Expenses" tables
- `post_periodic_transactions`: Add a new periodic transaction in the "Incomes" or "Expenses" tables
- `delete_periodic_transactions`: Delete a periodic transaction in the "Incomes" or "Expenses" tables

## Configuration

**Method:** `config(**credential, **database)`

The `Operator` also can be configured alter its initialization using the `config` method

### Example

```
from Joao-Marcionilo-finances.system import Operator

credential="""
    DRIVER={ODBC Driver 17 for SQL Server};
    SERVER=localhost;
    TRUSTED_CONNECTION=yes;
"""

operator = Operator()
operator.config(credential=credential, database="MyPersonalFinance")
```

### Parameters

| Parameter    | Type   | Description                                             |
|--------------|--------|---------------------------------------------------------|
| **credential | string | Configure the connection credentials of the SQL         |
| **database   | string | Define the database custom name. Default = `"Finances"` |

## Get all transactions from "Registries" table

**Method:** `get_transaction(**update, **start, **quantity)`

Fetch for the registries of all transactions

### Example

```
from Joao-Marcionilo-finances.system import Operator

operator = Operator()
registries = operator.get_transaction(start=0, quantity=20)
print(registries)
```

### Parameters

| Parameter  | Type    | Description                                                                                                                   |
|------------|---------|-------------------------------------------------------------------------------------------------------------------------------|
| **update   | boolean | Define if the registry should be updated with the out of date periodic incomes and expenses before fetching. Default = `True` |
| **start    | integer | Define how many transactions should be omitted from the newest to oldest registries                                           |
| **quantity | integer | Define a limit of transactions to return                                                                                      |

## Add transaction to "Registries" table

**Method:** `post_transaction(value, **time, **title, **summary)`

Registry a new transaction

### Example

```
from Joao-Marcionilo-finances.system import Operator

operator = Operator()
operator.post_transaction(
    "999.99", time="2024-09-30", title="Salary", summary="Monthly income"
)
```

### Parameters

| Parameter | Type   | Description               | Max Length |
|-----------|--------|---------------------------|------------|
| value     | string | Value of the transaction  | 20         |
| **time    | string | Time of the transaction   | 26         |
| **title   | string | Title of the transaction  | 100        |
| **summary | string | Resume of the transaction | 200        |

## Delete transaction from "Registries" table

**Method:** `delete_transaction(identifier)`

Delete a transaction

### Example

```
from Joao-Marcionilo-finances.system import Operator

operator = Operator()
operator.delete_transaction(1)
```

### Parameters

| Parameter  | Type    | Description                     |
|------------|---------|---------------------------------|
| identifier | integer | ID of the transaction to delete |

## Update "Registries" table

**Method:** `patch_transaction()`

Update the registries with the transactions in "Incomes" and "Expenses" tables that reached their date

### Example

```
from Joao-Marcionilo-finances.system import Operator

operator = Operator()
state = operator.patch_transaction()
print(state)
```

## Get all transactions from "Incomes" and "Expenses" tables

**Method:** `get_periodic_transactions()`

Fetch for the proprieties of all periodic transactions of "Incomes" and "Expenses" tables

### Example

```
from Joao-Marcionilo-finances.system import Operator

operator = Operator()
transactions = operator.get_transaction()
print(transactions)
```

## Add transaction to "Incomes" or "Expenses" tables

**Method:** `post_periodic_transactions(title, value, interval, number, next_date, **limit, **summary)`

Add a new periodic transaction in the "Incomes" or "Expenses" tables

### Example

```
from datetime import date

from Joao-Marcionilo-finances.system import Operator

operator = Operator()
# Creates an income of that is updated each 
transactions = operator.post_periodic_transactions(
    "Salary", "999.99", "MONTH", 1, date(2024, 9, 17),
    limit=12, summary="Monthly income"
)
```

### Parameters

| Parameter | Type    | Description                                                                           | Max Length |  
|-----------|---------|---------------------------------------------------------------------------------------|------------|
| table     | string  | "Incomes" or "Expenses"                                                               | -          |
| title     | string  | Title of the transaction                                                              | 100        | 
| value     | string  | Value of the transaction. Expenses should start with a `"-"`                          | 20         | 
| interval  | string  | Define the "interval" of the SQL Server function "DATEADD". Must be higher than a day | -          | 
| number    | integer | Define the "number" of the SQL Server function "DATEADD"                              | -          | 
| next_date | date    | Date of the next transaction                                                          | -          | 
| **limit   | integer | Add a maximum number of times this transaction can be used                            | -          | 
| **summary | string  | Resume of the transaction                                                             | 200        | 


## Delete transaction from "Incomes" or "Expenses" tables

**Method:** `delete_periodic_transactions(table, title)`

Delete a periodic transaction in the "Incomes" or "Expenses" tables

### Example

```
from Joao-Marcionilo-finances.system import Operator

operator = Operator()
operator.delete_periodic_transactions("Incomes", "Salary")
```

### Parameters

| Parameter     | Type    | Description              |  
|---------------|---------|--------------------------|
| table         | string  | "Incomes" or "Expenses"  | 
| title         | string  | Title of the transaction |