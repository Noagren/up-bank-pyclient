"""
Base models for the UP API
"""

from typing import Dict, Generic, List, Optional, TypeVar, Union
from pydantic import BaseModel, ConfigDict, Field

class Links(BaseModel):
    """Links object for API resources"""
    self: Optional[str] = None
    related: Optional[str] = None
    prev: Optional[str] = None
    next: Optional[str] = None

class RelationshipData(BaseModel):
    """Data object for relationships"""
    type: str
    id: str

class Relationship(BaseModel):
    """Relationship object for API resources"""
    data: Optional[Union[RelationshipData, List[RelationshipData]]] = None
    links: Optional[Links] = None

class MoneyObject(BaseModel):
    """Money object for currency amounts"""
    currency_code: str
    value: str
    value_in_base_units: int

    model_config = ConfigDict(
        alias_generator=lambda s: "".join(
            word.capitalize() if i > 0 else word.lower()
            for i, word in enumerate(s.split("_"))
        ),
        populate_by_name=True
    )

T = TypeVar("T", bound=BaseModel)

class PaginatedResponse(BaseModel, Generic[T]):
    """Base class for paginated responses"""
    data: List[T]
    links: Links 