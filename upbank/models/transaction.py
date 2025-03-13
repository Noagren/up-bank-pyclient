"""
Models for UP Bank transaction resources
"""

from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from upbank.models.base import Links, PaginatedResponse, Relationship, RelationshipData, MoneyObject

class HoldInfo(BaseModel):
    """Hold info object"""
    amount: MoneyObject
    foreignAmount: Optional[MoneyObject] = None

class CardPurchaseMethod(BaseModel):
    """Card purchase method object"""
    method: str
    deviceId: Optional[str] = None

class Note(BaseModel):
    """Note object"""
    value: str
    createdAt: datetime

class Customer(BaseModel):
    """Customer object"""
    id: str
    displayName: str

class TransactionAttributes(BaseModel):
    """Attributes of a transaction"""
    status: str
    rawText: Optional[str] = None
    description: str
    message: Optional[str] = None
    isCategorizable: bool
    holdInfo: Optional[HoldInfo] = None
    roundUp: Optional[MoneyObject] = None
    cashback: Optional[MoneyObject] = None
    amount: MoneyObject
    foreignAmount: Optional[MoneyObject] = None
    cardPurchaseMethod: Optional[CardPurchaseMethod] = None
    settledAt: Optional[datetime] = None
    createdAt: datetime
    transactionType: Optional[str] = None
    note: Optional[Note] = None
    performingCustomer: Optional[Customer] = None

class TransactionRelationships(BaseModel):
    """Relationships for a transaction"""
    account: Relationship = Field(default_factory=lambda: Relationship(data=RelationshipData(type="accounts", id="")))
    transferAccount: Optional[Relationship] = Field(default_factory=lambda: Relationship(data=None))
    category: Optional[Relationship] = Field(default_factory=lambda: Relationship(data=None))
    parentCategory: Optional[Relationship] = Field(default_factory=lambda: Relationship(data=None))
    tags: Relationship = Field(default_factory=lambda: Relationship(data=[]))

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "examples": [
                {
                    "account": {
                        "data": {
                            "type": "accounts",
                            "id": "test-account-id"
                        },
                        "links": {
                            "related": "https://api.up.com.au/api/v1/accounts/test-account-id"
                        }
                    },
                    "transferAccount": {
                        "data": None,
                        "links": {
                            "related": None
                        }
                    },
                    "category": {
                        "data": None,
                        "links": {
                            "related": None
                        }
                    },
                    "parentCategory": {
                        "data": None,
                        "links": {
                            "related": None
                        }
                    },
                    "tags": {
                        "data": [],
                        "links": {
                            "related": "https://api.up.com.au/api/v1/transactions/test-transaction-id/tags"
                        }
                    }
                }
            ]
        }
    }

class Transaction(BaseModel):
    """Transaction resource"""
    type: str = "transactions"
    id: str
    attributes: TransactionAttributes
    relationships: TransactionRelationships
    links: Links

    model_config = {
        "populate_by_name": True
    }

class TransactionList(PaginatedResponse[Transaction]):
    """List of transactions response"""
    pass 