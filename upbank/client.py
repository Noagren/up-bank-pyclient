"""
UP Bank API Client implementation
"""

from typing import Dict, List, Optional, Union
import requests
from pydantic import BaseModel
from requests.exceptions import HTTPError

from upbank.models.account import Account, AccountList
from upbank.models.transaction import Transaction, TransactionList
from upbank.models.category import Category, CategoryList
from upbank.models.tag import Tag, TagList
from upbank.models.webhook import Webhook, WebhookList, WebhookLog, WebhookLogList

class UpClient:
    """
    UP Bank API Client
    
    Args:
        api_key (str): Your UP Bank API key
        base_url (str, optional): Base URL for the API. Defaults to "https://api.up.com.au/api/v1".
    """
    
    def __init__(self, api_key: str, base_url: str = "https://api.up.com.au/api/v1"):
        self.api_key = api_key
        self.token = api_key  # Alias for compatibility
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json"
        }
        self.session.headers.update(self.headers)

    def _request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict] = None,
        json: Optional[Dict] = None
    ) -> Dict:
        """Make a request to the UP API"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        response = self.session.request(method, url, params=params, json=json)
        response.raise_for_status()
        return response.json() if response.content else {}

    def list_accounts(self, page_size: Optional[int] = None) -> AccountList:
        """List all accounts"""
        params = {"page[size]": page_size} if page_size else None
        data = self._request("GET", "/accounts", params=params)
        return AccountList.model_validate(data)

    def get_account(self, account_id: str) -> Account:
        """Get a specific account"""
        data = self._request("GET", f"/accounts/{account_id}")
        return Account.model_validate(data["data"])

    def list_transactions(
        self,
        page_size: Optional[int] = None,
        status: Optional[str] = None,
        since: Optional[str] = None,
        until: Optional[str] = None,
        category: Optional[str] = None,
        tag: Optional[str] = None,
    ) -> TransactionList:
        """List all transactions with optional filters"""
        params = {
            "page[size]": page_size,
            "filter[status]": status,
            "filter[since]": since,
            "filter[until]": until,
            "filter[category]": category,
            "filter[tag]": tag,
        }
        params = {k: v for k, v in params.items() if v is not None}
        data = self._request("GET", "/transactions", params=params)
        return TransactionList.model_validate(data)

    def get_transaction(self, transaction_id: str) -> Transaction:
        """Get a specific transaction"""
        data = self._request("GET", f"/transactions/{transaction_id}")
        return Transaction.model_validate(data["data"])

    def list_categories(self, parent: Optional[str] = None) -> CategoryList:
        """List all categories"""
        params = {"filter[parent]": parent} if parent else None
        data = self._request("GET", "/categories", params=params)
        return CategoryList.model_validate(data)

    def get_category(self, category_id: str) -> Category:
        """Get a specific category"""
        data = self._request("GET", f"/categories/{category_id}")
        return Category.model_validate(data["data"])

    def list_tags(self, page_size: Optional[int] = None) -> TagList:
        """List all tags"""
        params = {"page[size]": page_size} if page_size else None
        data = self._request("GET", "/tags", params=params)
        return TagList.model_validate(data)

    def add_tags_to_transaction(self, transaction_id: str, tags: List[str]) -> None:
        """Add tags to a transaction"""
        json = {
            "data": [{"type": "tags", "id": tag} for tag in tags]
        }
        self._request("POST", f"/transactions/{transaction_id}/relationships/tags", json=json)

    def remove_tags_from_transaction(self, transaction_id: str, tags: List[str]) -> None:
        """Remove tags from a transaction"""
        json = {
            "data": [{"type": "tags", "id": tag} for tag in tags]
        }
        self._request("DELETE", f"/transactions/{transaction_id}/relationships/tags", json=json)

    def update_transaction_category(
        self, transaction_id: str, category_id: Optional[str]
    ) -> None:
        """Update or remove a transaction's category"""
        json = {
            "data": {"type": "categories", "id": category_id} if category_id else None
        }
        self._request(
            "PATCH", 
            f"/transactions/{transaction_id}/relationships/category",
            json=json
        )

    def list_webhooks(self, page_size: Optional[int] = None) -> WebhookList:
        """List all webhooks"""
        params = {"page[size]": page_size} if page_size else None
        data = self._request("GET", "/webhooks", params=params)
        return WebhookList.model_validate(data)

    def create_webhook(self, url: str, description: Optional[str] = None) -> Webhook:
        """Create a new webhook"""
        json = {
            "data": {
                "attributes": {
                    "url": url,
                    "description": description
                }
            }
        }
        data = self._request("POST", "/webhooks", json=json)
        return Webhook.model_validate(data["data"])

    def get_webhook(self, webhook_id: str) -> Webhook:
        """Get a specific webhook"""
        data = self._request("GET", f"/webhooks/{webhook_id}")
        return Webhook.model_validate(data["data"])

    def delete_webhook(self, webhook_id: str) -> None:
        """Delete a webhook"""
        self._request("DELETE", f"/webhooks/{webhook_id}")

    def list_webhook_logs(
        self, webhook_id: str, page_size: Optional[int] = None
    ) -> WebhookLogList:
        """List logs for a specific webhook"""
        params = {"page[size]": page_size} if page_size else None
        data = self._request("GET", f"/webhooks/{webhook_id}/logs", params=params)
        return WebhookLogList.model_validate(data)

    def get_accounts(self, page_size: Optional[int] = None) -> AccountList:
        """Alias for list_accounts"""
        return self.list_accounts(page_size)

    def get_transactions(self, **kwargs) -> TransactionList:
        """Alias for list_transactions"""
        return self.list_transactions(**kwargs)

    def get_categories(self, parent: Optional[str] = None) -> CategoryList:
        """Alias for list_categories"""
        return self.list_categories(parent)

    def get_webhooks(self, page_size: Optional[int] = None) -> WebhookList:
        """Alias for list_webhooks"""
        return self.list_webhooks(page_size)

    def ping(self) -> Dict:
        """Ping the API to check if it's working"""
        return self._request("GET", "/util/ping") 