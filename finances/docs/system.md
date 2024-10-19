# App System

CRUD operations in SQL Server for a personal finances app

## Configuration

### `config(**credential, **database)`

For the module to work appropriately it needs to be configured using `config` method

```
from Joao-Marcionilo-finances import sistema

credential="""
    DRIVER={ODBC Driver 17 for SQL Server};
    SERVER=localhost;
    TRUSTED_CONNECTION=yes;
"""

sistema.config(
    credential=credential, database="MyPersonalFinance"
)
```

### Parameters

| Parameter    | Type   | Description                                     |
|--------------|--------|-------------------------------------------------|
| **credential | string | Configure the connection credentials of the SQL |
| **database   | string | Define the database custom name                 |

## Get all transactions from "Registries" table

### `get_transaction(**update, **start, **quantity)`

Fetch for the registries of all transactions

```
from Joao-Marcionilo-finances import sistema

sistema.config()
registries = sistema.get_transaction(start=0, quantity=20)
print(registries)
```

### Parameters

| Parameter  | Type    | Description                                                                                                                 |
|------------|---------|-----------------------------------------------------------------------------------------------------------------------------|
| **update   | boolean | Define if the registry should be updated with the out of date periodic incomes and expenses before fetching. Default = True |
| **start    | integer | Define by which transaction should start, from newest to oldest                                                             |
| **quantity | integer | Define a limit of transactions to return                                                                                    |

## Add transaction to "Registries" table

### `post_transaction(value, **time, **title, **summary)`

Registry a new transaction

```
from Joao-Marcionilo-finances import sistema

sistema.config()
sistema.post_transaction(
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

### `delete_transaction(identifier)`

Delete an transaction

```
from Joao-Marcionilo-finances import sistema

sistema.config()
sistema.delete_transaction(1)
```

### Parameters

| Parameter  | Type    | Description                     |
|------------|---------|---------------------------------|
| identifier | integer | ID of the transaction to delete |

## Update "Registries" table

### `patch_transactions()`

Update the registries with the transactions in "Incomes" and "Expenses" tables that reached their date

```
from Joao-Marcionilo-finances import sistema

sistema.config()
situation = sistema.patch_transaction()
print(situation)
```

## Get all transactions from "Incomes" and "Expenses" tables

### `get_periodic_transactions()`

Fetch for the proprieties of all periodic transactions of "Incomes" and "Expenses" tables

```
from Joao-Marcionilo-finances import sistema

sistema.config()
transactions = sistema.get_transaction()
print(transactions)
```

## Add transaction to "Incomes" or "Expenses" tables

### `post_periodic_transactions(title, value, period, next_date, **limit, **summary)`

Add a new periodic transaction in the "Incomes" or "Expenses" tables

```
from datetime import date

from Joao-Marcionilo-finances import sistema

sistema.config()
# Creates an income of that is updated each 
transactions = sistema.post_periodic_transactions(
    "Salary", "999.99", ("MONTH", 1), date(2024, 9, 17),
    limit=12, summary="Monthly income"
)
```

### Parameters

| Parameter  | Type    | Description                                                 | Max Length |  
|------------|---------|-------------------------------------------------------------|------------|
| title      | string  | Title of the transaction                                    | 100        | 
| value      | string  | Value of the transaction                                    | 20         | 
| period     | tuple   | Define the two first values of the SQL function "DATEADD"   | -          | 
| next_date  | date    | Date of the next transaction                                | -          | 
| **limit    | integer | Add an maximum number of times this transaction can be used | -          | 
| **summary  | string  | Resume of the transaction                                   | 200        | 


## Delete transaction from "Incomes" or "Expenses" tables

### `delete_periodic_transactions(table, title)`

Delete a periodic transaction in the "Incomes" or "Expenses" tables

```
from Joao-Marcionilo-finances import sistema

sistema.config()
sistema.delete_periodic_transactions("Incomes", "Salary")
```

### Parameters

| Parameter     | Type    | Description              |  
|---------------|---------|--------------------------|
| table         | string  | Table of the transaction | 
| title         | string  | Title of the transaction |