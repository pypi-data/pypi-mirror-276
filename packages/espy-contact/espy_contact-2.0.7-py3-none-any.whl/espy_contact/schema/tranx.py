from datetime import datetime, date
from typing import Optional, Union
from pydantic import BaseModel
from espy_contact.util.enums import StatusEnum, NigerianBank


class TranxDto(BaseModel):
    id: Optional[int] = None
    ref: str
    stripeId: Optional[str] = None
    amount: float
    currency: Optional[str] = "NGN"
    status: Optional[StatusEnum] = StatusEnum.PENDING
    payee_id: Optional[int]  # Assuming Appuser has an ID field
    detail: Optional[Union[dict, str]] = None  # Can be dict or string for flexibility
    createdOn: Optional[datetime]
    modifiedOn: Optional[datetime]


class AccountDto(BaseModel):
    id: Optional[int] = None
    bank: NigerianBank
    account_name: str
    account_number: str
    currency: str
    is_active: bool
    account_officer: str
    account_admin: str
    created: datetime
    modified: datetime


class FeeDto(BaseModel):
    classroom_id: str
    fee_name: str
    amount: float
    due_date: date
    start_date: date
    status: StatusEnum
