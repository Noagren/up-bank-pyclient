"""
UP Bank API client usage example
"""

from upbank.client import UpClient
from upbank.models import (
    Account,
    AccountList,
    Transaction,
    TransactionList,
    Category,
    CategoryList,
    Tag,
    TagList,
    Webhook,
    WebhookList,
)

def init_client() -> UpClient:
    """Initialize the UP Bank client using API key from .env file"""
    from dotenv import load_dotenv
    import os
    
    load_dotenv()
    api_key = os.getenv("UP_API_KEY")
    if not api_key:
        raise Exception("UP_API_KEY not found in .env file")
        
    client = UpClient(api_key)
    ping_response = client.ping()
    if "meta" in ping_response and "statusEmoji" in ping_response["meta"]:
        print(f"Successfully connected to UP API {ping_response['meta']['statusEmoji']}")
        return client
    else:
        raise Exception("Failed to connect to UP API")

def get_accounts(client: UpClient) -> AccountList:
    """Get all accounts"""
    accounts = client.list_accounts()
    for account in accounts.data:
        print(f"Account: {account.id}")
        print(f"Type: {account.type}")
        print(f"Name: {account.attributes.display_name}")
        print(f"Balance: {account.attributes.balance.value}")
    return accounts

def main():
    """Main function to run the UP Bank API client usage example"""
    client = init_client()
    print("Connected to UP Bank API")

    accounts = get_accounts(client)
    print(f"Retrieved {len(accounts.data)} accounts")

if __name__ == "__main__":
    main()