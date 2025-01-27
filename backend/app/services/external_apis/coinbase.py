from typing import Dict, Any, Optional
from .base import ExternalAPIClient
from ...config import settings

class CoinbaseAPI(ExternalAPIClient):
    def __init__(self):
        super().__init__()
        self.base_url = settings.COINBASE_API_URL
        
    async def get_balance(self, credentials: Dict[str, Any]) -> float:
        """Obtiene el saldo de una cuenta de Coinbase"""
        endpoint = f"{self.base_url}/accounts/{credentials['account_id']}"
        headers = self._get_auth_headers(credentials)
        
        async with self.session as client:
            response = await client.get(endpoint, headers=headers)
            response.raise_for_status()
            data = response.json()
            return float(data['data']['balance']['amount'])
    
    async def get_transactions(self, credentials: Dict[str, Any], 
                             from_date: Optional[str] = None) -> list:
        """Obtiene las transacciones de una cuenta de Coinbase"""
        endpoint = f"{self.base_url}/accounts/{credentials['account_id']}/transactions"
        headers = self._get_auth_headers(credentials)
        params = {"start_time": from_date} if from_date else {}
        
        async with self.session as client:
            response = await client.get(endpoint, headers=headers, params=params)
            response.raise_for_status()
            return response.json()['data']
    
    def _get_auth_headers(self, credentials: Dict[str, Any]) -> Dict[str, str]:
        return {
            "CB-ACCESS-KEY": credentials["api_key"],
            "CB-ACCESS-SIGN": credentials["signature"],
            "CB-ACCESS-TIMESTAMP": credentials["timestamp"],
            "Content-Type": "application/json"
        } 