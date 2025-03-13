"""
Models for UP Bank webhook resources
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from upbank.models.base import Links, PaginatedResponse, Relationship

class WebhookAttributes(BaseModel):
    """Attributes of a webhook"""
    url: str
    description: Optional[str] = None
    secret_key: Optional[str] = Field(None, alias="secretKey")
    created_at: str = Field(alias="createdAt")

    model_config = {
        "populate_by_name": True
    }

class WebhookRelationships(BaseModel):
    """Relationships for a webhook"""
    logs: Relationship

    model_config = {
        "populate_by_name": True
    }

class Webhook(BaseModel):
    """Webhook resource"""
    type: str = "webhooks"
    id: str
    attributes: WebhookAttributes
    relationships: WebhookRelationships
    links: Links

    model_config = {
        "populate_by_name": True
    }

class WebhookList(PaginatedResponse[Webhook]):
    """List of webhooks response"""
    pass

class WebhookLogRequest(BaseModel):
    """Request information in a webhook log"""
    body: str

class WebhookLogResponse(BaseModel):
    """Response information in a webhook log"""
    status_code: int = Field(alias="statusCode")
    body: str

    model_config = {
        "populate_by_name": True
    }

class WebhookLogAttributes(BaseModel):
    """Attributes of a webhook log"""
    request: WebhookLogRequest
    response: Optional[WebhookLogResponse] = None
    delivery_status: str = Field(alias="deliveryStatus")
    created_at: str = Field(alias="createdAt")

    model_config = {
        "populate_by_name": True
    }

class WebhookLogRelationships(BaseModel):
    """Relationships for a webhook log"""
    webhook_event: Relationship = Field(alias="webhookEvent")

    model_config = {
        "populate_by_name": True
    }

class WebhookLog(BaseModel):
    """Webhook log resource"""
    type: str = "webhook-logs"
    id: str
    attributes: WebhookLogAttributes
    relationships: WebhookLogRelationships
    links: Links

    model_config = {
        "populate_by_name": True
    }

class WebhookLogList(PaginatedResponse[WebhookLog]):
    """List of webhook logs response"""
    pass 