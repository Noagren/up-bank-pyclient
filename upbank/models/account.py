"""
Models for UP Bank account resources
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from upbank.models.base import Links, MoneyObject, PaginatedResponse, Relationship

class AccountAttributes(BaseModel):
    """Attributes of an account"""
    display_name: str = Field(alias="displayName")
    account_type: str = Field(alias="accountType")
    ownership_type: str = Field(alias="ownershipType")
    balance: MoneyObject
    created_at: str = Field(alias="createdAt")

    model_config = {
        "populate_by_name": True
    }

class AccountRelationships(BaseModel):
    """Relationships for an account"""
    transactions: Relationship

class Account(BaseModel):
    """Account resource"""
    type: str = "accounts"
    id: str
    attributes: AccountAttributes
    relationships: AccountRelationships
    links: Links

class AccountList(PaginatedResponse[Account]):
    """List of accounts response"""
    pass 