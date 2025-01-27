from typing import Dict, Any, Optional
from .base import ExternalAPIClient
from ...config import settings

class SantanderAPI(ExternalAPIClient):
    def __init__(self):
        super().__init__()
        self.base_url = settings.SANTANDER_API_URL
        
    async def get_balance(self, credentials: Dict[str, Any]) -> float:
        """Obtiene el saldo de una cuenta de Santander"""
        endpoint = f"{self.base_url}/accounts/{credentials['account_id']}/balance"
        headers = self._get_auth_headers(credentials)
        
        async with self.session as client:
            response = await client.get(endpoint, headers=headers)
            response.raise_for_status()
            data = response.json()
            return float(data['balance'])
    
    async def get_transactions(self, credentials: Dict[str, Any], 
                             from_date: Optional[str] = None) -> list:
        """Obtiene las transacciones de una cuenta de Santander"""
        endpoint = f"{self.base_url}/accounts/{credentials['account_id']}/transactions"
        headers = self._get_auth_headers(credentials)
        params = {"from_date": from_date} if from_date else {}
        
        async with self.session as client:
            response = await client.get(endpoint, headers=headers, params=params)
            response.raise_for_status()
            return response.json()['transactions']
    
    def _get_auth_headers(self, credentials: Dict[str, Any]) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {credentials['access_token']}",
            "Content-Type": "application/json"
        } 