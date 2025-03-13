"""
Models for UP Bank category resources
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from upbank.models.base import Links, PaginatedResponse, Relationship, RelationshipData

class CategoryAttributes(BaseModel):
    """Attributes of a category"""
    name: str

class CategoryRelationships(BaseModel):
    """Relationships for a category"""
    parent: Optional[Relationship] = Field(default_factory=lambda: Relationship(data=None))
    children: Relationship = Field(default_factory=lambda: Relationship(data=[]))

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "examples": [
                {
                    "parent": {
                        "data": None,
                        "links": {
                            "related": None
                        }
                    },
                    "children": {
                        "data": [],
                        "links": {
                            "related": "https://api.up.com.au/api/v1/categories/test-category-id/children"
                        }
                    }
                }
            ]
        }
    }

class Category(BaseModel):
    """Category resource"""
    type: str = "categories"
    id: str
    attributes: CategoryAttributes
    relationships: CategoryRelationships
    links: Links

    model_config = {
        "populate_by_name": True
    }

class CategoryList(PaginatedResponse[Category]):
    """List of categories response"""
    pass 