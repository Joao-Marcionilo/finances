"""
CRUD operations in SQL Server for a personal finances app
"""

from datetime import date

import pyodbc

from default_credential import default_data

_intervals = [
    'month', 'year', 'yyyy', 'yy', 'quarter', 'qq', 'q', 'mm', 'm', 'dayofyear', 'dy', 'y', 'day', 'dd', 'd', 'week',
    'ww', 'wk', 'weekday', 'dw', 'w'
]
_transaction_fields = "id, transactionValue, transactionDate, title, summary"
_transaction_converted = ("id", "value", "time", "title", "summary")
_periodic_fields = "title, transactionValue, await, awaitValue, nextDate, limit, summary"
_periodic_converted = ("title", "value", "interval", "number", "next_date", "limit", "summary", "table")


class Operator:
    def __init__(self, credentials=default_data, database="Finances"):
        """
        Initialize the operator to utilize its CRUD methods
        :param credentials: Configure the connection credentials of the SQL
        :param database: Define the database custom name
        """
        self.credential = None
        self.config(credentials=credentials, database=database)

    def _sql(self, command, *parameters, fetch=0, autocommit=False):
        with (pyodbc.connect(self.credential, autocommit=autocommit)) as conn:
            cursor = conn.cursor()
            cursor.execute(command, parameters)
            if fetch: return cursor.fetchall()
            cursor.commit()

    def config(self, credentials=default_data, database="Finances"):
        """
        Configure the credentials of the database and its name
        :param credentials: Configure the connection credentials of the SQL
        :param database: Define the database custom name
        """
        self.credential = credentials
        self._sql(f"""
        IF NOT EXISTS(SELECT * FROM sys.databases WHERE name = '{database}')
        BEGIN CREATE DATABASE {database} END
        """, autocommit=True)
        self.credential = f"{credentials}DATABASE={database};"

        def config_table(table: str, columns: str):
            self._sql(f"""
            IF NOT EXISTS(SELECT * FROM sysobjects WHERE name='{table}' AND xtype='U')
            CREATE TABLE {table}({columns})
            """, autocommit=True)

        config_table("Registries", """
        id int PRIMARY KEY,
        transactionValue varchar(20) NOT NULL,
        transactionDate varchar(26),
        title varchar(100),
        summary varchar(200)
        """)
        self._sql("""
        IF NOT EXISTS (SELECT * FROM Registries)
        INSERT INTO Registries(id, transactionValue) VALUES(0, '')
        """)
        for each in ("Incomes", "Expenses"):
            config_table(each, """
        title varchar(100) PRIMARY KEY,
        transactionValue varchar(20) NOT NULL,
        await varchar(20) NOT NULL,
        awaitValue INT NOT NULL,
        nextDate date NOT NULL,
        limit int,
        summary varchar(200)
            """)

    def get_transaction(self, update=True, start=0, quantity=0) -> list:
        """
        Fetch for the registries of all transactions
        :param update: Define if the registry should be updated with the out of date periodic incomes and
        expenses before fetching. Default = True
        :param start: Define how many transactions should be omitted from the newest to oldest registries
        :param quantity: Define a limit of transactions to return
        :return: registries
        """
        if update: self.patch_transaction()
        (limit_query, parameters) = ("FETCH FIRST ? ROWS ONLY", (start, quantity)) if quantity else ("", (start, ))
        registries = self._sql(f"""
        SELECT {_transaction_fields} FROM Registries
        WHERE id != 0
        ORDER BY id DESC
        OFFSET ? ROWS
        {limit_query}
        """, *parameters, fetch=1)
        return [
            {col: valor for col, valor in zip(_transaction_converted, registry)}
            for registry in registries
        ]

    def post_transaction(self, value:str, time="", title="", summary=""):
        """
        Registry a new transaction
        :param value: Value of the transaction. Max length 20
        :param time: Time of the transaction. Max length 26
        :param title: Title of the transaction. Max length 100
        :param summary: Resume of the transaction. Max length 200
        """
        self._sql(f"""
        INSERT INTO Registries({_transaction_fields})
        VALUES(1+(SELECT TOP 1 id FROM Registries ORDER BY id DESC), ?, ?, ?, ?)
        """, value, time, title, summary)

    def delete_transaction(self, identifier:int):
        """
        Delete a transaction
        :param identifier: ID of the transaction to delete
        """
        self._sql(f"DELETE FROM Registries WHERE id = ? AND id != 0", identifier)

    def patch_transaction(self) -> str:
        """
        Update the registries with the transactions in "Incomes" and "Expenses" tables that reached their date
        :return: Confirmation if the table was updated
        """
        changed = False
        to_registry = []
        while True:
            for table in ("Incomes", "Expenses"):
                to_registry += self._sql(f"""
                SELECT transactionValue, nextDate, title, summary, await, awaitValue, '{table}'
                FROM {table} WHERE CONVERT(DATE, GETDATE()) > nextDate
                """, fetch=1)
            if not to_registry: break
            print(to_registry)
            for fields in to_registry:
                self._sql(f"""
                UPDATE {fields[6]}
                SET nextDate = DATEADD({fields[4]}, ?, nextDate)
                WHERE title = ?
                UPDATE {fields[6]}
                SET limit = limit - 1
                WHERE title = ? AND limit > 0
                DELETE FROM {fields[6]} WHERE limit = 0
                """, fields[5], fields[2], fields[2])
                self.post_transaction(fields[0], time=fields[1], title=fields[2], summary=fields[3])
            to_registry = []
            changed = True
        changed = "changed" if changed else "unchanged"
        return changed

    def get_periodic_transactions(self) -> list:
        """
        Fetch for the proprieties of all periodic transactions of "Incomes" and "Expenses" tables
        :return: Information of the periodic transactions
        """
        result = []
        for table in ("Incomes", "Expenses"):
            for transaction in self._sql(f"SELECT {_periodic_fields} FROM {table}", fetch=1):
                result.append({x: y for x, y in zip(_periodic_converted, list(transaction)+[table])})
        print(result)
        return result

    def post_periodic_transactions(
            self, table:str, title:str, value:str, interval:str, number:int, next_date:date, limit=-1, summary=""
    ) -> tuple:
        """
        Add a new periodic transaction in the "Incomes" or "Expenses" tables
        :param table: "Incomes" or "Expenses"
        :param title: Title of the transaction. Max length 100
        :param value: Value of the transaction. Expenses should start with a "-". Max length 20
        :param interval: Define the "interval" of the SQL Server function "DATEADD"
        :param number: Define the "number" of the SQL Server function "DATEADD"
        :param next_date: Date of the next transaction
        :param limit: Add a maximum number of times this transaction can be used
        :param summary: Resume of the transaction. Max length 200
        """
        if table not in ("Incomes", "Expenses"):
            raise ValueError(f"invalid option string '{table}': should be 'Incomes' or 'Expenses'")
        if interval not in _intervals:
            raise ValueError(f"invalid option '{interval}': should be one of the following {_intervals}"
        )
        if number < 1:
            raise ValueError(f"number parameter should be greater than 0 ")
        if not isinstance(next_date, date):
            raise TypeError("next_date parameter should be instance of datetime.date")
        try:
            self._sql(f"""
            INSERT INTO {table}({_periodic_fields})
            VALUES(?, ?, LOWER(?), ?, ?, ?, ?)
            """, title, value, interval, number, next_date, limit, summary, fetch=0)
            return 201, f"'{title}' created in '{table}' table"
        except pyodbc.IntegrityError as ex:
            if ex.args[0] == "23000": return 409, f"'{title}' already exist in '{table}' table"
            raise ex

    def delete_periodic_transactions(self, table:str, title:str):
        """
        Delete a periodic transaction in the "Incomes" or "Expenses" tables
        :param table: Table of the transaction
        :param title: Title of the transaction
        """
        if table not in ("Incomes", "Expenses"):
            raise ValueError(f"invalid option string '{table}': should be 'Incomes' or 'Expenses'")
        self._sql(f"DELETE FROM {table} WHERE title = ?", title)
