from abc import ABC, abstractmethod
import httpx
from typing import Dict, Any, Optional
from ...config import settings

class ExternalAPIClient(ABC):
    def __init__(self):
        self.session = httpx.AsyncClient()
        
    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.aclose()
    
    @abstractmethod
    async def get_balance(self, credentials: Dict[str, Any]) -> float:
        pass
    
    @abstractmethod
    async def get_transactions(self, credentials: Dict[str, Any], 
                             from_date: Optional[str] = None) -> list:
        pass 