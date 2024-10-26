from datetime import date
from typing import Optional, Literal

from pydantic import BaseModel, Field, constr, conint

periods = Literal[
    'month', 'year', 'yyyy', 'yy', 'quarter', 'qq', 'q', 'mm', 'm', 'dayofyear', 'dy', 'y', 'day', 'dd', 'd', 'week',
    'ww', 'wk', 'weekday', 'dw', 'w'
]


class TransactionSend(BaseModel):
    value: constr(max_length=20) = Field(..., example='999,99')
    time: Optional[constr(max_length=26)] = Field('', example='2024-09-30')
    title: Optional[constr(max_length=100)] = Field('', example='Salary')
    summary: Optional[constr(max_length=200)] = Field('', example='Monthly income')
    subtraction: bool = Field(..., description='True means the value is a subtraction')

    class Config:
        orm_mode = True


class TransactionReceive(TransactionSend):
    id: conint(gt=0)

    class Config:
        orm_mode = True


class Changed(BaseModel):
    state: Literal["changed", "unchanged"]


class PeriodicTransactions(BaseModel):
    table: Literal["Incomes", "Expenses"]
    title: constr(max_length=100) = Field(..., example='Salary')
    value: constr(max_length=20) = Field(..., example='999,99')
    interval: periods
    number: conint(gt=0)
    next_date: date
    limit: Optional[int]
    summary: Optional[constr(max_length=200)] = Field(None, example='Monthly income')

    class Config:
        orm_mode = True


class Message(BaseModel):
    message: str
